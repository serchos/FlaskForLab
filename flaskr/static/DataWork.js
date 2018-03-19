var buf='';
var ValId, ValCol, Str=0, Count=0;

$(document).ready(function(){

$(".color_table tr:not(#first_tr)").addClass("colors");

$(".colors:last").css("background-color", "#90ee90");
var tr_clr=$(".colors:last").css("background-color");
$(".colors:last").css("background-color", "white");

$(function()
{
	var CurCol;
	
	$('.color_table').on('mouseenter', 'tr', function()
	{
		if (this.className!="first_tr")
		{	
			CurCol=$(this).css("background-color");
			$(this).css("background-color", "yellow");
		}
	});

	$('.color_table').on('mouseleave', 'tr', function()
	{	
		if (this.className!="first_tr")
			$(this).css("background-color", CurCol);
	});
	
	$('.color_table').on('click', 'tr', function() 
	{	
		if(this.className!="first_tr" && CurCol!="rgb(255, 0, 0)")
			$(this).css("background-color", "red");
		else if (this.className!="first_tr")
			$(this).css("background-color", "");
		
		CurCol=$(this).css("background-color");
	});

    $('.color_table').on('dblclick', 'td', function(e) 
	{
		var t = e.target || e.srcElement;
		var elm_name = t.tagName.toLowerCase();
		if(elm_name != 'td')
			return false;
		
		window.Str= $(this).parent('tr').index();
		window.ValCol=$(this).index();
		window.ValId=$("#ColorTable tr:eq({0}) td:first".format(window.Str)).html();
		var val=$(this).html();

		window.buf=val;
		$(this).empty().append('<input type="text" id="edit" value="{0}"/>'.format(val));
		$('#edit').focus();
		$('#edit').blur(function()	
		{
			$(this).parent().empty().html(window.buf);		
		});
	});
});


$(window).keydown(function(event)
{
	if(event.keyCode == 13 && document.getElementById('edit')==document.activeElement) 
	{
		var ValData=$('#edit').val();
		RememberChanges(ValData, window.ValId, window.ValCol);
		window.buf=ValData;
		$('#edit').blur();
	}
});
});

/*
function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}*/

function RememberChanges(ValData, ValId, ValCol)
{		
	$("#DataField").append("<option selected value={0}>{0}</option>".format(ValData));
	$("#IdField").append("<option selected value={0}>{0}</option>".format(ValId));
	$("#ColumnField").append("<option selected value={0}>{0}</option>".format(ValCol));
}

function AddStr()
{
	var Id=$("#ColorTable tr:last td:first").html();
	if (isNumeric(Id)==true)
		Id++;
	else 
		Id=1;
	
	$("#AddStrField").append("<option selected value={0}>{0}</option>".format(Id));
	$("#ColorTable").append("<tr></tr>");
	$("#ColorTable tr:last").append("<td>{0}</td>".format(Id));
	
	for (i=1; i<$("#ColorTable tr:first td").length; i++)
		$("#ColorTable tr:last").append("<td></td>");
	

	return Id;
}

function AddColumn()
{	
	$("#myform").append("<p>Введите имя нового столбца</p>");
	$("#myform").append("<p><input name='NewColName' id='NewColName'/></p>");
	$("#myform").append("<p>Введите тип данных нового столбца</p>");
	$("#myform").append("<p><select id=NewColType name=NewColType></select></p>");
	$("#NewColType").append("<option selected value={0}>{0}</option>".format('Целый'));
	$("#NewColType").append("<option value={0}>{0}</option>".format('Вещественный'));
	$("#NewColType").append("<option value={0}>{0}</option>".format('Текстовый'));
	$("#NewColType").append("<option value={0}>{0}</option>".format('Другой'));
	$("#myform").append("<p><input type='submit' name='DataEdit' value='{0}' onclick='ValidateColName(event)'/></p>".format('Записать столбец'));
}

function ValidateColName(event)
{
	if ($("#NewColName").val()=='')
	{
		$("#NewColName").css("border-color", "red");
		event.preventDefault();
	}	
}

function DelStr()
{
	for (i=$("#ColorTable tr").length-1; i>=1; i--)
		if ($("#ColorTable tr:eq({0})".format(i)).css("background-color")=="rgb(255, 0, 0)")
		{
			var Id=$("#ColorTable tr:eq({0}) td:eq({1})".format(i, 0)).html();
			$("#DelStrField").append("<option selected value={0}>{0}</option>".format(Id));
			$("#ColorTable tr:eq({0})".format(i)).remove();
		}
}

/*
function AddColumn2()
{
	var Table=document.getElementById("ColorTable");
	var inpt=document.createElement("input");
	var sel=document.createElement("select");
	var cell=document.createElement("td");
	
	inpt.name="AddColName"+window.Count;
	sel.name="AddColType"+window.Count++;
	sel.options[0] = new Option("INTEGER", "INTEGER", true, true);
	sel.options[1] = new Option("REAL", "REAL");
	sel.options[2] = new Option("TEXT", "TEXT");
	sel.options[3] = new Option("HZ", "HZ");
	cell.width=140;	
	cell.appendChild(inpt);
	cell.appendChild(sel);
	Table.rows[0].appendChild(cell);
	
	for (i=1; i<Table.rows.length; i++)
	{
		var cell=document.createElement("td");
		cell.width=140;
		Table.rows[i].appendChild(cell);
	}
}*/

function AddColumn2()
{	
	$("#ColorTable tr:first").height(50);
	$("#ColorTable tr:first").append("<p><input name='AddColName{0}'/></p>".format(window.Count));
	$("#ColorTable tr:first").append("<p><select id=AddColType{0} name=AddColType{0}></select></p>".format(window.Count));
	$("#AddColType{0}".format(window.Count)).append("<option selected value={0}>{0}</option>".format('Целый'));
	$("#AddColType{0}".format(window.Count)).append("<option value={0}>{0}</option>".format('Вещественный'));
	$("#AddColType{0}".format(window.Count)).append("<option value={0}>{0}</option>".format('Текстовый'));
	$("#AddColType{0}".format(window.Count)).append("<option value={0}>{0}</option>".format('Другой'));
	
	window.Count++;
	
	for (i=1; i<$("#ColorTable tr").length; i++)
		$("#ColorTable tr:eq({0})".format(i)).append("<td></td>");
}

function ValidateAddCol()
{
	$("#AddColCount").val(window.Count);
}

function AddDataFromFile(filem)
{
	var reader=new FileReader();
	tfile=filem.files[0];
	
	reader.onload = function(event) 
	{
		var text = event.target.result, data='';
		var CurRow=$("#ColorTable tr").length, CurCol=1, NewId;
		
		if (text.length!=0) NewId=AddStr();
	
		for (var i=0; i<text.length; i++)
		{
			switch(text[i])
			{
				case ';':
				case ',':
					$("#ColorTable tr:eq({0}) td:eq({1})".format(CurRow, CurCol)).html(data);
					RememberChanges(data, NewId, CurCol);
					CurCol++;
					data='';
					break;
				case '\n':
					$("#ColorTable tr:eq({0}) td:eq({1})".format(CurRow, CurCol)).html(data);
					RememberChanges(data, NewId, CurCol);
					CurRow++;
					CurCol=1;
					data='';
					if (i+1<text.length) NewId=AddStr();
					break;
				default:
					data+=text[i];
			}
		}
		
		$("#ColorTable tr:eq({0}) td:eq({1})".format(CurRow, CurCol)).html(data);
		RememberChanges(data, NewId, CurCol);
	};
		  
	reader.readAsText(tfile);
}