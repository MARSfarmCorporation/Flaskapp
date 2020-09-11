function compare_chart(email, fst_sensor, sec_sensor){

    //send request to backent to get first type of data
    var fst_response = $.ajax({
        type: "POST",
        url: "/chart/" + email + "/" + fst_sensor,
        data: "100000",
        async: false,
        dataType: "text"
    }).responseText;
    
    //parse data into two array
    //one for timestamp, one for value
    var fst_dict = JSON.parse(fst_response);
    var fst_time = [];
    var fst_value = [];
    for(var key in fst_dict){
        if(fst_dict.hasOwnProperty(key)){
            fst_value.push(fst_dict[key]);
            fst_time.push(key);
        }
    }

    //send request to backent to get second type of data
    var sec_response = $.ajax({
        type: "POST",
        url: "/chart/" + email + "/" + sec_sensor,
        data: "100000",
        async: false,
        dataType: "text"
    }).responseText;
    
    //parse data into two array
    //one for timestamp, one for value
    var sec_dict = JSON.parse(sec_response); //dict gets overwritten
    var sec_time = [];
    var sec_value = [];
    for(var key in sec_dict){
        if(sec_dict.hasOwnProperty(key)){
            sec_value.push(sec_dict[key]);
            sec_time.push(key);
        }
    }
    

    //deal with CO2 outliers(>10000) by let it
    //equal to the previous one
    for(var i=0; i< fst_value.length; i++){
      fst_value[i] = parseFloat(fst_value[i])
      sec_value[i] = parseFloat(sec_value[i])
      if(fst_value[i] > 10000){
        fst_value[i] = fst_value[i - 1];
      }
      if(sec_value[i] > 10000){
        sec_value[i] = sec_value[i - 1];
      }
    }

  
    var date_all = [];
    var fst_avg = [];
    var sec_avg = [];

    for(var i=0; i < fst_time.length; i++){
      var res = fst_time[i].split("T", 2) //Split timestamp to get just the date
      fst_time[i] = res[0]
    }
    date_all.push(fst_time[fst_time.length-1]); //Theoratically fst_time and sec_time should be exactly the same
    fst_avg.push(fst_value[fst_time.length-1]);
    sec_avg.push(sec_value[fst_time.length-1]);

    var count = 1;  
    for(var i = fst_time.length - 1; i > 0; i--){
      if(fst_time[i] == fst_time[i - 1]){
        fst_avg[0] += fst_value[i - 1]; //If two adjacent value are from same day, add them together
        sec_avg[0] += sec_value[i - 1];
        count += 1;
      }
      else{
        fst_avg[0] = fst_avg[0] / count;//If not, get the average of the added value. 
        sec_avg[0] = sec_avg[0] / count;
        fst_avg.unshift(fst_value[i - 1]);
        sec_avg.unshift(sec_value[i - 1]);
        count = 1;

        date_all.unshift(fst_time[i - 1]);
      }
    }
    fst_avg[0] = fst_avg[0] / count; //take care of edge case
    sec_avg[0] = sec_avg[0] / count;


    var fst_color = "#FFFFFF";
    var sec_color = "#FFFFFF";
    var title = "N/A";
    var fst_label = "N/A";
    var sec_label = "N/A";
    var fst_stringlabel = "N/A";
    var sec_stringlabel = "N/A";

    //set color, title, and labels based on data types
    if (fst_sensor == "CO2" && sec_sensor == "Temperature"){
      fst_color = "#29BF38";
      sec_color = "#F55F5F";
      title = "Co2 - Compared with Temperature";
      fst_label = "Average CO2";
      sec_label = "Average Temperature";
      fst_stringlabel = "CO2";
      sec_stringlabel = "Temperature";
    }
    else if(fst_sensor == "CO2" && sec_sensor == "Humidity"){
      fst_color = "#29BF38";
      sec_color = "#42A1F9";
      title = "Co2 - Compared with Humidity";
      fst_label = "Average CO2";
      sec_label = "Average Humidity";
      fst_stringlabel = "CO2";
      sec_stringlabel = "Humidity";
    }
    else if(fst_sensor == "Temperature" && sec_sensor == "CO2"){
      fst_color = "#F55F5F";
      sec_color = "#29BF38";
      title = "Temperature - Compared with CO2";
      fst_label = "Average Temperature";
      sec_label = "Average CO2";
      fst_stringlabel = "Temperature";
      sec_stringlabel = "CO2";
    }
    else if(fst_sensor == "Temperature" && sec_sensor == "Humidity"){
      fst_color = "#F55F5F";
      sec_color = "#42A1F9";
      title = "Temperature - Compared with Humidity";
      fst_label = "Average Temperature";
      sec_label = "Average Humidity";
      fst_stringlabel = "Temperature";
      sec_stringlabel = "Humidity";
    }
    else if(fst_sensor == "Humidity" && sec_sensor == "Temperature"){
      fst_color = "#42A1F9";
      sec_color = "#F55F5F";
      title = "Humidity - Compared with Temperature";
      fst_label = "Average Humidity";
      sec_label = "Average Temperature";
      fst_stringlabel = "Humidity";
      sec_stringlabel = "Temperature";
    }
    else if(fst_sensor == "Humidity" && sec_sensor == "CO2"){
      fst_color = "#42A1F9";
      sec_color = "#29BF38";
      title = "Humidity - Compared with CO2";
      fst_label = "Average Humidity";
      sec_label = "Average CO2";
      fst_stringlabel = "Humidity";
      sec_stringlabel = "CO2";
    }
    

    //this piece acutually builds the chart
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: date_all,
        datasets: [
        { 
          data: fst_avg,      //first data
          label: fst_label,
          yAxisID: 'fst',
          backgroundColor: fst_color,
          borderColor: fst_color
        },

        {
          data: sec_avg,   //second average data
          label: sec_label,
          backgroundColor: sec_color,
          borderColor: sec_color,
          yAxisID: 'sec'
        },

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
          fontSize: 22
        },
        scales: {
          yAxes: [{
            id: 'fst',
            type: 'linear',
            position: 'left',
            scaleLabel: {
              display: true,
              labelString: fst_stringlabel,
              fontStyle: 'bold',
            },
            ticks: {
              // add unit to data depending on data type
              callback: function(value, index, values) {
                if (fst_sensor == "Humidity"){
                  return value + '%';
                }
                else if (fst_sensor == "Temperature"){
                  return value + '°C';
                }
                else if (fst_sensor == "CO2"){
                  return value;
                }
              }
            },
          }, {
            id: 'sec',
            type: 'linear',
            position: 'right',
            gridLines: {
              display:false
            },
            scaleLabel: {
              display: true,
              labelString: sec_stringlabel,
              fontStyle: 'bold'
            },
            ticks: {
              // add unit to data depending on data type
              callback: function(value, index, values) {
                if (sec_sensor == "Humidity"){
                  return value + '%';
                }
                else if (sec_sensor == "Temperature"){
                  return value + '°C';
                }
                else if (sec_sensor == "CO2"){
                  return value;
                }
              }
            },
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