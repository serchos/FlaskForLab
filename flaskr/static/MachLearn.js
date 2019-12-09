
$(document).ready(function(){


$(".DataTableCl tr:not(#first_tr)").addClass("colors");

$(".colors:last").css("background-color", "#90ee90");
var tr_clr=$(".colors:last").css("background-color");
$(".colors:last").css("background-color", "white");




$('input[type=radio][name=SwitchTSCO]').change(function() 
{	
	if (this.value == 'CDT') 
	{
		$("#AddPrecButton").attr("hidden", false);
		$("#ClassDataTable").attr("hidden", false);
    }
    else  
	{
		$("#AddPrecButton").attr("hidden", true);
		$("#ClassDataTable").attr("hidden", true);
    }
});


$(function()
{
	var CurCol;
	
	$('.DataTableCl').on('mouseenter', 'tr', function()
	{
		if (this.className!="first_tr")
		{	
			CurCol=$(this).css("background-color");
			$(this).css("background-color", "yellow");
		}
	});

	$('.DataTableCl').on('mouseleave', 'tr', function()
	{	
		if (this.className!="first_tr")
			$(this).css("background-color", CurCol);
	});
	
	$('.DataTableCl').on('click', 'tr', function() 
	{	
		if(this.className!="first_tr" && CurCol!="rgb(255, 0, 0)")
			$(this).css("background-color", "red");
		else if (this.className!="first_tr")
			$(this).css("background-color", "");
		
		CurCol=$(this).css("background-color");
	});
});	

});

/*
String.prototype.format = function(){
  var args = arguments
  return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, i) {
    if (m == "{{") return "{"
    if (m == "}}") return "}"
    return args[i]
  })
}*/

function RememberId(e, FormName, TableName)
{	
	if ($("#TabList").val()=='Выберите базу прецедентов')
	{
		alert("Сначала выберите базу");
		e.returnValue=false;
	}
	
	if ($("#SwitchTSCO3").prop("checked"))
		CreateSelectForRows2(e, "MLForm", "ClassDataTable");
	else
	{
		$("#{0}".format(FormName)).append("<input name='RowsNumber' hidden size=10 value='0'>");
		$("#{0}".format(FormName)).append("<input name='ColNumber' hidden size=10 value='0'>");
	}
	
	SaveIdTSCO(e, FormName, TableName);
	
	//e.returnValue=false;
	//IdRange();
	return false;
}

function CreateSelectForRows2(e, FormName, TableName)
{	
	var RowsNumber=$("#{0} tr".format(TableName)).length-1;
	var ColNumber=$("#{0} tr:first td".format(TableName)).length;
	
	$("#{0}".format(FormName)).append("<input name='RowsNumber' hidden size=10 value={0}>".format(RowsNumber));
	$("#{0}".format(FormName)).append("<input name='ColNumber' hidden size=10 value={0}>".format(ColNumber));
	
	for (i=0; i<ColNumber; i++)
	{		
		$("#{0}".format(FormName)).append("<select id={0} name={0} hidden multiple></select>".format("SelForCol"+i, "SelForCol"+i));

		for (j=1; j<=RowsNumber; j++)
		{
			var Text=$("#{0} tr:eq({1}) td:eq({2})".format(TableName, j, i)).html();
			$("#{0}".format("SelForCol"+i)).append("<option selected value={0}>{1}</option>".format(Text, Text));
		}
	}
}

function IdRange()
{	
	for (i=$("#RangeFrom").val(); i<=$("#RangeTo").val(); i++)
		if ($("#DataTable tr:eq({0})".format(i)).css("background-color")=="rgb(255, 0, 0)")
			$("#DataTable tr:eq({0})".format(i)).css("background-color", "white");
		else
			$("#DataTable tr:eq({0})".format(i)).css("background-color", "red");
}

function SaveIdTSCO(e, FormName, TableName)
{
	if ( $("#SwitchTSCO1").prop("checked") ||  $("#SwitchTSCO3").prop("checked"))
		var Field1="TSField", Field2="COField";
	else
		var Field1="COField", Field2="TSField";
		
	for (i=1; i<$("#DataTable tr").length; i++)
	{
		if ($("#DataTable tr:eq({0})".format(i)).css("background-color")=="rgb(255, 0, 0)")
			$("#{0}".format(Field1)).append("<option selected value={0}>{0}</option>".format($("#DataTable tr:eq({0}) td:first".format(i)).html()));
		else
			$("#{0}".format(Field2)).append("<option selected value={0}>{0}</option>".format($("#DataTable tr:eq({0}) td:first".format(i)).html()));
	}
}

function SaveDeleteRep()
{	
	for (i=1; i<$("#RepDataTable tr").length; i++)
		if ($("#RepDataTable tr:eq({0})".format(i)).css("background-color")=="rgb(255, 0, 0)")
			$("#RepSelect").append("<option selected value={0}>{0}</option>".format($("#RepDataTable tr:eq({0}) td:first".format(i)).html()));	
}

function CrossValidationFun(AlgorithmValue)
{
	switch(AlgorithmValue)
	{
		case 'KFoldCV':
			$("#DivKFoldCV").attr("hidden", false);
			$("#DivHoldOutCV").attr("hidden", true);
			break;
		case 'HoldOutCV':
			$("#DivKFoldCV").attr("hidden", true);
			$("#DivHoldOutCV").attr("hidden", false);
			break;
		case 'LOOCV':
			$("#DivKFoldCV").attr("hidden", true);
			$("#DivHoldOutCV").attr("hidden", true);
			break;
	}
}


