/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillUnmount, useEffect, useState, useRef} from  "@odoo/owl";
const actionRegistry = registry.category("actions");
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { user } from "@web/core/user";



class CrmDashboard extends Component {
   setup() {
         super.setup()
         this.orm = useService('orm')
         this.action = useService("action");
//         this.doughnut = null;
//         this.pie = null;
//         this.line = null;
//         this.bar = null;
//         this.table = null;
         this.dataFilter = useRef("dataFilter");
         this.fetchData = useRef("leadData");
         console.log("this.dataFilter",(this.dataFilter))

   onWillUnmount(async() => {

            this.renderBarChart();
            this.renderLineChart();
            this.renderDoughnutChart();
            this.renderPieChart();
//            this.renderTableChart();
            this.filterDasboard();
   });

         this.state = useState({
            month : [],
            monthLead : [],
            filter: '',
            fetch_data:{},
        });

        onWillStart(async ()=>{
              this._fetch_data()
//            this.renderBarChart();
//            this.renderLineChart();
//            this.renderDoughnutChart();
////            this._fetch_data()
//            this.renderPieChart();
//            this.renderTableChart();
//            this.filterDasboard();
        });


   }

   _fetch_data(){
   var self = this;
   const filter_value = this.state.filter
   this.orm.call("crm.lead", "get_tiles_data", [filter_value], {}).then((result)=> {
           this.state.fetch_data = result
//           document.getElementById('my_lead').append( result.total_leads );
//           document.getElementById("my_opportunity").append(result.total_opportunity);
//           document.getElementById("revenue").append(result.currency + result.expected_revenue);
//           document.getElementById("revenue_total").append(result.currency + result.revenue_total);
//           document.getElementById("lead_ratio").append(result.lead_ratio);
           });
//        }
       }
    async dashboardUsers(){
           this.normalUser = await user.hasGroup("sales_team.group_sale_salesman");
           this.CrmUser = await user.hasGroup("sales_team.group_sale_salesman_all_leads");
           this.CrmManager = await user.hasGroup("sales_team.group_sale_manager");
    }

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

        async renderBarChart(){
        var self = this;
        if (this.bar){
            console.log("barrrrrrrrrrrrr")
            this.bar.destroy()
        }
            const filter_value = this.state.filter
            await this.orm.call("crm.lead", "get_bar_data",  [filter_value], {}).then(function(result){
            console.log('this',self)

            self.bar = new Chart(document.getElementById('bar_chart'), {
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

        async renderLineChart(){
        var self = this;
        if (this.line){
            this.line.destroy()
        }
        const filter_value = this.state.filter
        await this.orm.call("crm.lead", "get_line_data",  [filter_value], {}).then((result)=> {

        self.line = new Chart(document.getElementById('line_chart'), {
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
//        }
        })
        }

        async renderDoughnutChart(){
        var self = this
        if (this.doughnut){
            this.doughnut.destroy()
        }
        const filter_value = this.state.filter
        await this.orm.call("crm.lead", "get_doughnut_data",  [filter_value], {}).then((result)=> {
            self.doughnut = new Chart(document.getElementById('doughnut_chart'), {
            type: "doughnut",
            data: {
                labels: result.medium_name,
                datasets: [{
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
    }
        async renderPieChart(){
        var self = this;
            if (this.pie){
                this.pie.destroy()
            }
         const filter_value = this.state.filter
         await this.orm.call("crm.lead", "get_pie_data",  [filter_value], {}).then((result)=> {
            self.pie = new Chart(document.getElementById('pie_chart'), {
            type: "pie",
            data: {
                labels: result.activity_name,
                datasets: [{
                    backgroundColor: ["orange", "green","red","blue"],
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

    async renderTableChart(){
        var self = this;
        if (this.table){
            this.table.destroy()
        }
         const filter_value = this.state.filter
         await this.orm.call("crm.lead", "get_table_data",  [filter_value], {}).then((result) => {
                self.table = document.getElementById('table_chart')
                this.state.month = result.final_month_name
                this.state.monthLead = result.leads_month_length
            })
    }


    async filterDasboard(){
        const filter_value = this.state.filter
        await this.orm.call("crm.lead", "get_filter_data",  [filter_value], {}).then((result) => {
            this.renderBarChart(),
            this.renderLineChart(),
            this.renderDoughnutChart(),
            this.renderPieChart(),
            this._fetch_data()
//            this.renderTableChart()
//            this.renderDoughnutChart()








        });
//            if (this.bar != null){
//                this.bar.destroy()
//            }
//            else{

//        }
////            var self = this;
//            this.orm.call("crm.lead", "get_tiles_data", [filter_value], {}).then((result)=> {
//            this.state.fetch_data = result
//           });
//         }


//        if (filter = null){
//            console.log("hyy")
//        }
//        else{
//            const filter_value = filter.value;
//            await this.orm.call("crm.lead", "get_filter_data",  [filter_value], {}).then((result) => {
//    //            const filter_value = document.getElementById('filter').value;
//    //            console.log("filter",filter)
//                var today =  luxon.DateTime.now();
//                console.log("today",today.c)
//                var this_month = (today.c).month
//                console.log("this_month",this_month)
//                var this_year =  (today.c).year
//                console.log("this_year",this_year)

////            });
//            }


//        if (this.user == this.CrmUser || this.user == this.CrmManager){
////            if (filter == "This month"){
////                console.log("mmmooonnthhhh");
////            }
//
//
//        }
        }
//    }

}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
