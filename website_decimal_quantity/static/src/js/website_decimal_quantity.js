/** @odoo-module **/

import { WebsiteSale } from '@website_sale/js/website_sale';
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import VariantMixin from "@website_sale/js/sale_variant_mixin";
import { localization } from "@web/core/l10n/localization";
import { insertThousandsSep } from "@web/core/utils/numbers";


WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        'click .oe_website_sale': 'onClickAddCartJSON',
        'change .oe_cart input.js_quantity[data-product-id]': '_onChangeCartQuantity',
        'change .js_main_product [data-attribute_exclusions]': 'onChangeVariant',
        'click input.js_product_change': 'onChangeVariant',
        'change .js_main_product [data-attribute_exclusions]': 'onChangeVariant',
    }),

    onClickAddCartJSON: function (ev, $dom_optional) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
//        var productPrice = $parent.find('.product_price');
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = (($link.has(".fa-minus").length ? -(0.1) : (0.1)) + previousQty).toFixed(1);
        var newQty = (quantity > min ? (quantity < max ? quantity : max) : min);


        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },
    _onChangeCartQuantity: function (ev) {
        var $input = $(ev.currentTarget);
        if ($input.data('update_change')) {
            return;
        }
        var value = parseFloat($input.val() || 0, 10);
        if (isNaN(value)) {
            value = 0.1;
        }
        var $dom = $input.closest('tr');
//        var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
        var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        var line_id = parseInt($input.data('line-id'), 10);
        var productIDs = [parseInt($input.data('product-id'), 10)];
        this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
    },

        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            $($dom_optional).toArray().forEach((elem) => {
                $(elem).find('.js_quantity').text(value);
                productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
            });
            $input.data('update_change', true);

            rpc("/shop/cart/update_json", {
                line_id: line_id,
                product_id: parseInt($input.data('product-id'), 10),
                set_qty: value,
                display: true,
            }).then((data) => {
                $input.data('update_change', false);
                var check_value = parseFloat($input.val() || 0, 10);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value === check_value) {
                    $input.trigger('change');
                    return;
                }
                if (!data.cart_quantity) {
                    return window.location = '/shop/cart';
                }
                $input.val(data.quantity);
                console.log($input.val(data.quantity))
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).text(data.quantity);

                wSaleUtils.updateCartNavBar(data);
                wSaleUtils.showWarning(data.notification_info.warning);
                // Propagating the change to the express checkout forms
                Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
                console.log("amount",data.amount,".minor_amount",data.minor_amount)
            });
        },

});
export default WebsiteSale;

