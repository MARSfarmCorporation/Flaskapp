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

    for(var i=0; i< value.length; i++){
      value[i] = parseFloat(value[i])
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
            value_7[0] = value_7[0] / count;
            value_7.unshift(value[i - 1]);
            count = 1;
            date_7.unshift(time[i - 1]);
            day-=1;
          }
        }
        value_7[0] = value_7[0] / count;
        time = date_7;
        value = value_7;
    }

    var date_all = [];
    var value_all = [];
    var max = [];
    var min = [];
    var count = 1;
    if (duration == "100000") {
      for(var i=0; i < time.length; i++){
        var res = time[i].split("T", 2)
        time[i] = res[0]
      }
      date_all.push(time[time.length-1]);
      value_all.push(value[time.length-1]);
      max.push(value[time.length-1]);
      min.push(value[time.length-1]);
      
      for(var i = time.length - 1; i > 0; i--){
        if(time[i] == time[i - 1]){
          value_all[0] += value[i - 1];
          count += 1;
          if (value[i - 1] > max[0]){
            max[0] = value[i - 1];
          }
          if (value[i - 1] < min[0]){
            min[0] = value[i - 1];
          }
        }
        else{
          value_all[0] = value_all[0] / count;
          value_all.unshift(value[i - 1]);
          min.unshift(value[i - 1]);
          max.unshift(value[i - 1]);
          count = 1;

          date_all.unshift(time[i - 1]);
        }
      }
      value_all[0] = value_all[0] / count;
      value = value_all;
      time = date_all;
    }

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [{
            data: value,
            backgroundColor: "rgba(153,255,51,0.4)"
            },
            {
              data: min
            },
            {
              data: max
            }
          ]
        }
    });
}