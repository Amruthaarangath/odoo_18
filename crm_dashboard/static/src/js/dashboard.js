/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useEffect} from  "@odoo/owl";
const actionRegistry = registry.category("actions");
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { user } from "@web/core/user";


class CrmDashboard extends Component {
   setup() {
         super.setup()
         this.orm = useService('orm')
//         this.user = useService('user')
         this._fetch_data()
         this.action = useService("action");
         this.chart = null;

         useEffect(() => {
            this.renderDoughnutChart();
            this.renderPieChart();
            this.renderLineChart();
            this.renderBarChart();

            });
//         this.state = useState({
//            month[],
//        });
   }

   _fetch_data(){
//   console.log(user, "0000000")
   var self = this;
   this.orm.call("crm.lead", "get_tiles_data", [], {}).then(function(result){
           document.getElementById('my_lead').append( result.total_leads );
           document.getElementById("my_opportunity").append(result.total_opportunity);
           document.getElementById("revenue").append(result.currency + result.expected_revenue);
           document.getElementById("revenue_total").append(result.currency + result.revenue_total);
           document.getElementById("lead_ratio").append(result.lead_ratio);
           });
//        }
       };
//    async dashboardUsers(){
//           await normalUser = user.hasGroup("sales_team.group_sale_salesman"),
//           await CrmUser = user.hasGroup("sales_team.group_sale_salesman_all_leads"),
//           await CrmManager = user.hasGroup("sales_team.group_sale_manager"),
//    }

       async leadTile() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            domain:[['type', "=", 'lead'],["user_id", "=", user.userId]],
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
                domain:[['type', "=", 'opportunity'],["user_id", "=", user.userId]],
                res_model: 'crm.lead',
                views: [[false, 'list']],
            });

        }
        async renderDoughnutChart(){
            await this.orm.call("crm.lead", "get_doughnut_data",  [], {}).then(function(result){
                var chart = new Chart(document.getElementById('doughnut_chart'), {
                type: "doughnut",
                data: {
                    labels: result.medium_name,
                    datasets: [{
//                        data: [result.leads_medium],
                        backgroundColor: ["#1f77b4", "#dddddd", "blue", "green", "red"],
                        data: result.leads_medium
                    }]
                },
                options: {
                    circumference: 500,
                    rotation: 270,
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "70%",
                    layout: {
                        padding: {
                             left: 30
                        },
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Doughnut Chart",
                            padding: 4,
                        },
                    aspectRatio: 2,
                },
                }
                });
                })
    //        }
        }
    async renderPieChart(){
         await this.orm.call("crm.lead", "get_pie_data",  [], {}).then(function(result){
            var chart = new Chart(document.getElementById('pie_chart'), {
            type: "pie",
            data: {
                labels: result.activity_name,
                datasets: [{
                    backgroundColor: ["orange", "green"],
                    data: result.leads_activity
                }]
            },
            options: {circumference: 500,
                    rotation: 270,
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                         padding: {
                             right: 100,
                        },
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Pie Chart",
                            padding: 4,
                        },
                    aspectRatio: 2,
                },
                }
        });
        })
    }
    async renderLineChart(){
        await this.orm.call("crm.lead", "get_line_data",  [], {}).then(function(result){
        var chart = new Chart(document.getElementById('line_chart'), {
            type: "line",
            data: {
                labels: result.campaign_name,
                datasets: [{
                    data: result.leads_campaign,
                    pointBackgroundColor: "red",
                }]
            },
            options: {circumference: 1000,
                    rotation: 300,
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: 30,
                    },
                plugins: {
                    legend: { display: false },
                    text: "Line Chart",
                    tooltip: {
                        intersect: false,
                        caretSize: 0,
                    },
            },
            }
        });
        })
        }

    async renderBarChart(){
        await this.orm.call("crm.lead", "get_bar_data",  [], {}).then(function(result){
        var chart = new Chart(document.getElementById('bar_chart'), {
        type: "bar",
        data: {
            labels: ["leads","opportunities"],
            datasets: [{
                data: [result.leads,result.opportunity],
                backgroundColor: ["green","orange"],
            }]
        },
        options: {circumference: 1000,
                rotation: 300,
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: 30,
                     left: 50
                },
            plugins: {
                legend: { display: false },
                tooltip: {
                    intersect: false,
                    position: "nearest",
                    caretSize: 0,
                },
        },
        }
    });
    })
    }

}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
