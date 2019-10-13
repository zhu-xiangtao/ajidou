function addRow(obj){
    var row = $(obj).parents("div.row").eq(0);
	temp = '<div class="row" style="background-color:#e9ecef;border-radius:0.75rem;margin:15px 5px;">' + row.html() + '</div>'
	row.after(temp);
}

function deleteRow(id, obj){
    var row = $(obj).parents("div.row").eq(0);
	if(id == "requests-params"){
		if($("#requests-params>div").length>1){
			row.remove();
		}
	}else if(id == "requests-headers"){
		if($("#requests-headers>div").length>1){
			row.remove();
		}
	}
}

function clearRow(obj){
	var row = $(obj).parents("div.row").eq(0);
	row.find("input[class='form-control key']").val("");
	row.find("input[class='form-control value']").val("");
}




