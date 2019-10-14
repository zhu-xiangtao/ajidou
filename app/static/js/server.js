function run_single_interface(){
    var url = $("input[name='url']").val();
    var method = $("#method").val();

    var request_data = {};
    request_data["url"] = url;
    request_data["method"] = method;
    var params = {};
    for(var i=0;i<$("input[name='params-key']").length;i++){
        var key = $("input[name='params-key']").eq(i).val();
        var value = $("input[name='params-value']").eq(i).val();
        if(key != ""){
            params[key] = value;
        }
    };
    var headers = {};
    for(var i=0;i<$("input[name='headers-key']").length;i++){
        var key = $("input[name='headers-key']").eq(i).val();
        var value = $("input[name='headers-value']").eq(i).val();
        if(key != ""){
            headers[key] = value;
        }
    };
    var data = window.request_data_editor.getValue();
//    post_script_str = window.post_script_editor.getValue();
    if(!jQuery.isEmptyObject(params)){
        request_data["params"] = JSON.stringify(params);
    }
    if(!jQuery.isEmptyObject(headers)){
        request_data["headers"] = JSON.stringify(headers);
    }
    if(data){
        request_data["data"] = data;
    }

    $.ajax({
        url: "http://127.0.0.1:5000/run_single_interface",
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data, status, xhr){
            if(data.status == "success"){
                 $(".response-ok").css("display","block");
                $(".response-error").css("display","none");
                if(!isEmptyObject(data.response_content)){
                    var content_type = data.response_headers["Content-Type"];
                    if(content_type.indexOf("application/json")!=-1){
						console.log(data.response_content);
						console.log(typeof(data.response_content));
                        window.response_body_editor.setValue(JSON.stringify(data.response_content,null,4));
                    }else if(content_type.indexOf("text/html")!=-1){
                        window.response_body_editor.setValue(data.response_content);
                    }
                }else{
                    window.response_body_editor.setValue("no data");
                };
                if(isEmptyObject(data.response_headers)){
                    window.response_headers_editor.setValue("no headers");
                }else{
                    window.response_headers_editor.setValue(JSON.stringify(data.response_headers,null,4));
                };
                if(isEmptyObject(data.cookies)){
                    window.response_cookies_editor.setValue("no cookies");
                }else{
                    window.response_cookies_editor.setValue(JSON.stringify(data.cookies,null,4));
                };
                window.test_results_editor.setValue(
                    "status code: "+ data.code +"\n" +
                    "start time: " + data.start_time + "\n" +
                    "end time: " + data.end_time
                    );
            }else if(data.status == "error"){
                console.log(data);
                $(".response-ok").css("display","none");
                $(".response-error").css("display","block");
                $(".error-editor").text(
                    "Could not get any response" + "\n" +
                    "There was an error connecting to " + request_data["url"] + "\n" +
                    "\n" + "\n" +
                    data.message);
            }
        }
    })
}


function add_test_suite(){
    var request_data = {};
    var suite_name = $("#suite_name").val();
    var suite_creater = $("#suite_creater").val();
    var suite_desc = $("#suite_desc").val();
    var suite_pre_scripts = window.pre_request_editor.getValue();
    var suite_variables = window.variables_editor.getValue();
    var project_id = $("#project").val();
    if(suite_name){
        request_data["suite_name"] = suite_name;
    }else{
        alert("Please editor suite name!");
        return;
    }

    if(suite_creater){
        request_data["suite_creater"] = suite_creater;
    }else{
        alert("Please editor suite creater!");
        return
    }

    if(suite_desc){
        request_data["suite_desc"] = suite_desc;
    }

    if(suite_pre_scripts){
        request_data["suite_pre_scripts"] = suite_pre_scripts;
    }

    if(suite_variables){
        request_data["suite_variables"] = suite_variables;
    }

    if(project_id){
        request_data["project_id"] = project_id;
    }

    $.ajax({
        url: "http://127.0.0.1:5000/add_test_suite",
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
           if(data.status == "success"){
                window.location.href = "http://127.0.0.1:5000/test_suites/" + project_id;
           }
        }
    })
}


function create_project(){
    var request_data = {};
    var project_name = $("#project_name").val();
    var project_creater = $("#project_creater").val();
    var project_desc = $("#project_desc").val();

    if(project_name){
        request_data["project_name"] = project_name;
    }else{
        alert("Please editor project name!");
        return
    }

    if(project_creater){
        request_data["project_creater"] = project_creater;
    }else{
        alert("Please editor project creater!");
        return
    }

    if(project_desc){
        request_data["project_desc"] = project_desc;
    }

    $.ajax({
        url: "http://127.0.0.1:5000/create_project",
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
            if(data.status == "success"){
                window.location.href = "http://127.0.0.1:5000/project_list";
            }
        }
    })


}


function edit_test_case(case_id, suite_id){

    var request_data = {};
    var casename = $("#name").val();
    if(casename){
        request_data["case_name"] = casename;
    }else{
        alert("Please edit case name!");
        return
    }
    var casecreater = $("#creater").val();
    if(casecreater){
        request_data["case_creater"] = casecreater;
    }else{
        alert("Please edit case creater!");
        return
    }
    var casedesc =  $("#description").val();
    request_data["case_desc"] = casedesc;
    var url = $("#url").val();
    if(url){
       request_data["url"] = url;
    }else{
        alert("Please edit request url!");
        return
    }
    var method = $("#method").val();
    if(method){
        request_data["method"] = method;
    }else{
        alert("Please edit request method!");
        return
    }
    var params = {};
    console.log($("input[name='params-key']").length);
    for(var i=0;i<$("input[name='params-key']").length;i++){
        var key = $("input[name='params-key']").eq(i).val();
        var value = $("input[name='params-value']").eq(i).val();
        if(key != ""){
            params[key] = value;
        }
    };
    var headers = {};
    for(var i=0;i<$("input[name='headers-key']").length;i++){
        var key = $("input[name='headers-key']").eq(i).val();
        var value = $("input[name='headers-value']").eq(i).val();
        if(key != ""){
            headers[key] = value;
        }
    };
    var data = window.request_data_editor.getValue();
//    post_script_str = window.post_script_editor.getValue();
    if(!jQuery.isEmptyObject(params)){
        request_data["params"] = JSON.stringify(params);
    }
    if(!jQuery.isEmptyObject(headers)){
        request_data["headers"] = JSON.stringify(headers);
    }
    if(data){
        request_data["data"] = data;
    }
//    request_data["post_script"] = post_script_str;
    console.log(request_data);

    $.ajax({
        url: "http://127.0.0.1:5000/edit_test_case/" + case_id,
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
            if(data.status == "success"){
				console.log(data);
                window.location.href = "http://127.0.0.1:5000/test_cases/" + suite_id;
            }
        }
//        error:function(data,status,xhr){
//            console.log(data);
//            console.log(status);
//            console.log(xhr.status);
//        }
    })
}


function add_test_case(suite_id){

    var request_data = {};
    var casename = $("#name").val();
    if(casename){
        request_data["case_name"] = casename;
    }else{
        alert("Please edit case name!");
        return
    }
    var casecreater = $("#creater").val();
    if(casecreater){
        request_data["case_creater"] = casecreater;
    }else{
        alert("Please edit case creater!");
        return
    }
    var casedesc =  $("#description").val();
    request_data["case_desc"] = casedesc;

    var url = $("#url").val();
    if(url){
       request_data["url"] = url;
    }else{
        alert("Please edit request url!");
        return
    }
    var method = $("#method").val();
    if(method){
        request_data["method"] = method;
    }else{
        alert("Please edit request method!");
        return
    }
    var params = {};
    console.log($("input[name='params-key']").length);
    for(var i=0;i<$("input[name='params-key']").length;i++){
        var key = $("input[name='params-key']").eq(i).val();
        var value = $("input[name='params-value']").eq(i).val();
        if(key != ""){
            params[key] = value;
        }
    };
    var headers = {};
    for(var i=0;i<$("input[name='headers-key']").length;i++){
        var key = $("input[name='headers-key']").eq(i).val();
        var value = $("input[name='headers-value']").eq(i).val();
        if(key != ""){
            headers[key] = value;
        }
    };
    var data = window.request_data_editor.getValue();
//    post_script_str = window.post_script_editor.getValue();
    if(!jQuery.isEmptyObject(params)){
        request_data["params"] = JSON.stringify(params);
    }
    if(!jQuery.isEmptyObject(headers)){
        request_data["headers"] = JSON.stringify(headers);
    }
    if(data){
        request_data["data"] = data;
    }
//    request_data["post_script"] = post_script_str;
    console.log(request_data);

    $.ajax({
        url: "http://127.0.0.1:5000/add_test_case/" + suite_id,
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
            if(data.status == "success"){
				console.log(data);
                window.location.href = "http://127.0.0.1:5000/test_cases/" + suite_id;
            }
        }
//        error:function(data,status,xhr){
//            console.log(data);
//            console.log(status);
//            console.log(xhr.status);
//        }
    })
}


function show_test_case(case_id){
	$.ajax({
		url: "http://127.0.0.1:5000/test_case/" + case_id,
        type: "get",
		success: function(data,status,xhr){
			if(status == "success"){
				window.location.href = "http://127.0.0.1:5000/run_single_interface"
				window.response_headers_editor.setValue(JSON.stringify(data.response.headers,null,4));
				console.log(data.response.headers);
			}
		}
	})
}


function edit_project(project_id){
    var request_data = {};
    var project_name = $("#project_name").val();
    if(project_name){
        request_data["project_name"] = project_name;
    }else{
        alert("Please edit project name!");
        return
    }
    var project_creater = $("#project_creater").val();
    if(project_creater){
        request_data["project_creater"] = project_creater;
    }else{
        alert("Please edit project creater!");
        return
    }
    var project_desc = $("#project_desc").val();
    if(project_desc){
        request_data["project_desc"] = project_desc;
    }

    $.ajax({
        url: "http://127.0.0.1:5000/edit_project/" + project_id,
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
            if(data.status == "success"){
                window.location.href = "http://127.0.0.1:5000/project_list";
            }
        }
    })
}


function add_test_runner(project_id){
    var request_data = {};
    var runner_name = $("#runner_name").val();
    if(runner_name){
        request_data["runner_name"] =  runner_name;
    }else{
        alert("Please edit runner name!");
        return
    }
    var runner_creater = $("#runner_creater").val();
    if(runner_creater){
        request_data["runner_creater"] =  runner_creater;
    }else{
        alert("Please edit runner creater!");
        return
    }
    var runner_desc = $("#runner_desc").val();
    if(runner_desc){
        request_data["runner_desc"] =  runner_desc;
    }
    var suite_id = $("#suite").val();
    if(suite_id){
        request_data["suite_id"] = suite_id;
    }else{
        alert("Please select test suite!");
        return
    }

    $.ajax({
        url: "http://127.0.0.1:5000/add_test_runner/" + project_id,
        type: "post",
        data: request_data,
        dataType: "json",
        success: function(data,status,xhr){
            if(data.status == "success"){
                window.location.href = "http://127.0.0.1:5000/show_test_runner/" + project_id;
            }
        }
    })
}


function isEmptyObject(obj) {
　　for (var key in obj){
　　　　return false;//返回false，不为空对象
　　}　　
　　return true;//返回true，为空对象
}