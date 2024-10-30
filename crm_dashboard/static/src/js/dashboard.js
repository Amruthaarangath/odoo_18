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
         this.barChart = useRef("barChart");
         this.lineChart = useRef("lineChart")
         this.fetchData = useRef("leadData");
         this.doughnutChart = useRef("doughnutChart");
         this.pieChart = useRef("pieChart");
         this.tableChart = useRef("tableChart");
         console.log("this.dataFilter",(this.dataFilter))

   this.state = useState({
            month : [],
            monthLead : [],
            filter: '',
            fetch_data:{},
        });

   onWillUnmount(async() => {
            this.renderBarChart();
            this.renderLineChart();
            this.renderDoughnutChart();
            this.renderPieChart();
            this.renderTableChart();
            this.filterDasboard();
   });

        onWillStart(async ()=>{
              this._fetch_data();
            this.renderBarChart();
            this.renderLineChart();
            this.renderDoughnutChart();
            this.renderPieChart();
            this.renderTableChart();
        });
   }

   _fetch_data(){
   var self = this;
   const filter_value = this.state.filter
   this.orm.call("crm.lead", "get_tiles_data", [filter_value], {}).then((result)=> {
           this.state.fetch_data = result
           });
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
            this.bar.destroy()
        }
            const filter_value = this.state.filter
            await this.orm.call("crm.lead", "get_bar_data",  [filter_value], {}).then(function(result){

            self.bar = new Chart(self.barChart.el.id, {
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

        self.line = new Chart(self.lineChart.el.id, {
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

        async renderDoughnutChart(){
        var self = this
        if (this.doughnut){
            this.doughnut.destroy()
        }
        const filter_value = this.state.filter
        await this.orm.call("crm.lead", "get_doughnut_data",  [filter_value], {}).then((result)=> {
            self.doughnut = new Chart(self.doughnutChart.el.id, {
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
            self.pie = new Chart(self.pieChart.el.id, {
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
         const filter_value = this.state.filter
         await this.orm.call("crm.lead", "get_table_data",  [filter_value], {}).then((result) => {
                self.table = self.tableChart.el.id
                this.state.month = result.final_month_name
                this.state.monthLead = result.leads_month_length
                console.log(this.state)
            })
    }
    async filterDasboard(){
        if (this.user == this.CrmUser || this.user == this.CrmManager){
            const filter_value = this.state.filter
            await this.orm.call("crm.lead", "get_filter_data",  [filter_value], {}).then((result) => {
                this.renderBarChart(),
                this.renderLineChart(),
                this.renderDoughnutChart(),
                this.renderPieChart(),
                this.renderTableChart(),
                this._fetch_data()

            });
            }
        }
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
