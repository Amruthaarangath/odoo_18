/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
    publicWidget.registry.return_order = publicWidget.Widget.extend({
        selector: '#quote_content',
        events: {
            'click #hidden_box_btn': '_onHiddenBoxBtnClick',
            'change #product': '_onProductChange',
        },
        /**
         * @override
         */

        _onHiddenBoxBtnClick: function (ev) {
            var self = this;
            ev.preventDefault();
            self.$('#hidden_box').modal('show');
        },

        _onProductChange: function (ev) {
            var self = this;
            var $product = $(ev.currentTarget);
            var $submitButton = self.$('#submit');
            $submitButton.toggleClass('d-none', $product.val() === 'none');
        },
    });