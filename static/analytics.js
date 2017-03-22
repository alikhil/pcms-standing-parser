$(function(){

    function sortKeys(obj, datef) {
        datef = datef || "MM-YYYY";
        var keys = Object.keys(obj);
        keys.sort(function(a,b){ return moment(a, datef) - moment(b, datef);});
        return keys;
    }
    function drawChart(data) {
        $("#myChart").remove();
        $("#charts").append("<canvas id='myChart' width='400' height='170'></canvas>");
        var context = $("#myChart");
        var datef = data.data_type == "month" ? "MM-YYYY" : "DD-MM-YYYY";
        
        
        var all = JSON.parse(data.all);
        var allKeys = sortKeys(all, datef);
        var allValues = allKeys.map(k => all[k]);

        var success = JSON.parse(data.success);
        var successValues = allKeys.map((k) => Object.hasOwnProperty.call(success, k) ?  success[k] : 0);

        var chartType = data.data_type == "month" ? "bar" : "line";
        var myChart = new Chart(context, {
            type: chartType,
            data: {
                labels: allKeys,
                datasets: [{
                    label: '# Успешных посылок',
                    data: successValues,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: "# всего попыток",
                    data: allValues,
                    backgroundColor:'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    }

    var data_type = "month";

    function collectFilters() {
        var range = $("#date-range").val();
        var group = $("#groupInput").val();
        var groupKeyVal = "";
        if (group !== undefined && group !== "") {
            groupKeyVal = "&group=" + group;
        }
        return "/pcms_standings/analytics/get_data?range="+range + groupKeyVal + "&data_type=" + data_type;
    }
    

    $(".dropdown-menu li a").click(function(){
        var selText = $(this).text();
        data_type = $(this).attr("val");
        console.log(data_type);
        console.log("drop down click");
        $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
    });

    $("#filterButton").click(function(){
        var url = collectFilters();
        $.ajax({
            url
        }).done(function(data, err) {
            console.log("analytics: sucseed");
            console.info(data);
            drawChart(data);
        }).fail(function(err) {
            console.error(err);
        });
    });

    
    function configurePicker()
    {
        
        var start = moment("01.09.2016", "DD.MM.YYYY");
        var end = moment();
        

        function updateDatePicker(start, end) {
            $("#reportrange span").html(start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY"));
            $("#date-range").val(start.format("D.MM.YYYY") + "-" + end.format("D.MM.YYYY"));
        }

        $("#reportrange").daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                "Сегодня": [moment(), moment()],
                "Вчера": [moment().subtract(1, "days"), moment().subtract(1, "days")],
                "Последние 7 дней": [moment().subtract(6, "days"), moment()],
                "Последние 30 дней": [moment().subtract(29, "days"), moment()],
                "Текущий месяц": [moment().startOf("month"), moment().endOf("month")],
                "Прошлый месяц": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")],
                "За все время": [moment("20160110","YYYYDDMM"), moment()]
            }
        }, updateDatePicker);

        updateDatePicker(start, end);
    }

    configurePicker();
    

});