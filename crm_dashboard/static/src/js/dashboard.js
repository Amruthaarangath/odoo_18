/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";


var uid = session.storeData.Store.odoobot.id
//console.log("thiss",session.storeData.Store.odoobot.id)
class CrmDashboard extends Component {
   setup() {
         super.setup()
         this.orm = useService('orm')
         this._fetch_data()
         this.action = useService("action");

   }
   _fetch_data(){
   var self = this;
   this.orm.call("crm.lead", "get_tiles_data", [], {}).then(function(result){
           document.getElementById('my_lead').append( result.total_leads );
           document.getElementById("my_opportunity").append(result.total_opportunity);
           document.getElementById("revenue").append(result.currency + result.expected_revenue);
           document.getElementById("revenue_total").append(result.currency + result.revenue_total);
           });
       };
       async leadTile() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            domain:[['type', "=", 'lead'],["user_id", "=", uid]],
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list']],
        });
    }
    async oppourtunityTile() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Oppourtunity'),
            target: 'current',
            domain:[['type', "=", 'opportunity'],["user_id", "=", uid]],
            res_model: 'crm.lead',
            views: [[false, 'list']],
        });
    }
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
