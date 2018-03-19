$(document).ready(function(){

	$(function() 
	{
		$('.NewBP').on('click', 'td',function() 
		{
			var Col=$(this).index();
			
			if ($("#Scheme tr:first td").eq(Col).css("background-color")==("rgb(255, 255, 255)"))
			{
				$("#Scheme tr:first td").eq(Col).css("background-color", "red");
				$("#Scheme tr:last td").eq(Col).css("background-color", "red");
			}
			else
			{
				$("#Scheme tr:first td").eq(Col).css("background-color", "white");
				$("#Scheme tr:last td").eq(Col).css("background-color", "white");
			}
		});
	});
});

function AddColumns()
{	
	if ($("#Scheme tr").length==0)
	{
		$("#Scheme").append("<tr></tr>");
		$("#Scheme").append("<tr></tr>");
	}
	
	for (i=0; i<$("#ColCount").val(); i++)
	{
		$("#Scheme tr:first").append("<td bgcolor='white'><input name='ColName' size=10></td>");
		$("#Scheme tr:last").append($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
	}
	
	$("#Accept").attr("hidden", false);
}

function AddToEnd()
{	
	if ($("#Scheme tr").length==0)
	{
		$("#Scheme").append("<tr></tr>");
		$("#Scheme").append("<tr></tr>");
	}
	
	$("#Scheme tr:first").append("<td bgcolor='white'><input name='ColName' size=10></td>");
	$("#Scheme tr:last").append($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));
	
	$("#Accept").attr("hidden", false);
}


function DelFromEnd()
{
	
	$("#Scheme tr:first td:last").remove();
	$("#Scheme tr:last td:last").remove();
	
	if ($("#Scheme tr:first td").length==0)
		$("#Accept").attr("hidden", true);

}

function DelChoice()
{	
	for (i=$("#Scheme tr:first td").length-1; i>=0; i--)
		if ($("#Scheme tr:first td").eq(i).css("background-color")== "rgb(255, 0, 0)")
		{
			$("#Scheme tr:first td").eq(i).remove();
			$("#Scheme tr:last td").eq(i).remove();
		}
		
	if ($("#Scheme tr:first td").length==0)
		$("#Accept").attr("hidden", true);
}

function AddChoice()
{	
	/* ДРУГОЙ ВАРИАНТ
	for (i=$("#Scheme tr:first td").length-1; i>=0; i--)
		if ($("#Scheme tr:first td").eq(i).css("background-color") == "rgb(255, 0, 0)")
		{
			$("#Scheme tr:first td").eq(i).before("<td><input name='ColName' size=10></td>");
			$("#Scheme tr:last td").eq(i).before($("<td></td>").append($("#Types").clone().attr('hidden', false)));
		}
	*/
		
	$($("#Scheme tr:first td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
			$(this).before("<td bgcolor='white'><input name='ColName' size=10></td>");});
		
	$($("#Scheme tr:last td").get().reverse()).each(function(){
		if ($(this).css("background-color") == "rgb(255, 0, 0)")     
			$(this).before($("<td bgcolor='white'></td>").append($("#Types").clone().attr('hidden', false)));});	
}

function RemoveMark()
{
	$("#Scheme tr:first td").each(function(){$(this).css("background-color", "white");});
	$("#Scheme tr:last td").each(function(){$(this).css("background-color", "white");});
}

function ChangeAllTypes(value)
{
	$("Select").each(function(ind, elem){elem[value].selected=true;});
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

function SetIdToElems()
{
	var Count=0;
	$("input[name='ColName']").each(function(){$(this).attr('name', 'ColName'+Count++)});
	Count=0;
	$("select[name='ColType']").each(function(){$(this).attr('name', 'ColType'+Count++)});
	$("#ColCount").val($("#Scheme tr:first td").length);
}

function FormValidate(event)
{
	if ($("#BPName").val()=='')
	{
		$("#BPName").css("border-color", "red");
		event.preventDefault();
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

	SetIdToElems();
}

function CreateSchemeFromFile(filem)
{
	var reader=new FileReader();
	tfile=filem.files[0];
	var IdInFile=document.getElementById('IdInFile');
	
	reader.onload = function(event) 
	{
		var text = event.target.result;
		var i=0, count=0, data='';
	
		while (i<text.length && text[i]!='\n')
		{
			if (text[i]==';' || text[i]==',') 
			{
				if (!(count==0 && IdInFile.checked==true))
				{
					AddToEnd();
				
					if (data % 1 === 0) 
						$("#Scheme tr:last td:last :nth-child(1)").attr("selected", "selected");
					else if (!isNaN(data) && data % 1 !== 0 )
						$("#Scheme tr:last td:last :nth-child(2)").attr("selected", "selected");
					else
						$("#Scheme tr:last td:last :nth-child(3)").attr("selected", "selected");
				}
				data='';
				count++;
			}
			else
				data+=text[i];
			
			i++;
		}
		
		if (text.length!=0 && text[i-1]!=';')
		{
			AddToEnd();
				
			if (data % 1 === 0) 
				$("#Scheme tr:last td:last :nth-child(1)").attr("selected", "selected");
			else if (!isNaN(data) && data % 1 !== 0 )
				$("#Scheme tr:last td:last :nth-child(2)").attr("selected", "selected");
			else
				$("#Scheme tr:last td:last :nth-child(3)").attr("selected", "selected");
		}
	};
		  
	reader.readAsText(tfile);
}