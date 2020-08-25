function charting(email, duration, sensor){

    //send request to backent to get data
    var response = $.ajax({
        type: "POST",
        url: "/chart/" + email + "/" + sensor,
        data: duration,
        async: false,
        dataType: "text"
    }).responseText;
    
    //parse data into two array
    //one for timestamp, one for value
    var dict = JSON.parse(response);
    var time = [];
    var value = [];
    for(var key in dict){
        if(dict.hasOwnProperty(key)){
            value.push(dict[key]);
            time.push(key);
        }
    }

    //deal with CO2 outliers(>10000) by let it
    //equal to the previous one
    for(var i=0; i< value.length; i++){
      value[i] = parseFloat(value[i])
      if(value[i] > 10000){
        value[i] = value[i - 1];
      }
    }

    //request one week chart
    if (duration == "168"){
        for(var i=0; i < time.length; i++){
            var res = time[i].split("T", 2)//Split timestamp to get just the date
            time[i] = res[0]
        }
        
        var date_7 = [];
        var avg = [];
        var count = 1;
        var day = 6;
        date_7.push(time[time.length-1])
        avg.push(value[value.length-1])
        for(var i = time.length - 1; i > 0; i--){
          if(time[i] == time[i - 1]){ //If two adjacent value are from same day, add them together
            avg[0] += value[i - 1];
            count+=1;
          }
          else{
            if(day == 0){
              break;
            }
            avg[0] = avg[0] / count;//If not, get the average of the added value. 
            avg.unshift(value[i - 1]);
            count = 1;
            date_7.unshift(time[i - 1]);
            day-=1;
          }
        }
        avg[0] = avg[0] / count; //Take care of edge case
        time = date_7;
        value = avg;
    }

    //request all-time chart
    var date_all = [];
    var avg = [];
    var max = [];
    var min = [];
    var count = 1;
    if (duration == "100000") {
      for(var i=0; i < time.length; i++){
        var res = time[i].split("T", 2) //Split timestamp to get just the date
        time[i] = res[0]
      }
      date_all.push(time[time.length-1]);
      avg.push(value[time.length-1]);
      max.push(value[time.length-1]);
      min.push(value[time.length-1]);
      
      for(var i = time.length - 1; i > 0; i--){
        if(time[i] == time[i - 1]){
          avg[0] += value[i - 1]; //If two adjacent value are from same day, add them together
          count += 1;
          if (value[i - 1] > max[0]){ //Track max
            max[0] = value[i - 1];
          }
          if (value[i - 1] < min[0]){ //Track min
            min[0] = value[i - 1];
          }
        }
        else{
          avg[0] = avg[0] / count;//If not, get the average of the added value. 
          avg.unshift(value[i - 1]);
          min.unshift(value[i - 1]);
          max.unshift(value[i - 1]);
          count = 1;

          date_all.unshift(time[i - 1]);
        }
      }
      avg[0] = avg[0] / count; //take care of edge case
      value = avg;
      time = date_all;
    }

    //Building the chart
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [
            { 
              data: value,
              label: "average",
              backgroundColor: "rgba(153,255,51,0.4)"
            },
            {
              data: min,
              label: "min"
            },
            {
              data: max,
              label: "max"
            }
          ]
        }
    });
}