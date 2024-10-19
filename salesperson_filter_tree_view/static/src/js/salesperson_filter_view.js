/** @odoo-module **/
import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
import { Component, onWillStart, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { ForecastSearchModel } from "@crm/views/forecast_search_model";
import { SearchModel } from "@web/search/search_model";


class CustomListController extends ListController{
    setup(){
        super.setup();

        this.orm = useService("orm")
        this.state = useState({
            partner_id : [],
            partner: ''
       });
        onWillStart(async ()=>{
            this.partner_id = await this.orm.searchRead('res.users',[], ['id','name']);
            this.state.partner_id = this.partner_id
            console.log(this.partner_id,"idididi")
    });

    }
    updateFilter() {
        console.log("ssss", this.state.partner)
            let partnerId = this.state.partner
//            let partnerId = partnerint.name
//        const filters = partnerId ? [[['user_id', '=', partnerId]]] : [];
        const updated_filters = this.env.searchModel.splitAndAddDomain(`[['user_id', '=', 'Marc Demo']]`)
        console.log("hiii",partnerId)
        console.log("hloooo",updated_filters)
//        this.updateFilter(filters);
//        self.updateFilter(filters).push
//        this.updateFilter();

    }
}
CustomListController.template = "salesperson_filter_tree_view.Selection"
export const CustomListView = {
    ...listView,
    Controller: CustomListController,
};

registry.category("views").add('salesperson_filter', CustomListView);
console.log('registry',registry.category("views"))
