function charting(email, duration){

    var response = $.ajax({
        type: "POST",
        url: "/humidity/" + email + "/chart",
        data: duration,
        async: false,
        dataType: "text"
    }).responseText;
    
    var dict = JSON.parse(response);
    var time = [];
    var value = [];
    for(var key in dict){
        if(dict.hasOwnProperty(key)){
            value.push(dict[key]);
            time.push(key);
        }
    }

    if (duration == "168"){
        for(var i=0; i < time.length; i++){
            var res = time[i].split("T", 2)
            time[i] = res[0]
        }
        
        var date_7 = [];
        var value_7 = [];
        var count = 1;
        var day = 6;
        date_7.push(time[time.length-1])
        value_7.push(value[value.length-1])
        for(var i = time.length - 1; i > 0; i--){
          if(time[i] == time[i - 1]){
            value_7[0] += value[i - 1];
            count+=1;
          }
          else{
            if(day == 0){
              break;
            }
            value_7.unshift(value[i - 1]);
            value_7[1] = value_7[1] / count;
            count = 1;
            date_7.unshift(time[i - 1]);
            day-=1;
          }
        }
        value_7[0] = value_7[0] / count;
        time = date_7;
        value = value_7;
    }
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [{
            label: 'Last 24 Hours',
            data: value,
            backgroundColor: "rgba(153,255,51,0.4)"
            }]
        }
    });
}