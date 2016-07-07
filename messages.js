$submit_button = $('#submit')
$result_table = $('#table')
$textfield = $('#search-box')
$start_date_picker = $('#startDatePicker')
$end_date_picker = $('#endDatePicker')

allMessages = null

function setMessages(messages) {
    allMessages = messages
}

// Load JSON from file
$.getJSON("messages.json", function(json) {	
    setMessages(json);
});

// Submit button onclick
$(function () {
    $submit_button.click(function () {
        displayMessages();
    });
});

// Bind enter key on textfield to perform search
$textfield.bind("enterKey", function(e) {
    displayMessages();
});

$textfield.keyup(function(e) {
    if (e.keyCode == 13) {
       $(this).trigger("enterKey");
    }
});

// Settings for datepickers
$start_date_picker.datepicker({
    autoclose: true,
    format: 'mm/dd/yyyy'
});

$end_date_picker.datepicker({
    autoclose: true,
    format: 'mm/dd/yyyy'
});

// Initalize table
$result_table.bootstrapTable({
    columns: [{
        field: 'date',
        title: 'Date'
    }, {
        field: 'name',
        title: 'Sender'
    }, {
        field: 'text',
        title: 'Message'
    }],
    data: []
});


// Determines if a phrase exists in the given message
function messageContains(message, phrase) {
    return message.toLowerCase().indexOf(phrase) > -1;
}

// Iterates through messages list and updates the table accordingly
function displayMessages() {
    var startTime = new Date($start_date_picker.datepicker('getFormattedDate')).getTime();
    var endTime = new Date($end_date_picker.datepicker('getFormattedDate')).getTime();

    var displayMessages = []
    for (var i = 0; i < allMessages.length; i++) {
        message = allMessages[i]; 
        
        if (message.timestamp < startTime) {
            continue;
        }

        if (message.timestamp > endTime) {
            break;
        }

        if (messageContains(message.text, $textfield.val())) {
            displayMessages.push(message);
        }
    }


    $result_table.bootstrapTable("load", displayMessages)
}
