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

    //Building the 24-hour chart
    if (duration=="24" || duration=="168"){
      
      //set color, title and label based on data type and duration
      var borderColor = "#FFFFFF";
      var backgroundColor = "#FFFFFF";
      var title = "N/A";
      var yLable = "N/A";
      if (sensor == "Humidity"){
        yLable = "Humidity";
        if(duration=="24"){
          borderColor = "#3e95cd";
          backgroundColor = "#3e95cd";
          title = "Humidity - Last 24 Hours";
        }
        else if(duration=="168"){
          borderColor = "#42A1F9";
          backgroundColor = "#42A1F9";
          title = "Humidity - Last 7 Days";
        }
      }
      else if (sensor == "Temperature"){
        yLable = "Temperature";
        borderColor = "#F55F5F";
        backgroundColor = "#F55F5F";
        if(duration=="24"){
          title = "Temperature - Last 24 Hours";
        }
        else if(duration=="168"){
          title = "Temperature - Last 7 Days";
        }
      }
      else if (sensor == "CO2"){
        borderColor = "#29BF38";
        backgroundColor = "#29BF38";
        yLable = "Co2 (in ppm)";
        if(duration=="24"){
          title = "Co2 - Last 24 Hours";
        }
        else if(duration=="168"){
          title = "Co2 - Last 7 Days"
        }
      }

      //this part actually builds the chart
      var ctx = document.getElementById('myChart');
      var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: time,  //this line takes in x-axis labels
          datasets: [
          { 
            data: value,  //this line takes in data
            label: "Average", //line label
            borderColor: borderColor,
            backgroundColor: backgroundColor
          }  
          ]
        },
        options: {
          legend: {
            display: true,
            labels: {
              boxWidth: 14, 
            }
          },
          title: {
            display: true,
            text: title,
            fontSize: 22,
            fontStyle: 'bold'  
          },
          scales: {
            yAxes: [{
              ticks: {
                //Add unit to data based on data type
                callback: function(value, index, values) {
                  if (sensor == "Humidity"){
                    return value + '%';
                  }
                  else if (sensor == "Temperature"){
                    return value + '°C';
                  }
                  else if (sensor == "CO2"){
                    return value;
                  }
                }
              },
              scaleLabel: {
                display: true,
                labelString: yLable,
                fontStyle: 'bold'
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Time',
                fontStyle: 'bold'
                }
            }]
          }
        }
      });
    }
    else{

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
}