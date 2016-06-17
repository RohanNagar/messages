$submit_button = $('#submit')
$result_table = $('#table')
$textfield = $('#search-box')

// Submit button onclick
$(function () {
        $submit_button.click(function () {
            readJSON();
        });
    });

function readJSON() {
	$.getJSON("test.json", function(json) {
		displayMessages(json);
	});
}

function displayMessages(messages) {
	console.log(messages);
	console.log($textfield.val());
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
    		data: messages});
}
