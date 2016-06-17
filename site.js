$submit_button = $('#submit')
$result_table = $('#table')
$textfield = $('#search-box')

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

$textfield.bind("enterKey",function(e){
    displayMessages();
});

$textfield.keyup(function(e){
    if(e.keyCode == 13) {
       $(this).trigger("enterKey");
    }
});

$('#startDatePicker').datepicker({
    autoclose: true,
    format: 'mm/dd/yyyy'
});

$('#endDatePicker').datepicker({
    autoclose: true,
    format: 'mm/dd/yyyy'
});

function messageContains(message, phrase) {
    return message.indexOf(phrase) > -1;
}

function displayMessages() {
    console.log($textfield.val());

    var startTime = new Date($('#startDatePicker').datepicker('getFormattedDate')).getTime();
    var endTime = new Date($('#endDatePicker').datepicker('getFormattedDate')).getTime();
    console.log(startTime + " " + endTime);

    var displayMessages = []
    for (var i = 0; i < allMessages.length; i++) {
        message = allMessages[i]; 
        
        if (message.timestamp < startTime) {
            continue;
        }

        if (message.timestamp > endTime) {
            break;
        }
        
        if (messageContains(allMessages[i].text, $textfield.val())) {
            displayMessages.push(allMessages[i]);
        }
    }
    console.log(displayMessages);

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
    	data: displayMessages
    });

    $result_table.bootstrapTable("load", displayMessages)
}
