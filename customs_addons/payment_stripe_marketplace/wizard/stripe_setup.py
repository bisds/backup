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

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import requests
import logging
_logger = logging.getLogger(__name__)

class StripeMarketplaceSetup(models.TransientModel):
    _name = "stripe.marketplace.setup"
    _description = "This model is used for Connecting to Standalone Stripe Accounts(that is controlled by the account holder: your platform's user i.e. seller by integrating OAuth)"

    @api.depends("mp_seller_id.stripe_access_token")
    def _get_stripe_status(self):
        for rec in self:

            if rec.mp_seller_id and rec.mp_seller_id.stripe_access_token:
                rec.is_oauth_done = True
            else:
                rec.is_oauth_done = False

    mp_seller_id = fields.Many2one("res.partner", string="Seller", default=lambda self: self.env.user.partner_id)
    is_oauth_done = fields.Boolean("OAuth Done", compute="_get_stripe_status")

    def integrating_stripe_oauth(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url':   "/stripe_mp/authorize",
        }

    def deauthorize_stripe_oauth(self):

        self.ensure_one()
        payment_acquirer = self.env["payment.acquirer"].sudo().search(
            [("is_mp_stripe", "=", True)])
        stripe_user_id = self.env.user.partner_id.sudo().stripe_user_id
        if stripe_user_id:
            if payment_acquirer and payment_acquirer.stripe_mp_client_key:
                deauth_url = "https://connect.stripe.com/oauth/deauthorize"
                r = requests.post(deauth_url,
                    auth=(payment_acquirer.stripe_secret_key, ''),
                    params={"client_id":str(payment_acquirer.stripe_mp_client_key), "stripe_user_id":stripe_user_id})
                return_stripe_user_id = r.json().get("stripe_user_id")
                if return_stripe_user_id == stripe_user_id:
                    self.env.user.partner_id.sudo().write({
                        "stripe_access_token":False,
                        "stripe_user_id":False,
                        "stripe_refresh_token": False,
                        "stripe_publishable_key": False
                    })
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                    }
                else:
                    raise Warning(_("Stripe account does not exist."))
            else:
                raise Warning(
                    _("Stripe marketplace or stripe client key not found."))
        else:
            raise Warning(
                _("Seller has not stripe id. "))
