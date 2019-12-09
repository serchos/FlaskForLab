$(function(){
	$("#TableChoice").on('change', function(){
		LookBPRequest($(this).val());
	});
});

function LookBPRequest(TabCh)
{	
	$.ajax({
		type: "GET",
		async: false, 
		url: "/LookBPRequest",
		data: {TableChoice: TabCh, Id:-1},
		success: function(data){
			var json=JSON.parse(data);
			LoadBP(TabCh, 0, 0, json['TotalCount'], 150);
			$(".progress-div").hide();
		}
	});
}

function LoadBP(TabCh, CurId, CurCount, TotalCount, CountStr)
{
	$.ajax({
		type: "GET",
		url: "/LookBPRequest",
		data: {TableChoice: TabCh, Id:CurId, CountStr: CountStr},
		success: function(data){
			var json=JSON.parse(data);
			Handler(json, CurCount+json['TabData'].length, TotalCount);
			if (CurCount+json['TabData'].length<TotalCount)
				LoadBP(TabCh, CurId+CountStr, CurCount+json['TabData'].length, TotalCount, CountStr);
			else
				$(".progress-div").hide();
		}
	});
}

function Handler(json, CurCount, TotalCount)
{
	if (json['Id']==0)
	{
		$("#TabData tbody").replaceWith("<tbody></tbody>");
		$("#DescrTabData tbody").replaceWith("<tbody></tbody>").append("<tr></tr>");
	
		var fragment1 = document.createDocumentFragment(),
			fragment2 = document.createDocumentFragment(),
			fragment3 = document.createDocumentFragment();

		var tr=document.createElement("tr");
		for (var i=0; i<json['TabInfo'].length; i++)
			$("<th/>", {text: json['TabInfo'][i][0]}).appendTo(tr);
		
		fragment1.appendChild(tr);
		
		tr=document.createElement("tr");
		
		for (var i=0; i<json['DescrTabInfo'].length; i++)
			$("<th/>", {text: json['DescrTabInfo'][i][0]}).appendTo(tr);
		
		fragment2.appendChild(tr);
		
		var td;
		for (var i=0; i<json['DescrTabData'].length; i++)
		{
			tr=document.createElement("tr");
			
			for (var j=0; j<json['DescrTabData'][i].length; j++)
			{
				td=tr.insertCell(j);
				td.innerHTML=json['DescrTabData'][i][j];
			}
			
			fragment3.appendChild(tr);
		}
      
		$("#TabData").append(fragment1);
		$("#DescrTabData").append(fragment2);
		$("#DescrTabData").append(fragment3);
		
		$("#TabDataDiv").show();
		$(".progress-div").show();
	}

	var fragment1 = document.createDocumentFragment(),
		tr, td;
	
	for (var i=0; i<json['TabData'].length; i++)
	{
		tr=document.createElement("tr");
			
		for (var j=0; j<json['TabData'][i].length; j++)
		{
			td=tr.insertCell(j);
			td.innerHTML=json['TabData'][i][j];
		}
			
		fragment1.appendChild(tr);
	}
		
	$("#TabData").append(fragment1);
	var progressValue=Math.floor(CurCount/TotalCount*100);
	
	$("#ProgressBar").val(progressValue);
	$(".progress-text").html("Загрузка {0} %".format(progressValue));
}