const clientNameList = [];
const clientcountList = [];
var y2Values = [];
var y1Values = [];

async function fetchDataAndCreateCharts() {
    try {
        const response = await fetch("/static/json/clientData.json");
        if (response.ok) {
            const data = await response.json();
            exportData(data);
            
            if (window.fetchedData) {
                for (const id in window.fetchedData['clientImageList']) {
                    const clientId = window.fetchedData.clientImageList[id];
                    const clientName = clientId.clientsName;
                    clientNameList.push(clientName);
                    const clientCount = clientId.clientsCount;
                    clientcountList.push(clientCount);
                }
                const prints = window.fetchedData.print_Image_data.printImageCount;
                const site = window.fetchedData.site_Image_data.siteImageCount;
                const client = window.fetchedData.client_Image_data.clientImageCount;
                const total = window.fetchedData.total_Image_data.totalImageCount;
                y2Values.push(site, client, prints);
                y1Values.push(20000 - total, total);
				
                createCharts();
            } else {
                console.log("No data available yet.");
            }
        } else {
            console.log("Error in retrieval");
        }
    } catch (error) {
        console.log("ERROR:", error);
    }
}

function exportData(data) {
    window.fetchedData = data;
}

function createCharts() {
    
	if (document.querySelector('[id*="BreakDown"]')) {
		new Chart("BreakDown", {
			type: "doughnut",
			data: {
			  labels: ["Site", "Client", "Prints"],
			  datasets: [
				{
				  backgroundColor: ["#7933FC", "#B6FC33", "#33FCDD"],
				  data: y2Values,
				},
			  ],
			},
			options: {
			  elements: {
				arc: {
				  borderWidth: 0, 
				},
			  },
			  cutout: "90%",
			  plugins: {
				legend: {
				  display: true,
				},
			  },
			},
		});
	};



	if (document.querySelector('[id*="Totals"]')) {
		new Chart("Totals", {
		type: "doughnut",
		data: {
				labels: ["Remaining Storage","Total Stored"],
				datasets: [{
					backgroundColor: ["#7933FC", "#B6FC33"],
					data: y1Values
				}]
			},
			options: {
				elements: {
				arc: {
					borderWidth: 0, 
				},
				},
				cutout: "90%",
				plugins: {
				legend: {
					display: true,
				},
				},
			},
		});
	};

	if (document.querySelector('[id*="clientImageChart1"]')) {
		new Chart('clientImageChart1', {
			type: 'bar',
			data: {
				labels: clientNameList,
				datasets: [{
					label: 'Number of Client images',
					data: clientcountList,
					backgroundColor: (context) => {
						const bgColor = [
							"#7933FC",
							"#33FCDD",
							"#B6FC33"
						];
						if (!context.chart.chartArea) {
							return bgColor;
						}
						const {chartArea: { left, right } } = context.chart;
						const gradientBg = context.chart.ctx.createLinearGradient(left, 0, right, 0);
						gradientBg.addColorStop(1, bgColor[2]);
						gradientBg.addColorStop(0.7, bgColor[1]);
						gradientBg.addColorStop(.6, bgColor[0]);
						return gradientBg;
					},
					borderWidth: 0,
					width: 14
				}]
			},
			options: {
				scales: {
					y: {
						beginAtZero: true,
						grid: {
							color: '#252525',
							lineWidth: 1
						}
					},
					x: {
						grid: {
							color: '#474747',
							lineWidth: 1
						}
					}
				},
				indexAxis: 'y',
				barPercentage: 0.9,
				categoryPercentage: 0.1

			}
		});
	};
	
	breakdownChart.update();
	totalsChart.update();
	clientImageChart.update();
}

fetchDataAndCreateCharts();
