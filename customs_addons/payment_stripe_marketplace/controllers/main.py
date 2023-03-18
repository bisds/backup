# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import http, _
from odoo.http import route, request
from odoo.exceptions import Warning
import werkzeug
import requests
import logging
import pprint
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
from odoo.addons.payment_stripe.controllers.main import StripeController

class StripeController(StripeController):
    _checkout_return_url = '/payment/stripe/checkout_return'

    @http.route(_checkout_return_url, type='http', auth='public', csrf=False)
    def stripe_return_from_checkout(self, **data):
        """ Process the data returned by Stripe after redirection for checkout.

        :param dict data: The GET params appended to the URL in `_stripe_create_checkout_session`
        """

        # Retrieve the tx and acquirer based on the tx reference included in the return url
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_feedback_data(
            'stripe', data
        )
        acquirer_sudo = tx_sudo.acquirer_id

        # Fetch the PaymentIntent, Charge and PaymentMethod objects from Stripe
        payment_intent = acquirer_sudo._stripe_make_request(
            f'payment_intents/{tx_sudo.stripe_payment_intent}', method='GET'
        )
        _logger.info("received payment_intents response:\n%s", pprint.pformat(payment_intent))

        res_charge = payment_intent.get("charges").get("data")[0]
        # create receiver
        stripe_mp_receipt_vals = {
            "receipt_email": res_charge.get("receipt_email") and res_charge.get("receipt_email").strip(),
            "charge_obj_id": res_charge.get("id"),
            "balance_txn": res_charge.get("balance_transaction"),
            "transfer": res_charge.get("transfer"),
            "source_id": res_charge.get("source").get("id") if res_charge.get("source") else False,
            "is_paid": "Yes" if res_charge.get("paid") else "No",
            "status": res_charge.get("status"),
            "destination_acc_id": res_charge.get("destination"),
            "amount": format(float(res_charge.get("amount") / 100.00), '.2f') if res_charge.get("amount") else 0.00,
            "currency": res_charge.get("currency"),
            "stripe_response": payment_intent,
            "tx_id": tx_sudo.id
        }
        if not payment_intent.get('destination_acc_id'):
            stripe_mp_receipt_vals.update({
                "destination_acc_id": payment_intent['transfer_data'].get('destination') if res_charge.get('transfer_data') else ''
            })

        request.env["stripe.marketplace.receiver"].sudo().create(stripe_mp_receipt_vals)


        self._include_payment_intent_in_feedback_data(payment_intent, data)
        # Handle the feedback data crafted with Stripe API objects
        request.env['payment.transaction'].sudo()._handle_feedback_data('stripe', data)

        # Redirect the user to the status page
        return request.redirect('/payment/status')

    def _generate_and_pay_seller_payment_by_sripe_mp(self, tx, seller_bill):
        if seller_bill:
            _logger.info('<%s> transaction completed, auto-generated seller bill %s (ID %s) for %s (ID %s)',
                         tx.acquirer_id.name, seller_bill.name, seller_bill.id, tx.sale_order_ids.name, tx.sale_order_ids.id)
            seller_journal_id = request.env['res.config.settings'].get_mp_global_field_value("seller_payment_journal_id")
            journal_obj = request.env["account.journal"].sudo().browse(seller_journal_id) or tx.acquirer_id.journal_id
            if journal_obj:
                seller_bill.action_post()
        else:
            _logger.warning('<%s> transaction completed, could not auto-generate seller bill for %s (ID %s)',
                            tx.acquirer_id.name, tx.sale_order_id.name, tx.sale_order_id.id)

    @http.route('/stripe_mp/authorize', type='http', auth='public')
    def stripe_mp_authorize(self, **post):
        payment_acquirer = request.env["payment.acquirer"].sudo().search(
            [('provider', '=', 'stripe'),("is_mp_stripe", "=", True),('state', '!=', 'disabled')], limit=1)
        if payment_acquirer and payment_acquirer.stripe_mp_client_key:
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if payment_acquirer.stripe_account_type == "express":
                url_type = "https://connect.stripe.com/express/oauth/authorize"
            else:
                url_type = "https://connect.stripe.com/oauth/authorize"
            url = url_type + "?response_type=code&client_id=" + \
                str(payment_acquirer.stripe_mp_client_key) + "&scope=read_write"
            if base_url:
                url = url + "&redirect_uri=" + base_url + "/stripe_mp/oauth/callback"
            return werkzeug.utils.redirect(url)
        else:
            raise Warning(
                _("Stripe marketplace or stripe client key not found."))

    @http.route('/stripe_mp/oauth/callback', type='http', auth="public", website=True)
    def stripe_mp_aouth_return(self, **post):
        """This is the redirect URL used to link seller's account to admin. Redirect after linking process."""
        payment_acquirer = request.env["payment.acquirer"].sudo().search(
            [("is_mp_stripe", "=", True)])
        code = post.get('code')

        if code:
            data = {
                'client_secret': payment_acquirer.stripe_secret_key,
                'grant_type': 'authorization_code',
                'client_id': payment_acquirer.stripe_mp_client_key,
                'code': code
            }
            # Making /oauth/token endpoint POST request
            url = "https://connect.stripe.com/oauth/token"
            response = requests.post(url, params=data)
            # Fetching access_token(using this as marketplace seller's API key)
            access_token = response.json().get('access_token')
            stripe_user_id = response.json().get('stripe_user_id')
            refresh_token = response.json().get('refresh_token')
            stripe_publishable_key = response.json().get('stripe_publishable_key')
            request.env.user.partner_id.sudo().write({
                "stripe_access_token":access_token,
                "stripe_user_id":stripe_user_id,
                "stripe_refresh_token": refresh_token,
                "stripe_publishable_key": stripe_publishable_key
            })
        else:
            request.env.user.partner_id.sudo().write({
                "stripe_access_token":False,
                "stripe_user_id":False,
                "stripe_refresh_token": False,
                "stripe_publishable_key": False
            })
        stripe_mp_setup_menu = request.env['ir.model.data']._xmlid_lookup(
            'payment_stripe_marketplace.stripe_marketplace_setup_menu')[2]
        stripe_mp_setup_action = request.env['ir.model.data']._xmlid_lookup(
            'payment_stripe_marketplace.stripe_marketplace_setup_action')[2]
        new_url = "/web#view_type=form&model=stripe.marketplace.setup&menu_id=" + \
            str(stripe_mp_setup_menu) + "&action=" + \
            str(stripe_mp_setup_action)
        return request.redirect(new_url)

    @http.route(['/payment_stripe/order/validate',], type='json', auth="public", methods=['POST'], website=True)
    def payment_stripe_order_validate(self, **post):
        order = request.website.sale_get_order()
        
        if order:
            # onboard_seller_ids = order.get_onboard_seller_ids()

            sellers = order.order_line.mapped('product_id').mapped('marketplace_seller_id')
            if len(sellers) > 1:
                return "You can not checkout multiple seller's products at once."
            # if len(onboard_seller_ids) > 1:
            #     return "You can not checkout multiple seller's products at once"
            other_sellers = order.order_line.mapped('product_id').mapped('marketplace_seller_id').filtered(lambda sel: not sel.stripe_user_id and not sel.stripe_access_token)
            
            if other_sellers:
                return "You can not checkout current seller's product using stripe payment getway."
            for line in order.order_line:
                if not line.is_delivery:
                    if sellers and not line.product_id.marketplace_seller_id:
                        return "You can not checkout seller's and admin's products together."
        return False
