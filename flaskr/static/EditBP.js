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

function Algorithms(AlgorithmValue)
{
	switch(AlgorithmValue)
	{
		case 'Classification':
			$("#DivKMeans").attr("hidden", true);
			$("#DivClassification").attr("hidden", false);
			break;
		case 'KMeans':
			$("#DivKMeans").attr("hidden", false);
			$("#DivClassification").attr("hidden", true);
			break;
		case 'TimurAlgorithm':
			$("#DivKMeans").attr("hidden", true);
			$("#DivClassification").attr("hidden", true);
			break;
	}
}


/*-----Новый код-----*/

var DelArr={}, DelTdArr={}, TabCh;

// ----- Код WorkWithStrings -----

function HighlightStr()
{
	var TrCollection=$("#TabData tr"),
		HFrom=$("#HighlightFrom").val(), HTo=$("#HighlightTo").val(),	
		TrNumFrom=GetId(TrCollection, HFrom), TrNumTo=GetId(TrCollection, HTo),
		Color="red";
	
	if ($("[name=Highlight]:checked").val()=='off')
		Color="";

	if (HFrom!=+TrCollection.eq(TrNumFrom).find("td").eq(0).html())
	{
		alert("Введите существующий id начала диапазона!");
		return;
	}

	if (HTo!=+TrCollection.eq(TrNumTo).find("td").eq(0).html())
	{
		alert("Введите существующий id конца диапазона!");
		return;
	}
	
	var fragment=document.createDocumentFragment();
	
	for (i=TrNumFrom; i<=TrNumTo; i++)
		TrCollection.eq(i).clone().css("background-color", Color).appendTo(fragment);
	
	for (i=TrNumFrom; i<=TrNumTo; i++)
		TrCollection.eq(i).remove();
	
	TrCollection.eq(TrNumFrom-1).after(fragment);
	
	//$("#TabData").append(fragment);
	//alert("TrNumFrom: {0}   TrNumTo: {1}".format(TrNumFrom, TrNumTo));
}

function RandomHighlightStr()
{
	var TrCollection=$("#TabData tr"),
		HFrom=$("#RandomHighlightFrom").val(), HTo=$("#RandomHighlightTo").val(),
		TrNumFrom=GetId(TrCollection, HFrom), TrNumTo=GetId(TrCollection, HTo),
		HCount=$("#RandomHighlightCount").val(),
		Color="red", Id;
		
	if (HFrom!=+TrCollection.eq(TrNumFrom).find("td").eq(0).html())
	{
		alert("Введите существующий id начала диапазона!");
		return;
	}

	if (HTo!=+TrCollection.eq(TrNumTo).find("td").eq(0).html())
	{
		alert("Введите существующий id конца диапазона!");
		return;
	}
	
	if (HTo-HFrom+1<=HCount)
	{
		var fragment=document.createDocumentFragment();
	
		for (i=TrNumFrom; i<=TrNumTo; i++)
			TrCollection.eq(i).clone().css("background-color", Color).appendTo(fragment);
	
		for (i=TrNumFrom; i<=TrNumTo; i++)
			TrCollection.eq(i).remove();
	
		TrCollection.eq(TrNumFrom-1).after(fragment);
	}
	else
	{
		for (i=0; i<HCount; i++)
		{
			for (j=0; j<1;)
			{
				Id = TrNumFrom + Math.random() * (TrNumTo + 1 - TrNumFrom);
				Id = Math.floor(Id);
				if (TrCollection.eq(Id).css("background-color")!="rgb(255, 0, 0)")
				{
					TrCollection.eq(Id).css("background-color", "red");
					j++;
				}
			}
		}
	}
}

function InsertStr()
{
	var CountStr=$("#InsertStrCount").val();

	$.ajax({
		type: "POST", 
		url: "/EditBPRequest",
		data: {TableChoice: TabCh, Operation: "Insert", Count: CountStr},
		success: function(data){
			var json=JSON.parse(data), fragment=document.createDocumentFragment(), tr;

			for (i=0; i<json['LastInsertRowId'].length; i++)
			{
				tr=document.createElement("tr");
				$("<td/>", {text: json['LastInsertRowId'][i]}).appendTo(tr)

				for (j=1; j<$("#TabData tr:first th").length; j++)
					tr.insertCell(j);
				
				fragment.appendChild(tr);
			}
			
			$("#TabData").append(fragment);
		}
	});
}

function DeleteStr()
{
	//var TabCh=$("#TableChoice option:selected").text();
	
		$.ajax({
			type: "POST", 
			url: "/EditBPRequest",
			data: {TableChoice: TabCh, Operation: "Delete", JsonObj: JSON.stringify(DelArr)},
			success: function(data){
				for (var i in DelTdArr)
					DelTdArr[i].remove();
				alert('Success Delete');
			}
		});
}

function DeleteAllStr()
{
	$.ajax({
		type: "POST", 
		url: "/EditBPRequest",
		data: {TableChoice: TabCh, Operation: "DeleteAll"},
		success: function(data){
			var th=$("#TabData tbody tr:first");
			$("#TabData tbody").replaceWith("<tbody></tbody>");
			$("#TabData").append(th);
			alert('Success DeleteAll');
		}
	});
}

// -------------------------

// ----- Код WorkWithColumns -----

function InsertColumn()
{
	//var AddColDiv=$("<div><p>Название столбца<input type='text' id='ColumName'></p><input type='button' ><></div>");
	var Div=$("<div>");
	Div.append($("<p>", {text: "Название столбца"}));
	Div.append($("<input>", {type: 'button', text: 'Cоздать столбец'}));
	alert('OK');
}

// -------------------------

// ----- Код WorkWithData -----

function AddDataFromFile()
{
	var tfile=$("#ImportBPFile").prop('files')[0], FD= new FormData();
	FD.append("ImportBPFile", tfile);
	FD.append("TableChoice", TabCh);
	FD.append("Operation", "Load From File");
	$.ajax({
			type: "POST", 
			url: "/EditBPRequest",
			data: FD,
			cache: false,
			dataType: 'json',
			processData: false,
			contentType: false,
			success: function(data){
				LoadBP(TabCh, data['LastId'], data['TCBI'], data['TCAI'], 150);
				alert('Success Load From File');
			}
		});
}

function ExportTestSampleToFile()
{
	var TestSample=$("#TabData tr"), Id="";

	for (i=1; i<TestSample.length; i++)
		if (TestSample.eq(i).css("background-color")=="rgb(255, 0, 0)")
			Id+=TestSample.eq(i).find("td").eq(0).html()+",";

	$("[name=HiddenTableChoice]").val(TabCh);		
	$("[name=HiddenTestSample]").val(Id.slice(0, Id.length-1));
}

// -------------------------

// ----- Код WorkWithTable -----

function DeleteBP()
{ 
	var BPChoice={}, SelectedTables=$("#TabSelect a[class='list-group-item active']");
	
	$(SelectedTables).each(function(i){
		BPChoice[i]=$(this).html();
	});

	$.ajax({
		type: "POST",
		async: false, //Подумай над синхронностью... 
		url: "/DeleteBP",
		data: {BPChoice: JSON.stringify(BPChoice)},
		success: function(){
			$(SelectedTables).each(function(i){
				if ($(this).html()==TabCh)
				{
					$("#TabData tbody").replaceWith("<tbody></tbody>").append("<tr></tr>");
					$("#DescrTabData tbody").replaceWith("<tbody></tbody>").append("<tr></tr>");
					$("#TableChoiceTab a span").html("Выберите базу");
				}
				$(this).remove();
			});
		}
	});
}

function RenameBP()
{
	var NewBPNames={}, RenamedTables=$("#TabSelect a");
	
	$(RenamedTables).each(function(i){
		NewBPNames[i]=$(this).html();
	});
	
	$.ajax({
		type: "POST",
		url: "/RenameBP",
		data: {NewBPNames: JSON.stringify(NewBPNames)},
		success: function(){
			alert("Переименовывание таблиц успешно завершено!");
		}
	});	
}

// -------------------------

// ----- Код ImproveEfficiency -----

function Optimization()
{
	var OptAlgol=$("#OptAlgol option:selected").val(),
		OptArr={"OptAlgol": OptAlgol};

	switch(OptAlgol)
	{
		case 'Classification':
			OptArr['ClassSimilarity']=$("#ClassSimilarity").val();
			OptArr['ClassMetric']=$("#ClassMetric option:selected").val();
			break;
		case 'KMeans':
			OptArr['KMClusterCount']=$("#KMClusterCount").val();
			OptArr['KMPrimaryCenter']=$("#KMPrimaryCenter option:selected").val();
			OptArr['KMMetric']=$("#KMMetric option:selected").val();
			break;
		case 'TimurAlgorithm':
			break;
	}
	
	$.ajax({
		type: "POST", 
		url: "/OptimizationBP",
		data: {TableChoice: TabCh, JsonObj: JSON.stringify(OptArr)},
		success: function(data){
			alert('Success Optimization!');
		}
	});
}

function ShowOptAlgolOptions()
{
	var OptAlgol=$("#OptAlgol option:selected").val();

	switch(OptAlgol)
	{
		case 'Classification':
			$("#DivKMeans").hide();
			$("#DivClassification").show();
			break;
		case 'KMeans':
			$("#DivClassification").hide();
			$("#DivKMeans").show();
			break;
		case 'TimurAlgorithm':
			$("#DivClassification").hide();
			$("#DivKMeans").hide();
			break;
	}
}

// -------------------------


function EditBPRequest()
{
	//TabCh=$("#TableChoice option:selected").text();
	LookBPRequest();
}



/*
function InsertStr(Count)
{
	//var TabCh=$("#TableChoice option:selected").text(),
	var tr=document.createElement("tr"),
	td=tr.insertCell(0);

	
	
	
	for (var i=1; i<$("#TabData tr:first th").length; i++)
		tr.insertCell(i);
	
	$("#TabData").append(tr);
	
	$.ajax({
		type: "POST", 
		url: "/EditBPRequest",
		data: {TableChoice: TabCh, Operation: "Insert"},
		success: function(data){
			var json=JSON.parse(data);
			td.innerHTML=json['LastInsertRowId'];
		}
	});
}*/


/*
function UpdateStr()
{
	//var TabCh=$("#TableChoice option:selected").text();
	
	if (jsonObj)
	{
		$.ajax({
			type: "POST", 
			url: "/EditBPRequest",
			data: {TableChoice: TabCh, Operation: "Update", JsonObj: JSON.stringify(UpdArr)},
			success: function(data){
				alert('Success Update');
			}
		});
	}
}*/

//Наведения курсора на таблицы
$(function()
{
	// ----- Наведение и клики по таблице прецедентов -----
	var CurCol;
	
	$('#TabData').on('mouseenter', 'tr', function()
	{
		if (this.className!="first_tr")
		{	
			CurCol=$(this).css("background-color");
			$(this).css("background-color", "yellow");
		}
	});

	$('#TabData').on('mouseleave', 'tr', function()
	{	
		if (this.className!="first_tr")
			$(this).css("background-color", CurCol);
	});
	
	$('#TabData').on('click', 'tr', function() 
	{	
		if(this.className!="first_tr" && $(this).css("background-color")!="rgb(255, 0, 0)")
		{
			$(this).css("background-color", "red");
			DelArr[$(this).find('td')[0].innerHTML]=$(this).find('td')[0].innerHTML;
			DelTdArr[$(this).find('td')[0].innerHTML]=$(this);
			//alert(DelTdArr[$(this).find('td')[0].innerHTML]);
		}
		else if (this.className!="first_tr")
		{
			$(this).css("background-color", "");
			delete DelArr[$(this).find('td')[0].innerHTML];
			delete DelTdArr[$(this).find('td')[0].innerHTML];
		}
		
		CurCol=$(this).css("background-color");
	});
	// --------------------------
	
	// ----- Двойные клики по таблице прецедентов -----
	
	$("#TabData").on('dblclick', 'td', function(){
		if ($(this).find('input').length==0)
		{
			var Val=$(this).html();
			
			$('<input>', {
				'id': 'EditTd',
				'type': 'text',
				'class': 'form-control',
				'value': Val,
				'css': {
					'color': 'black',
					'text-align': 'center',
					'height': '100%',
				},
			}).appendTo($(this).empty()).focus();			
			
			$("#EditTd").on('blur', function()
			{
				$("#EditTd").parent().empty().html(Val);
			});
			
			$("#EditTd").on('keydown', function(e){
				if (e.keyCode==13)
				{
					var Val=$("#EditTd").val(), 
						ColName=$("#TabData tr:first").find("th").eq($(this).parent().index()).html(),
						Id=$("#EditTd").parent().parent().find('td')[0].innerHTML,
						UpdArr={"Id":Id, "ColName":ColName, "Value": Val};
						
					$.ajax({
						type: "POST", 
						url: "/EditBPRequest",
						data: {TableChoice: TabCh, Operation: "Update", JsonObj: JSON.stringify(UpdArr)},
						success: function(data){
							alert('Success Update');
							$("#EditTd").parent().empty().html(Val);
						}
					});
				}
			});
		}
	});
	
	$("#TabData").on('dblclick', 'th', function(){
		if ($(this).find('input').length==0)
		{
			var Val=$(this).html();
			
			$('<input>', {
				'id': 'EditTh',
				'type': 'text',
				'class': 'form-control',
				'value': Val,
				'css': {
					'color': 'black',
					'text-align': 'center',
					'height': '100%',
				},
			}).appendTo($(this).empty()).focus();			
			
			$("#EditTh").on('blur', function()
			{
				$("#EditTh").parent().empty().html(Val);
			});
			
			$("#EditTh").on('keydown', function(e){
				if (e.keyCode==13)
				{
					var Val=$("#EditTh").val(), 
						ColName=$("#TabData tr:first").find("th").eq($("#EditTh").parent().index()).html(),
						UpdArr={"ColName":ColName, "Value": Val};
						
					$.ajax({
						type: "POST", 
						url: "/EditBPRequest",
						data: {TableChoice: TabCh, Operation: "RenameColumn", JsonObj: JSON.stringify(UpdArr)},
						success: function(data){
							alert('Success Rename Column');
							$("#EditTh").parent().empty().html(Val);
						}
					});
				}
			});
		}
	});
	// --------------------------
	
	// ------- Клики по списку с именами БП -------
	$("#TabSelect").on('click', 'a', function(){
		if ($(this).find('input').length==0)
		{
			if ($(this).attr("class")=="list-group-item")
				$(this).attr("class", "list-group-item active");
			else
				$(this).attr("class", "list-group-item");
		}
	});
	
	$("#TabSelect").on('dblclick', 'a', function(){
		if ($(this).find('input').length==0)
		{
			var Val=$(this).html();
			
			$('<input>', {
				'id': 'NewBPName',
				'type': 'text',
				'class': 'form-control',
				'value': Val,
				'css': {
					'color': 'black',
					'text-align': 'center',
					'height': '100%',
				},
			}).appendTo($(this).empty()).focus();
			
			$("#NewBPName").on('blur', function(){
				$("#NewBPName").parent().empty().html(Val);
			});
			
			$("#NewBPName").on('keydown', function(e){
				if (e.keyCode==13)
				{
					var Val=$("#NewBPName").val();
					$("#NewBPName").parent().empty().html(Val);
				}
			});
		}
	});
	// ----------------------------
});

//Обработчики кнопок
$(function(){
	$('#InsertManyStr').on('click', InsertStr);
	
	$('#ExportBPToFile').on('click', function(){
		$("[name=HiddenTableChoice]").val(TabCh);
	});
	
	$('#ExportTestSampleToFile').on('click', ExportTestSampleToFile);
	
	$('#ExportTrainSampleToFile').on('click', ExportTestSampleToFile);
	
	$("#TableChoiceTab ul li").on('click', 'a', function()
	{
		TabCh=$(this).html();
		$("#TableChoiceTab a span").html(TabCh);
		LookBPRequest(TabCh);
	});
	
	$('.btn-file input[type=file]',).on('change', function (){
		var FileName=$(this).val();
		//alert($(this).parent());
		$('.btn-file .btn-file-name').html(FileName);
	});
	
	$("#RenameBP").on('click', RenameBP);
	
	$("#DeleteBP").on('click', DeleteBP);
	
	$("#HighlightStr").on('click', HighlightStr);
	
	$("#RandomHighlightStr").on('click', RandomHighlightStr);

	$("#OptAlgol").on('change', ShowOptAlgolOptions);

	$("#DeleteStr").on('click', DeleteStr);

	$("#DeleteAllStr").on('click', DeleteAllStr);

	$("#InsertColumn").on('click', InsertColumn);

	$("#AddDataFromFile").on('click', AddDataFromFile);
});


function GetId(TrCollection, Id)
{
	var TrId=+TrCollection.eq(Id).find("td").eq(0).html(), 
		TrNumId=TrId;

	if(TrId!=Id)
	{	 
		if (TrId>Id && TrId-Id<=Id)
		{
			for (TrNumId=TrId; TrNumId>=0 && TrId!=Id; TrNumId--)
				TrId=+TrCollection.eq(TrNumId).find("td").eq(0).html();
			
			TrNumId++;
		}
		else if (TrId>Id && TrId-Id>Id)
		{
			for (TrNumId=0; TrNumId<TrCollection.length && TrId!=Id; TrNumId++)
				TrId=+TrCollection.eq(TrNumId).find("td").eq(0).html();
			
			TrNumId--;
		}
		else if (TrId<Id && Id-TrId<=$("#TabData tr").length-Id)		 
		{
			for (TrNumId=TrId; TrNumId<TrCollection.length && TrId!=Id; TrNumId++)
				TrId=+TrCollection.eq(TrNumId).find("td").eq(0).html();
			
			TrNumId--;
		}
		else if (TrId<Id && Id-TrId>$("#TabData tr").length-Id)
		{
			for (TrNumId=TrCollection.length-1; TrNumId>=0 && TrId!=Id; TrNumId--)
				TrId=+TrCollection.eq(TrNumId).find("td").eq(0).html();
			
			TrNumId++;
		}
		else
		{
			for (TrNumId=0; TrNumId<TrCollection.length && TrId!=Id; TrNumId++)
				TrId=+TrCollection.eq(TrNumId).find("td").eq(0).html();
			
			TrNumId--;
		}
	}
	
	return TrNumId;
}
