# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Odoo Marketplace Stripe Connect",
  "summary"              :  """Odoo Marketplace Stripe Connect - will split the payment among the seller(s) and admin dynamically.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "http://www.webkul.com",
  "description"          :  """""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=payment_stripe_marketplace&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'website_payment',
                             'odoo_marketplace',
                             'payment_stripe',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'wizard/stripe_setup_view.xml',
                             'views/res_partner_view.xml',
                             'views/payment_views.xml',
                             'data/stripe_mp_payment_acquirer_data.xml',
                             'data/seller_payment_method_data.xml',
                             'views/templates.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  'assets': {
        'web.assets_frontend': [
            'payment_stripe_marketplace/static/src/js/frontend_stripe.js',
            'payment_stripe_marketplace/static/src/css/frontent_stripe.css',
        ],
    },
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  125,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
