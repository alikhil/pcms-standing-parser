$(function(){

    function getUrlVars() {
        var vars = {};
        var parts = decodeURIComponent(window.location.href).replace(
            /[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
          vars[key] = value;
        });
        return vars;
    }  

    function navigate(button)
    {
        console.log("lo");
        console.log($(button));
        var page = $(button).attr("page");
        var link = collectFilters() + "&page="+page;
        console.log(link);
        $(button).prop("href", link);
    }

    function collectFilters() {
        var range = $("#date-range").val();
        var group = $("#groupInput").val();
        console.log("group:" + group);
        var groupKeyVal = "";
        if (group !== undefined && group !== "") {
            groupKeyVal = "&group=" + group;
        }
        return "/submissions?range="+range + groupKeyVal;
    }
    
    $("#earlierButton").click(function() {
        navigate(this);
    });
    $("#laterButton").click(function() {
        navigate(this);
    });

    $("#filterButton").click(function(){
        var link = collectFilters();
        console.log(link);
        $(this).prop("href", link);
    });

    var group = getUrlVars()["group"];
    if (group !== undefined) {
        $("#groupInput").val(decodeURI(group));
    }

    function configurePicker()
    {
        var range = getUrlVars()["range"];
        var start = moment().subtract(29, "days");
        var end = moment();

        if (range !== undefined) {
            var dates = range.split("-");
            start = moment(dates[0], "DD.MM.YYYY");
            end = moment(dates[1], "DD.MM.YYYY");
        }

        function cb(start, end) {
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
        }, cb);

        cb(start, end);
    }

    configurePicker();


});