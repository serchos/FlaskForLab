var handler1 = function(Col, Direct, DirectMas){MoveBanner(Col, Direct, DirectMas);};

window.onload=function(){alert("Денёк добрейший!");};
$(document).ready(function(){Clock();});
window.addEventListener("DOMContentLoaded", Calendar, false);
window.addEventListener("DOMContentLoaded", handler1.bind(this, 0, 1, [1, 0]), false);


var Answers=[]; 
			 
var DistFun ={
				0:	[function(Direct){ $("#Banner").css(Direct, parseInt($("#Banner").css(Direct), 10)-10); },
					 function(Direct){ $("#Banner").css(Direct, parseInt($("#Banner").css(Direct), 10)+10); }]
			 };
		
		
function MoveBanner(Col, Direct, DirectMas)
{
	var PosL=parseInt($("#Banner").css("left"), 10), PosT=parseInt($("#Banner").css("top"), 10);
	var DirectMasStr=["left", "top"]

	if (Col==10)
	{
		var rand= 0 - 0.5 + Math.random() * (1 - 0 + 1);
		Direct = Math.round(rand);
		Col=0;
	}
	else
		Col++;
	
	if (PosL<=20 || $(document).width()-PosL-$("#Banner").width()<=20)
		DirectMas[0]=Number(!DirectMas[0]);
	else
	if (PosT<=20 || $(document).height()-PosT-$("#Banner").height()<=20)
		DirectMas[1]=Number(!DirectMas[1]);

	
	window.DistFun[0][DirectMas[Direct]](DirectMasStr[Direct]);
	setTimeout(MoveBanner, 30, Col, Direct, DirectMas);
}

function LoadQuestions(elem)
{
	var file=elem.files[0];
	var reader=new FileReader();
	reader.onload=function(e)
	{
		var text=e.target.result;
		var arr=text.split('\n');
		
		for (i=0; i<arr.length/2; i++)
		{
			$("#Questions").append("<p>{0}</p>".format(arr[i*2]));
			$("#Questions").append("<p><input class=answer></p>");
			window.Answers[i]=arr[i*2+1];
		}
		
	$("#Questions").append("<p><input type=button value='Проверить' onclick='CheckAnswers()'/></p>");
	}
	reader.readAsText(file);
	$("#{0}".format("LoadQuestions")).hide();
}

function CheckAnswers()
{
	var correct=true;

	for (i=0; i<$(".answer").length && correct==true; i++)
	{
		var ans1=$(".answer").eq(i).val(), ans2=window.Answers[i];

		ans1 = ans1.replace(/\r|\n|\s/g, '').toLowerCase();
		ans2 = ans2.replace(/\r|\n|\s/g, '').toLowerCase();
		
		if (ans1.localeCompare(ans2)!=0)
			correct=false;
	}

	CreateWindow(correct)
}

function CreateWindow(correct)
{
	var Win = window.open("about:blank", 'Результат', 'height=400,width=400');

	Win.document.write('<html><head><title>Результат</title></head>');
	Win.document.write('<body>');

	if (correct==true)
		Win.document.write('<div>Все верно!</div>');
	else
		Win.document.write('<div>У Вас ошибки!</div>');


	Win.document.write('<p><a href="javascript:self.close()">Закрыть</a></p>');
	Win.document.write('</body></html>');
	Win.document.close();
}

function Calendar()
{
    var date = new Date();
    var y = date.getFullYear(), m = date.getMonth(), d = date.getDate();
    var date1 = new Date(y, m + 1, 0);
    var LastDay = date1.getDate();
    var RowNum = 1;

    for (i = 1; i <= 6; i++)
        for (j = 1; j <= 7; j++)
            $("#Calendar tr:eq({0})".format(i)).append("<td></td>");

    for (i = 1; i <= LastDay; i++)
    {
        var cur = new Date(y, m, i);
        var dw = cur.getDay();

        if (dw == 0) {
            $("#Calendar tr:eq({0}) td:eq(6)".format(RowNum)).html(i);
            if (d == i) $("#Calendar tr:eq({0}) td:eq(6)".format(RowNum)).css("background-color", "red");
        }
        else {
            $("#Calendar tr:eq({0}) td:eq({1})".format(RowNum, dw - 1)).html(i);
            if (d == i) $("#Calendar tr:eq({0}) td:eq({1})".format(RowNum, dw-1)).css("background-color", "red");
        }

        if (cur.getDay() == 0) RowNum = RowNum + 1;
    }
}

function Clock()
{
    var date = new Date();
    var h = date.getHours(), m = date.getMinutes(), s = date.getSeconds();
    if (h < 10) h = "0" + h;
    if (m < 10) m = "0" + m;
    if (s < 10) s = "0" + s;
	$("#Hour").html(h);
	$("#Minute").html(m);
	$("#Second").html(s);
    setTimeout("Clock()", 1000);
}