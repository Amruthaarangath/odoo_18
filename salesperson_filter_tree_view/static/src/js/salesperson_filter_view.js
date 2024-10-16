/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { Component } from "@odoo/owl";
import { listView } from '@web/views/list/list_view';
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";


// the controller usually contains the Layout and the renderer.
class CustomListController extends ListRenderer {
    static template = "salesperson_filter_tree_view.Selection";
    setup() {
       super.setup();
       }
       async onClick(ev) {
        console.log("yy")
    }
//    static template = "web.WebClient";
//    static template = "web.WebClient";
//    console.log("hyyyy")
    // Your logic here, override or insert new methods...
    // if you override setup(), don't forget to call super.setup()
}


CustomListController.template = "salesperson_filter_tree_view.Selection";
//console.log("hyy")
//    selector: '.selection_list',
//            events: {
//            'change #partner_id': 'render_function'
//            },
//    render_function : function(){
//    var self = this;
//    var template_window =  $(QWeb.render("salesperson_filter_tree_view.Selection", {
////            console.log("hlo")
//            partners : self.partners,
//            }));
//    template_window.appendTo(this.$el);
//  },


export const customListView = {
    ...listView, // contains the default Renderer/Controller/Model
    Controller: CustomListController,
};

// Register it to the views registry
registry.category("views").add("custom_list", customListView);

