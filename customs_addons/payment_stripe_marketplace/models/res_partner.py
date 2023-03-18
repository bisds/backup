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

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    stripe_access_token = fields.Char("Stripe Access Token", readonly="1")
    stripe_user_id = fields.Char("Stripe User Id", readonly="1")
    stripe_refresh_token = fields.Char("Stripe Refresh Token", readonly="1")
    stripe_publishable_key = fields.Char("Stripe Publishable Key", readonly="1")