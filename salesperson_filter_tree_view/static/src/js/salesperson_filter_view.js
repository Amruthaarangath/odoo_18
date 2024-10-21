/** @odoo-module **/
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { Component, onWillStart, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";


class CustomListController extends ListController{
    setup(){
        super.setup();
        this.orm = useService("orm")
        this.state = useState({
            partner_id : [],
            partner: '',
       });
        onWillStart(async ()=>{
            this.partner_id = await this.orm.searchRead('res.users',[], ['id','display_name']);
            this.state.partner_id = this.partner_id
    });

    }
    updateFilter(ev) {
            let a = this.state.partner_id.map(item => item.id)
            ev.matchingPartner = this.state.partner
            console.log("a", ev.target.value)
//            console.log("a", ev.matchingPartner)
            const updated_filters = this.env.searchModel.splitAndAddDomain(`[['user_id', 'ilike', '${ev.target.value}']]`)
    }
}
CustomListController.template = "salesperson_filter_tree_view.Selection"
export const CustomListView = {
    ...listView,
    Controller: CustomListController,
};

registry.category("views").add('salesperson_filter', CustomListView);
