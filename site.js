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

function messageContains(message, phrase) {
    return message.indexOf(phrase) > -1;
}

function displayMessages() {
    console.log($textfield.val());

    var displayMessages = []
    for (var i = 0; i < allMessages.length; i++) {
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
