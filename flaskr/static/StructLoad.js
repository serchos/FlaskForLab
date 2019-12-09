var case_='', result_='';
var id = 1;
var switch_res;
$(document).ready(function(){
	$('#res_div').hide();
	// $('#switch_res_json').attr('checked', false);
	$('#switch_res_json').change(function() {
		defaultColors();
		$('#success_message').hide();
		if ($(this).is(":checked"))
		{
			switch_res = true;
			$('#res_div').show();
			$('#select_div').hide();
			$('#json_res_template').focus();
		}
		else {
			$('#res_div').hide();
			switch_res = false;
			$('#select_div').show();
			}
		});
	
	$('#case_button').click(function() {
		defaultColors();
		case_ = $('#json_case_template').val();
		$('#success_message').show();
	});
	$('#result_button').click(function() {
		defaultColors();
		result_ = $('#json_res_template').val();
		$('#success_message').show();
	});
	// $('.del_prec').click(function() {
	// $(this).parent('row').remove();
	// });
	// });
	$('#TabData').on('click','.del_prec', function(){
		defaultColors();
		$(this).closest('tr').remove();
		var rowCount = $('#TabData tr').length;
		if (rowCount == 1) {
			$('#switch_res_json').prop('disabled', false);
			id = 1;
		}
	});
	$('#add_prec').click(function() {
		defaultColors();
		// добавить имена столбцам
		$('#success_message').hide();
		$('#switch_res_json').prop('disabled', true);
		$( "#TabData" ).append("<tr><td><input type='text' class='form-control' value='{0}'/></td><td><input type='text' name='caseName' class='form-control' value='{1}'/></td><td><input type='text' name='resultName' class='form-control' value='{2}' /></td><td><button type='button' class='btn btn-danger del_prec'> <span class='glyphicon glyphicon-trash'></span></button></td></tr>".format(id, case_, result_));
		id++;
	});
});
function BPValidate(event) {
	var case_json='', result_json='';
	if ($('#bp_name').val() == '')
	{
		event.preventDefault();
		$('#bp_name').css("border-color", "red");
	}
	for (var i=1; i < $('#TabData tr').length; i++)
	{
		var case_input = $('#TabData tr:eq({0}) td:eq(1) input'.format(i));
		var result_input = $('#TabData tr:eq({0}) td:eq(2) input'.format(i));
		case_json = case_input.val();
		//case_json = $('#TabData tr:eq({0}) td:eq(1) input'.format(i)).val();
		if (!IsJsonString(case_json))
		{
			$('#alert_message').show();
			case_input.css("border-color", "red");
			event.preventDefault();
			//todo: message об ошибке, выделял красным взять из exphandload
			//добавить валидацию формы
		}
		result_json = result_input.val();
		if (switch_res) {
			if (!IsJsonString(result_json))
			{
				$('#alert_message').show();
				current_input.css("border-color", "red");
				event.preventDefault();
				//todo: message об ошибке
			}
		}
		else {
			var types_val = $("#Types").val();
			if (types_val == 'INT')
			{
				if (isNaN(parseInt(result_json,10)))
				{
					$('#alert_message').show();
					result_input.css("border-color", "red");
					event.preventDefault();
				}
			}
			if (types_val == 'DOUBLE')
			{
				if (isNaN(parseFloat(result_json)))
				{
					$('#alert_message').show();
					result_input.css("border-color", "red");
					event.preventDefault();
				}
			}
			if (result_json == '')
			{
				$('#alert_message').show();
				result_input.css("border-color", "red");
				event.preventDefault();
			}
		}
	}
	SetIdToElems();
	$('#switch_res_json').prop('disabled', false);
	// $('#TabData tr').closest('tr').find("input").each(function() {
        // alert(this.value)
};
function defaultColors() {
	$('#alert_message').hide();
	$('input[type=text]').css("border-color","#ccc");
}
	// IsJsonString()
function IsJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}
function SetIdToElems() //добавление id к параметрам
{
	var Count1=0, Count2=0;
	// $("input[name='ColName']:not(:first)").each(function(){$(this).attr('name', 'ColName'+Count++)});
	$("input[name*='caseName']").each(function(){$(this).attr('name', 'caseName'+Count1++)});
	$("input[name*='resultName']").each(function(){$(this).attr('name', 'resultName'+Count2++)});
	$('#ColCount').val(Count1);
}