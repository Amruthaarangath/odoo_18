/** @odoo-module **/
import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
import { Component, onWillStart, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";


class CustomListController extends ListController{
    setup(){
        super.setup();

        this.orm = useService("orm")
        this.state = useState({
            partner_id : [],
        });
        onWillStart(async ()=>{
            this.partner_id = await this.orm.searchRead('res.users',[], ['id','name']);
            this.state.partner_id = this.partner_id
            console.log(this.partner_id,"idididi")

    });
//    updateFilter(partnerId) {
//        const filters = partnerId ? [[['user_id', '=', partnerId]]] : [];
//        console.log("hyyyy")
//        this.updateFilter(filters);
//    }

        }
    updateFilter(partner_id) {
        const filters = partner_id ? [[['user_id', '=', partner_id]]] : [];
        console.log("hyyyy",filters)
        this.updateFilter(filters);
    }
}
CustomListController.template = "salesperson_filter_tree_view.Selection"
export const CustomListView = {
    ...listView,
    Controller: CustomListController,
};

registry.category("views").add('salesperson_filter', CustomListView);
console.log('registry',registry.category("views"))
