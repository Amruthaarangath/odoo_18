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
//            this.renderGraphChart();
//            return () => {
//                if (this.chart) {
//                    this.chart.destroy();
//                }
//            }
            });
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
        renderDoughnutChart(){
            const Banner = 1
            const Direct = 2
            console.log("doughnut_chart")
            var chart = new Chart("doughnut_chart", {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [Banner, Direct],
                    backgroundColor: ["#1f77b4", "#dddddd"],
//                    data: [0, 10, 20, 30, 40]
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
                         left: 1000
                    },
                },
                plugins: {
                    title: {
                        display: true,
                        text: this.title,
                        padding: 4,
                    },
                aspectRatio: 2,
            },
            }
            });
//        }
    }
    renderPieChart(){
        var chart = new Chart("pie_chart", {
        type: "pie",
        data: {
            datasets: [{
                backgroundColor: ["orange", "green"],
                data: [0, 10, 20, 30, 40]
            }]
        },
        options: {circumference: 500,
                rotation: 270,
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                     padding: {
                         right: 1000,
                    },
                },
                plugins: {
                    title: {
                        display: true,
                        text: this.title,
                        padding: 4,
                    },
                aspectRatio: 2,
            },
            }
    });
}
renderLineChart(){
    var chart = new Chart("line_chart", {
        type: "line",
        data: {
            labels: [10, 20, 30, 40, 50],
            datasets: [{
                data: [10, 20, 30, 40, 50],
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
//            plugins: {
//                legend: { display: false },
//                tooltip: {
//                    intersect: false,
//                    position: "nearest",
//                    caretSize: 0,
//                },
//        },
        }
    });
    }

    renderBarChart(){
        var newww = this.orm.call("crm.lead", "get_bar_data",  [], {}).then(function(result){
        leads,
        opportunity
        })
        console.log("bnm",newww.leads_len)
        var chart = new Chart("bar_chart", {
        type: "bar",
        data: {
            labels: ["leads","opportunities"],
            datasets: [{
                backgroundColor: ["green","orange"],
                data: [newww.leads_len,newww.opportunity_len]
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
    }

}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
