$(document).ready(function(){
	var array = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1];
	// заполняем селект для весов
	array.forEach(function(item, i, array) {
		$('#Weights').append($('<option>', { 
			value: item,
			text : item.toString()
			}));
	});

	$(function() 
	{
		$('.NewBP').on('click', 'td',function() 
		{
			var param_len = $("#Scheme tr:contains('Параметр') td").length - 1;
			var Col=$(this).index();
			//if (Col == ) 
			if ($(this).index()== param_len || $(this).index() == 0)
			{
				return;
			}
			if ($("#Scheme tr:contains('Параметр') td").eq(Col).css("background-color")==("rgb(255, 255, 255)"))
			{
				$("#Scheme tr:contains('Параметр') td").eq(Col).css("background-color", "red");
				$("#Scheme tr:contains('Тип') td").eq(Col).css("background-color", "red");
				$("#Scheme tr:contains('Описание') td").eq(Col).css("background-color", "yellow");
				$("#Scheme tr:contains('Единицы измерения') td").eq(Col).css("background-color", "yellow");
				$("#Scheme tr:contains('От (Диапазон)*') td").eq(Col).css("background-color", "red");
				$("#Scheme tr:contains('До (Диапазон)*') td").eq(Col).css("background-color", "red");
				$("#Scheme tr:contains('Вес') td").eq(Col).css("background-color", "yellow");
			}
			else
			{
				$("#Scheme tr:contains('Параметр') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('Тип') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('Описание') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('Единицы измерения') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('От (Диапазон)*') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('До (Диапазон)*') td").eq(Col).css("background-color", "white");
				$("#Scheme tr:contains('Вес') td").eq(Col).css("background-color", "white");
			}
		});
	});
});

function AddColumns() //добавить параметры (столбцы), число предварительно указано
{	
	// if ($("#Scheme tr").length==0)
	// {
		// $("#Scheme").append("<tr></tr>");
		// $("#Scheme").append("<tr></tr>");
	// }
	if ($("#ColCount").val() == "")
	{
		$("#mistake_message").html("<strong>Ошибка!</strong> Сначала введите число параметров.");
		$("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
		return;
	}
	$("#mistake_message").attr("hidden", true); // делаем инфу об ошибках невидимой
	$("#Scheme").attr("hidden", false); // делаем таблицу видимой
	$("#hidden_info").attr("hidden", false); // делаем информацию о атрибутах видимой
	for (i=0; i<$("#ColCount").val(); i++)
	{
		// $("#Scheme tr:first").append("<td bgcolor='white'><input name='ColName' size=10></td>");
		// $("#Scheme tr:last").append($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
		AddToEnd();
		// $("#Scheme tr:contains('Параметр')").append("<td bgcolor='white'><input name='ColName' size=10></td>");
		// $("#Scheme tr:contains('Тип')").append($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
		// $("#Scheme tr:contains('От (Диапазон)*')").append("<td bgcolor='white'><input name='RangeFrom' size=10></td>");
		// $("#Scheme tr:contains('До (Диапазон)*')").append("<td bgcolor='white'><input name='RangeTo' size=10></td>");
		// $("#Scheme tr:contains('Описание')").append("<td bgcolor='white'><input name='DescriptionName' size=20></td>");
		// $("#Scheme tr:contains('Единицы измерения')").append($("<td bgcolor='white'></td>").append($("#Units").clone().attr('hidden', false)));
		// $("#Scheme tr:contains('Вес')").append($("<td bgcolor='white'></td>").append($("#Weights").clone().attr('hidden', false)));
	}
	
	$("#Accept").attr("hidden", false);
}
// $(function(){ //через 5сек сообщение закрывается
        // window.setTimeout(function(){
            // $('#mistake_message').attr("hidden", true);
        // },5000);
    // });
function AddToEnd() //добавление нового параметра (столбца)
{	
	// if ($("#Scheme tr").length==0)
	// {
		// $("#Scheme").append("<tr></tr>");
		// $("#Scheme").append("<tr></tr>");
	// }
	//alert('blabla');
	if ($("#Scheme tr:first td").length == 1)
	{
		$("#mistake_message").attr("hidden", true); // делаем инфу об ошибках видимой
		$("#Scheme").attr("hidden", false); // делаем таблицу видимой
		$("#hidden_info").attr("hidden", false); // делаем информацию о атрибутах видимой
		
		$("#Scheme tr:contains('Параметр')").append("<td bgcolor='white'><input name='ColName' size=10></td>");
		$("#Scheme tr:contains('Тип')").append($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
		//Add_Last_param();
		$("#Scheme tr:contains('Параметр') td:last").before("<td bgcolor='white'><input name='ColName' size=10></td>");
		$("#Scheme tr:contains('Тип') td:last").before($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
		$("#Scheme tr:contains('От (Диапазон)*')").append("<td bgcolor='white'><input name='RangeFrom' size=10></td>");
		$("#Scheme tr:contains('До (Диапазон)*')").append("<td bgcolor='white'><input name='RangeTo' size=10></td>");
		$("#Scheme tr:contains('Описание')").append("<td bgcolor='white'><input name='DescriptionName' size=20></td>");
		$("#Scheme tr:contains('Единицы измерения')").append($("<td bgcolor='white'></td>").append($("#Units").clone().attr('hidden', false)));
		$("#Scheme tr:contains('Вес')").append($("<td bgcolor='white'></td>").append($("#Weights").clone().attr('hidden', false)));
	
		$("#Accept").attr("hidden", false);
	}
	else {
		Add_Last_param();
	}
}

function Add_Last_param() //добавить параметр в конец перед ответом
{
	$("#Scheme tr:contains('Параметр') td:last").before("<td bgcolor='white'><input name='ColName' size=10></td>");
	$("#Scheme tr:contains('Тип') td:last").before($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
	
	$("#Scheme tr:contains('От (Диапазон)*')").append("<td bgcolor='white'><input name='RangeFrom' size=10></td>");
	$("#Scheme tr:contains('До (Диапазон)*')").append("<td bgcolor='white'><input name='RangeTo' size=10></td>");
	$("#Scheme tr:contains('Описание')").append("<td bgcolor='white'><input name='DescriptionName' size=20></td>");
	$("#Scheme tr:contains('Единицы измерения')").append($("<td bgcolor='white'></td>").append($("#Units").clone().attr('hidden', false)));
	$("#Scheme tr:contains('Вес')").append($("<td bgcolor='white'></td>").append($("#Weights").clone().attr('hidden', false)));
}
function DelFromEnd()
{
	var param_len = $("#Scheme tr:contains('Параметр') td").length-2;
	if ($("#Scheme tr:first td").length == 1 && $("#Scheme tr:first td").is(':hidden'))
	{
		$("#mistake_message").html("<strong>Ошибка!</strong> Не обнаружено параметров для удаления.");
		$("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
		return;
	}
	if ($("#Scheme tr:first td").length > 2)
	{		
	$("#mistake_message").attr("hidden", true); // делаем инфу об ошибках невидимой
	$("#Scheme tr:contains('Параметр') td").eq(param_len).remove();
	$("#Scheme tr:contains('Тип') td").eq(param_len).remove();
	$("#Scheme tr:contains('Описание') td:last").remove();
	$("#Scheme tr:contains('Единицы измерения') td:last").remove();
	$("#Scheme tr:contains('Вес') td:last").remove();
	$("#Scheme tr:contains('От (Диапазон)*') td:last").remove();
	$("#Scheme tr:contains('До (Диапазон)*') td:last").remove();
	}
	//var collection = $(".a"); collection.eq(collection.length - 2)…
	//alert($("#Scheme tr:contains('Параметр') td").length());

	// $("#Scheme tr:first td:last").remove();
	// $("#Scheme tr:last td:last").remove();
	if ($("#Scheme tr:first td").length == 2)
	{
		$("#Scheme tr:contains('Параметр') td:last").remove();
		$("#Scheme tr:contains('Тип') td:last").remove();
	}
	if ($("#Scheme tr:first td").length == 1)
	{
		$("#Scheme").attr("hidden", true); // делаем таблицу невидимой
		$("#Accept").attr("hidden", true); // делаем кнопку создать бп невидимой 
		$("#hidden_info").attr("hidden", true); // делаем информацию о атрибутах невидимой
	}
	

}

function DelChoice() //удалить из указанного места
{	
flag = 0;
	for (i=$("#Scheme tr:first td").length-1; i>0; i--)
		if ($("#Scheme tr:contains('Параметр') td").eq(i).css("background-color")== "rgb(255, 0, 0)")
		{
			$("#Scheme tr:contains('Параметр') td").eq(i).remove();
			$("#Scheme tr:contains('Тип') td").eq(i).remove();
			$("#Scheme tr:contains('Описание') td").eq(i).remove();
			$("#Scheme tr:contains('Единицы измерения') td").eq(i).remove();
			$("#Scheme tr:contains('От (Диапазон)*') td").eq(i).remove();
			$("#Scheme tr:contains('До (Диапазон)*') td").eq(i).remove();
			$("#Scheme tr:contains('Вес') td").eq(i).remove();
			$("#mistake_message").attr("hidden", true); // делаем инфу об ошибках невидимой
			 flag = 1;
		}
	if (flag == 0)
	{
		$("#mistake_message").html("<strong>Ошибка!</strong> Выберите параметр для удаления.");
		$("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
		return;
	}
	if ($("#Scheme tr:first td").length == 2)
	{
		$("#Scheme tr:contains('Параметр') td:last").remove();
		$("#Scheme tr:contains('Тип') td:last").remove();
	}
	if ($("#Scheme tr:first td").length==1)
	{
		$("#Scheme").attr("hidden", true); // делаем таблицу невидимой
		$("#Accept").attr("hidden", true); // делаем кнопку создать бп невидимой 
		$("#hidden_info").attr("hidden", true); // делаем информацию о атрибутах невидимой
	}
}

function AddChoice() //добавить в выбранное место
{	
	/* ДРУГОЙ ВАРИАНТ
	for (i=$("#Scheme tr:first td").length-1; i>=0; i--)
		if ($("#Scheme tr:first td").eq(i).css("background-color") == "rgb(255, 0, 0)")
		{
			$("#Scheme tr:first td").eq(i).before("<td><input name='ColName' size=10></td>");
			$("#Scheme tr:last td").eq(i).before($("<td></td>").append($("#Types").clone().attr('hidden', false)));
		}
	*/
	flag = 0;	
	$($("#Scheme tr:contains('Параметр') td").get().reverse()).each(function(){ //почему здесь reverse
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
		{
			$("#mistake_message").attr("hidden", true); // делаем невидимой
			$(this).before("<td bgcolor='white'><input name='ColName' size=10></td>");
			flag = 1;
		}
		
		// else
		// {
			// $("#mistake_message").html("<strong>Ошибка!</strong> Сначала выберите место для добавления.");
			// $("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
			// return;
		// }
		});
		if (flag == 0)
		{
			$("#mistake_message").html("<strong>Ошибка!</strong> Выберите место для добавления.");
			$("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
			return;
		}
	$($("#Scheme tr:contains('Тип') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
			$(this).before($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)))});
	$($("#Scheme tr:contains('Вес') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 255, 0)")     
			$(this).before($("<td bgcolor='white'></td>").append($("#Weights").clone().attr('hidden', false)))});	
	$($("#Scheme tr:contains('От (Диапазон)*') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
			$(this).before("<td bgcolor='white'><input name='RangeFrom' size=10></td>");});	
	$($("#Scheme tr:contains('До (Диапазон)*') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
			$(this).before("<td bgcolor='white'><input name='RangeTo' size=10></td>");});		
		
	$($("#Scheme tr:contains('Описание') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 255, 0)")     
			$(this).before("<td bgcolor='white'><input name='DescriptionName' size=20></td>");});	
	$($("#Scheme tr:contains('Единицы измерения') td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 255, 0)") 
			$(this).before($("<td bgcolor='white'></td>").append($("#Units").clone().attr('hidden', false)))});
		
}


function RemoveMark() //снять выделение
{
	$("#Scheme tr:contains('Параметр') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('Тип') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('Описание') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('Единицы измерения') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('От (Диапазон)*') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('До (Диапазон)*') td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:contains('Вес') td").each(function(){$(this).css("background-color", "white");});
}

function ChangeAllTypes(value)
{
	$("select[name='ColType']").each(function(ind, elem){elem[value].selected=true;});
}

function CustomNames(CB)
{	
	if (CB.checked==true)
	{
		var Count=0;
		$("input[name='ColName']").each(function(){$(this).val('Col'+Count++)});
	}
	else
		$("input[name='ColName']").each(function(){$(this).val('')});
}

function SetIdToElems() //добавление id к параметрам
{
	var Count=0;
	// $("input[name='ColName']:not(:first)").each(function(){$(this).attr('name', 'ColName'+Count++)});
	// Count=0;
	// $("select[name='ColType']:not(:first)").each(function(){$(this).attr('name', 'ColType'+Count++)});
	// Count=0;
	// $("input[name='DescriptionName']:not(:first)").each(function(){$(this).attr('name', 'DescriptionName'+Count++)});
	// Count=0;
	// $("select[name='ColUnit']:not(:first)").each(function(){$(this).attr('name', 'ColUnit'+Count++)});
	$("input[name='ColName']").each(function(){$(this).attr('name', 'ColName'+Count++)});
	Count=0;
	$("select[name='ColType']").each(function(){$(this).attr('name', 'ColType'+Count++)});
	Count=0;
	//alert($("input[name='ColName']").attr("name"));
	$("input[name='DescriptionName']").each(function(){$(this).attr('name', 'DescriptionName'+Count++)});
	Count=0;
	$("select[name='ColUnit']").each(function(){$(this).attr('name', 'ColUnit'+Count++)});
	Count=0;
	$("select[name='ColWeights']").each(function(){$(this).attr('name', 'ColWeights'+Count++)});
	Count=0;
	$("input[name='RangeTo']").each(function(){$(this).attr('name', 'RangeTo'+Count++)});
	Count=0;
	$("input[name='RangeFrom']").each(function(){$(this).attr('name', 'RangeFrom'+Count++)});
	//alert($("input[name='RangeFrom']").attr("name"));
	$("#ColCount").val($("#Scheme tr:first td").length - 1);
}
function testfunction()
{
		//if 
	//alert($("#Scheme tr:first td").length - 1);
	alert($("#ColCount").val());
}
function FormValidate(event) //проверка, все ли хорошо
{
	if ($("#BPName").val()=='')
	{
		$("#BPName").css("border-color", "red");
		$('[data-toggle="tooltip"]').tooltip();
		event.preventDefault();
		$("#mistake_message").html("<strong>Ошибка!</strong> Для создания базы прецедентов, заполните все поля, подсвеченные красным.");
		$("#mistake_message").attr("hidden", false); // делаем инфу об ошибках видимой
	}
	else
		$("#BPName").css("border-color", "green");
	
	$("input[name='ColName']").each(function(){
		if ($(this).val()=='')
		{
			$(this).css("border-color", "red");
			event.preventDefault();
		}	
		else
			$(this).css("border-color", "green");});
	$("input[name='RangeTo']").each(function(){
		if ($(this).val()=='')
		{
			$(this).css("border-color", "red");
			event.preventDefault();
		}	
		else
			$(this).css("border-color", "green");});
	$("input[name='RangeFrom']").each(function(){
		if ($(this).val()=='')
		{
			$(this).css("border-color", "red");
			event.preventDefault();
		}	
		else
			$(this).css("border-color", "green");});
	SetIdToElems();
}
	
	
function GetRangesFromFile(filem, max, min)
{
	var reader=new FileReader(); //создание объекта чтения из файла
	tfile=filem.files[0];
	var symb = "";
	var IdInFile=document.getElementById('IdInFile');
	//var textToArray;
	reader.readAsText(tfile);
	reader.onload = function(event)  //прочли файл
	{
		var text = event.target.result; //данные из файла
		if (text.indexOf(",") != -1)
			symb = ",";
		else if (text.indexOf(";") != -1)
			symb = ";";
		else 
		{
			alert("Недопустимый файл");
			return;
		}
		try
		{
		if (IdInFile.checked==true) //если в файле есть айди, то они нам не нужны в диапазонах
		{
			var textToArray = reader.result.split("\n").map(function(x){return x.split(symb)}); // map - простой массив , shift - удаляет эл-т с начала todo shift удаляет посл. элемент а должен первый мб из-за сплита
			//textToArray.shift();
			for (var i = 0; i < textToArray.length; i++){
				textToArray[i].pop();
				textToArray[i].shift();
			}
			}
		else //если нет, то оставляем первый столбец, убираем только ответ
		{
			var textToArray = reader.result.split("\n").map(function(x){return x.split(symb)}); // map - простой массив , shift - удаляет эл-т с начала
			for (var i = 0; i< textToArray.length; i++)
			{
				textToArray[i].pop();
			}
		}
		}
		catch(e) {
			alert('Ошибка при загрузке бп из файла' + e.name + ":" + e.message + "\n" + e.stack); // (3) <--
			return;
		}
	var transpot_matrix = new Array(textToArray[0].length);
	for (var i=0; i < transpot_matrix.length; i++)
	{
		transpot_matrix[i] = new Array(textToArray.length);
	}
	try {
	for (var row = 0; row < textToArray.length; row++){
		for (var col = 0; col < textToArray[row].length; col++){
			transpot_matrix[col][row] = textToArray[row][col];
		}
	}
	}
	catch(e) {
			alert('Ошибка при загрузке бп из файла' + e.name + ":" + e.message + "\n" + e.stack); // (3) <--
			return;
	}

	for (var i = 0; i < transpot_matrix.length; i++){
		max.push(Math.max.apply(null, transpot_matrix[i])); //TODO
		min.push(Math.min.apply(null, transpot_matrix[i]));
	}
	alert(max_array);
	};
}

function CreateSchemeFromFile(filem) //создание схемы по файлу
{
	if ($("#Scheme tr:first td").length > 1)
	{
		for (i=0; i<$("#Scheme tr:first td").length-1; i++)
		{
			DelFromEnd();
		}
	}
	var reader=new FileReader(); //создание объекта чтения из файла
	tfile=filem.files[0];
	var IdInFile = document.getElementById('IdInFile');
	var copydata = document.getElementById('CopyDataToBP');
	var symb = "";
	//var my_index=0;
	reader.onload = function(event)  //прочли файл
	{
		var text = event.target.result; //данные из файла
		var i=0, count=0, data='';		
		while (i<text.length && text[i]!='\n')
		{
			if (text[i]==';' || text[i]==',') 
			{
				if (!(count==0 && IdInFile.checked==true))
				{
					AddToEnd();
					//my_index++;
					var param_len = $("#Scheme tr:contains('Тип') td").length-2;
					if (data % 1 === 0) //если тип - int
						$("#Scheme tr:contains('Тип') td").eq(param_len).find(" :nth-child(1)").attr("selected", "selected");
					else if (!isNaN(data) && data % 1 !== 0 ) //если тип - веществ.
						{
							$("#Scheme tr:contains('Тип') td").eq(param_len).find(" :nth-child(2)").attr("selected", "selected");
						}
					else //если текст.
						$("#Scheme tr:contains('Тип') td").eq(param_len).find(" :nth-child(3)").attr("selected", "selected");
				}
				data='';
				count++;
			}
			else
				data+=text[i];
			
			i++;
		}
		
		if (text.length!=0 && text[i-1]!=';') // для последней строчки
		{
			// AddToEnd();
				
			if (data % 1 === 0) 
				$("#Scheme tr:contains('Тип') td:last :nth-child(1)").attr("selected", "selected");
			else if (!isNaN(data) && data % 1 !== 0 )
				$("#Scheme tr:contains('Тип') td:last :nth-child(2)").attr("selected", "selected");
			else
				$("#Scheme tr:contains('Тип') td:last :nth-child(3)").attr("selected", "selected");
		}
		
		//диапазоны
		if (copydata.checked)
		{
			if (text.indexOf(",") != -1)
			symb = ",";
			else if (text.indexOf(";") != -1)
			symb = ";";
			else 
			{
				alert("Недопустимый файл");
				return;
			}
			try
			{
				if (IdInFile.checked==true) //если в файле есть айди, то они нам не нужны в диапазонах
				{
					var textToArray = reader.result.split("\n").map(function(x){return x.split(symb)}); // map - простой массив , shift - удаляет эл-т с начала todo shift удаляет посл. элемент а должен первый мб из-за сплита
					//textToArray.shift();
					for (var i = 0; i < textToArray.length; i++){
						textToArray[i].pop();
						textToArray[i].shift();
					}
				}
				else //если нет, то оставляем первый столбец, убираем только ответ
				{
					var textToArray = reader.result.split("\n").map(function(x){return x.split(symb)}); // map - простой массив , shift - удаляет эл-т с начала
					for (var i = 0; i< textToArray.length; i++)
					{
						textToArray[i].pop();
					}
				}
			}
			catch(e) {
				alert('Ошибка при загрузке бп из файла' + e.name + ":" + e.message + "\n" + e.stack); // (3) <--
				return;
			}
			var transpot_matrix = new Array(textToArray[0].length);
			for (var i=0; i < transpot_matrix.length; i++)
			{
				transpot_matrix[i] = new Array(textToArray.length);
			}
			try {
				for (var row = 0; row < textToArray.length; row++){
					for (var col = 0; col < textToArray[row].length; col++){
						transpot_matrix[col][row] = textToArray[row][col];
					}
				}
			}
			catch(e) {
				alert('Ошибка при загрузке бп из файла' + e.name + ":" + e.message + "\n" + e.stack); // (3) <--
				return;
			}
			var max_array = []; //максимум
			var min_array = []; //минимум
	
			for (var i = 0; i < transpot_matrix.length; i++){
				max_array.push(Math.max.apply(null, transpot_matrix[i])); //TODO
				min_array.push(Math.min.apply(null, transpot_matrix[i]));
			}
			//alert(max_array);
			var i=0;
			var j=0;
			$("input[name='RangeFrom']").each(function(){$(this).val(min_array[i++])});
			$("input[name='RangeTo']").each(function(){$(this).val(max_array[j++])});
		}	
		
	};
		  
	reader.readAsText(tfile);
	// }
}