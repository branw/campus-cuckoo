$(document).ready(function() {
    // Load the most recent database
    $.getScript("/js/data.js", function() {
        // Populate locations
        $('#location').empty();
        if (navigator.geolocation) {
            $('#location').append($("<option />").val('NEARBY').html('&#8982; Nearby'));
        }

        for (var i = 0; i < DISPLAY_BUILDINGS.length; i++) {
            var building_name = BUILDING_NAMES[BUILDINGS.indexOf(DISPLAY_BUILDINGS[i])];
            $('#location').append($("<option />").val(DISPLAY_BUILDINGS[i]).text(building_name));
        }

        // Add handlers
        $('form').change(function() { update(); });

        // Create a slider for time selection
        var current_time = Math.ceil(((new Date()).getMinutes() + (new Date()).getHours() * 60) / 5) * 5;
        current_time = Math.max(Math.min(current_time, 23*60), 7*60);
        var time_slider = document.getElementById('time');

        noUiSlider.create(time_slider, {
            range: {
                min: 7 * 60,
                max: 23 * 60
            },
            connect: true,
            step: 5,
            start: [ current_time, current_time + 60 ],
            tooltips: [ formatter, formatter ]
        });

        $('#time-start').timepicker({
            template: false,
            showInputs: false,
            minuteStep: 5,
        }).on('changeTime.timepicker', function(e) {
            var time = e.time.minutes + e.time.hours*60;
            if (e.time.meridian == 'PM' && e.time.hours < 12) {
                time += 12*60;
            }
            time_slider.noUiSlider.set([time, null]);
        });
        $('#time-end').timepicker({
            template: false,
            showInputs: false,
            minuteStep: 5
        }).on('changeTime.timepicker', function(e) {
            var time = e.time.minutes + e.time.hours*60;
            if (e.time.meridian == 'PM' && e.time.hours < 12) {
                time += 12*60;
            }
            time_slider.noUiSlider.set([null, time]);
        });

        // Update slider hints
        var update_slider = function(values) {
            $('#time-start').timepicker('setTime', formatter.to(values[0]));
            $('#time-end').timepicker('setTime', formatter.to(values[1]));
            update();
        };
        time_slider.noUiSlider.on('change', update_slider);
        update_slider(time_slider.noUiSlider.get());

        // Put message in results
        $('#results').empty();
        $('<li class="list-group-item list-group-item-info">Acquiring location...</li>').appendTo('#results');

        // Create the first selection
        update();

        // Move past the loading screen
        $("#main").fadeIn();
        $("#loader").fadeOut();
    });
});

var haversine = function(lat1,lon1,lat2,lon2) {
  var R = 6371;
  var dLat = deg2rad(lat2-lat1);
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c;
  return d; // km
};

var deg2rad = function(deg) {
  return deg * (Math.PI/180)
};

var formatter = {
  to: function(value) {
    var date = new Date(1970, 0, 1, Math.floor(value/60), value % 60);
    return date.toLocaleTimeString();
  },
  from: function(value) { }
};

var update = function(acquired_building = false) {
    var building = acquired_building || $('#location').val();
    // Attempt geolocation
    if (!acquired_building && building == 'NEARBY') {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude  = position.coords.latitude;
            var longitude = position.coords.longitude;

            var best_dist = 9999999;
            var best_i = 0;

            for (var i = 0; i < BUILDINGS.length; i++) {
                var building_latitude = LATITUDES[i], building_longitude = LONGITUDES[i];
                if (building_latitude == 0 || building_longitude == 0) {
                    continue;
                }

                var dist = haversine(latitude, longitude, building_latitude, building_longitude);
                if (dist < best_dist) {
                    best_dist = dist;
                    best_i = i;
                }
            }

            console.log('closest is', BUILDINGS[best_i]);

            update(BUILDINGS[best_i]);
        }, function() {
            $('#results').empty();
            $('<li class="list-group-item list-group-item-danger">Unable to acquire location! Try selecting a building.</li>').appendTo('#results');
        });
        return;
    }
    else if (acquired_building && $('#location').val() != 'NEARBY') {
        return;
    }

    var times = document.getElementById('time').noUiSlider.get();
    var day = $('input[name=day]:checked').val();

    var has_whiteboard = $("#has-whiteboard").is(':checked');
    var has_chalkboard = $("#has-chalkboard").is(':checked');

    var index = BUILDINGS.indexOf(building);
    var building_name = BUILDING_NAMES[index];

    // Start with all of the rooms in the building
    var available = ROOMS[index].slice();

    // Discard rooms that don't meet the attributes
    for (var i = available.length - 1; i >= 0; i--) {
        var room = available[i];
        var attribs = ROOM_ATTRIBS[index][ROOMS[index].indexOf(room)];

        if (has_whiteboard && attribs.indexOf('FX14') == -1) {
            available.splice(i, 1);
        }
        if (has_chalkboard && attribs.indexOf('FX13') == -1) {
            available.splice(i, 1);
        }
    }

    // Discard rooms that are occupied for classes
    for (var i = 0; i < CLASSES[index].length; i++) {
        var c = CLASSES[index][i];

        // Overlapping time
        if (day == c[2] && !(times[1] < c[0] || times[0] > c[1])) {
            var available_index = available.indexOf(c[3]);
            if (available.indexOf(c[3]) != -1) {
                available.splice(available_index, 1);
            }
        }
    }

    var current = new Date();
    var weekstart = current.getDate() - current.getDay();    
    var weekend = weekstart + 6;
    var current_day = new Date(current.setDate(weekstart + DAYS.indexOf(day)));
    current_day.setHours(0, 0, 0, 0);

    // Discard rooms that are occupied for events
    for (var i = 0; i < EVENTS[index].length; i++) {
        var e = EVENTS[index][i];

        var start_date = new Date(e[2] * 1000);
        start_date.setHours(0, 0, 0, 0);
        var end_date = new Date(e[3] * 1000);
        end_date.setHours(0, 0, 0, 0);

        // Overlapping time
        if (day == e[4] && !(times[1] < e[0] || times[0] > e[1]) && 
            (start_date.getTime() <= current_day.getTime() && 
                end_date.getTime() >= current_day.getTime())) {
            var available_index = available.indexOf(e[5]);
            if (available.indexOf(e[5]) != -1) {
                available.splice(available_index, 1);
            }
        }
    }

    $('#results').empty();
    $('<li class="list-group-item list-group-item-light">' + available.length + ' room(s) available in ' + building_name + '</li>').appendTo('#results');

    for (var i = 0; i < available.length; i++) {
        var room = available[i];
        var room_index = ROOMS[index].indexOf(room);
        var short_name = BUILDINGS[index] + ' ' + room;
        var full_name = BUILDING_NAMES[index] + ' ' + room;
        var capacity = ROOM_CAPACITIES[index][room_index];
        var attribs = ROOM_ATTRIBS[index][room_index];

        var type = '';
        if (attribs.indexOf('TY25') != -1) {
            type = 'Computer Lab';
        }
        else if (attribs.indexOf('TY26') != -1) {
            type = 'Auditorium';
        }
        else if (attribs.indexOf('TY28') != -1 || attribs.indexOf('TY32') != -1) {
            type = 'Classroom';
        }
        else if (attribs.indexOf('TY33') != -1) {
            type = 'Tiered Classroom';
        }

        var badges = '';
        if (attribs.indexOf('FX13') != -1) {
            badges += '<span class="badge badge-pill badge-dark">Chalkboard</span> ';
        }
        if (attribs.indexOf('FX14') != -1) {
            badges += '<span class="badge badge-pill badge-light">Whiteboard</span> ';
        }
        if (attribs.indexOf('PC19') != -1) {
            badges += '<span class="badge badge-pill badge-info">A/C</span> ';
        }

        var ga_classroom = attribs.indexOf('PC30') != -1;

        $('<div class="list-group-item flex-column align-items-start">' + 
            '<div class="d-flex flex-wrap w-100 justify-content-between mb-2">' +
              '<div>' + 
                '<h5 class="mb-0">' + full_name + (ga_classroom ? ' &#9733;' : '') + '</h5>' +
                '<small class="text-muted">' + short_name + (type != '' ? ' (' + type + ')': '') + '</small> ' +
                '<span class="badge badge-secondary">Fits ' + capacity + '</span>' +
              '</div>' +
              '<div>' + badges + '</div>' +
            '</div>' + 
          '</div>').appendTo('#results');
    }
};
