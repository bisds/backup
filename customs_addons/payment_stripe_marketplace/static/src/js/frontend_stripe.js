/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('payment_stripe_markeptlace.frontent_stripe', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');
    var PaymentForm = require('payment.checkout_form');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.PaymentCheckoutForm.include({

        _onClickPaymentOption: function(ev){
            var self = this;
            this._super.apply(this, arguments);
            var checked_radio = this.$('input[type="radio"]:checked');
            var error_div = $('.paypal_stripe_error');
            if (checked_radio.length !== 1) {
                return;
            }
            checked_radio = checked_radio[0];
            var provider = checked_radio.dataset.provider
            if(provider == 'stripe'){
                $('#o_payment_submit_button').hide();
                return self._rpc({
                    route: "/payment_stripe/order/validate",
                }).then(function (error) {
                    if(error){
                        self.$('input[type="radio"]:checked').prop('checked', false);
                        error_div.text(error);
                        error_div.show();
                        const $submitButton = $('button[name="o_payment_submit_button"]');
                        $submitButton.attr('disabled', true);
                    }
                    else{
                        error_div.text("");
                        error_div.hide();
                    }
                });
            }
            else{
                    error_div.text("");
                    error_div.hide();
                }

        },
    });

});