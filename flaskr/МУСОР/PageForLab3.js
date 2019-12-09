var TimerId;

$(document).ready(function()
{

	document.getElementById("StartTest").addEventListener("click", StartTestHandler);
	document.getElementById("EndTest").addEventListener("click", EndTestHandler2);
});

function StartTestHandler() 
{
	$("#Hour").html("2");
	$("#Minute").html("10");
	$("#Second").html("15");
	
	$(".Timer").attr("hidden", false);
	$("#Questions").attr("hidden", false);
	$("#StartTest").attr("hidden", true);
	$("#EndTest").attr("hidden", false);
	$("#Results").empty();
		
	alert("Тест начался!");
	Timer();
}

function EndTestHandler()
{
	var count=$("#Questions div").length;
	var ColRight=0, ColNotAnswer=0, ColNotRight=0;
		
	for (i=1; i<=count; i++)
	{
		var CheckAnswers=$('input[name=Question{0}]:checked'.format(i));
		
		if (CheckAnswers.length==0)
			ColNotAnswer++;
		else
		{
			var Right=true;
			for (j=0; j<CheckAnswers.length && Right==true; j++)
				if (CheckAnswers.eq(j).val()=='false')
					Right=false;
			
			if (Right==true)
				ColRight++;
			else
				ColNotRight++;
		}
	}
		
	clearTimeout(window.TimerId);
		
	$(".Timer").attr("hidden", true);
	$("#Questions").attr("hidden", true);
	$("#EndTest").attr("hidden", true);
		
	$("#StartTest").attr("hidden", false);
	$("#Results").append("<p>Правильных ответов: {0}</p>".format(ColRight));
	$("#Results").append("<p>Неправильных ответов: {0}</p>".format(ColNotRight));
	$("#Results").append("<p>Ответов не дано: {0}</p>".format(ColNotAnswer));
	
	for (i=1; i<=count; i++)
		$('input[name=Question{0}]:checked'.format(i)).each(function(){ $(this).removeAttr("checked"); });
}


function EndTestHandler2()
{
	var count=$("#Questions div").length;
	var ColRight=0, ColNotAnswer=0, ColNotRight=0;
		
	for (i=1; i<=count; i++)
	{
		var CheckAnswers=$('input[name=Question{0}]:checked'.format(i));
		var CorrAnswers=$('input[name=Question{0}][value=true]'.format(i));
		
		if (CheckAnswers.length==0)
			ColNotAnswer++;
		else
		{
			var Right=true;
			for (j=0; j<CheckAnswers.length && Right==true; j++)
				if (CheckAnswers.eq(j).val()=='false')
					Right=false;
			
			if (Right==true && CorrAnswers.length==CheckAnswers.length)
				ColRight++;
			else
				ColNotRight++;
		}
	}
		
	clearTimeout(window.TimerId);
		
	$(".Timer").attr("hidden", true);
	$("#Questions").attr("hidden", true);
	$("#EndTest").attr("hidden", true);
		
	$("#StartTest").attr("hidden", false);
	$("#Results").append("<p>Правильных ответов: {0}</p>".format(ColRight));
	$("#Results").append("<p>Неправильных ответов: {0}</p>".format(ColNotRight));
	$("#Results").append("<p>Ответов не дано: {0}</p>".format(ColNotAnswer));
	
	for (i=1; i<=count; i++)
		$('input[name=Question{0}]:checked'.format(i)).each(function(){ $(this).removeAttr("checked"); });
}





function Timer()
{
	var Hour=$("#Hour").html();
	var Minute=$("#Minute").html();
	var Second=$("#Second").html();
	var EndTime=false;
	
	if (Second>0)
		Second--;
	else
	{
		if (Minute>0)
		{
			Second=59;
			Minute--;
		}
		else
		{
			if (Hour>0)
			{
				Minute=59;
				Hour--;
			}
			else
				EndTime=true;
		}
	}
	
	if (EndTime==true)
	{
		alert("Время истекло!");
		EndTestHandler();
	}
	else
	{
		$("#Hour").html(Hour);
		$("#Minute").html(Minute);
		$("#Second").html(Second);
		window.TimerId=setTimeout(Timer, 1000);
	}
}
