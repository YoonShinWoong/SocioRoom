function openNav() {
    document.getElementById("mySidenav").style.width = "180px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
//chart
new Chart(document.getElementById("chart_1"),
    {
        "type":"doughnut",
        "data":{
            labels: [
                '1A',
            ],
            "datasets":[
                {   
                    "data":[1, 2],
                    "backgroundColor":["rgba(255, 205, 86)","rgba(79, 81, 81, .3)"],
                    "borderWidth": 0.3
                },
            ]
        }
    });
new Chart(document.getElementById("chart_2"),
    {
        "type":"doughnut",
        "data":{
            labels: [
                '1B',
            ],
            "datasets":[
                {
                    "data":[2, 1],
                    "backgroundColor":["rgba(255, 99, 132)","rgba(79, 81, 81, .3)"],
                    "borderWidth": 0.3
                }
            ]
        }
    });
new Chart(document.getElementById("chart_3"),
    {
        "type":"doughnut",
        "data":{
            labels: [
                '3A',
            ],
            "datasets":[
                {
                    "data":[1, 3],
                    "backgroundColor":["rgba(54, 162, 235)","rgba(79, 81, 81, .3)"],
                    "borderWidth": 0.3
                }
            ]
        }
    });