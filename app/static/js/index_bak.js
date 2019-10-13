var data_editor_is_show = true;
var pre_script_editor_is_show = true;
var post_script_editor_is_show = true;

var response_body_editor_is_show = true;
var response_cookies_editor_is_show = true;
var response_headers_editor_is_show = true;
var test_results_editor_is_show = true;

function show_data_editor(){
    if(data_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".requests-data-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
         window.data_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        data_editor.setOption("value", initValue);
        data_editor.on("keypress", function() {
            data_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
        data_editor.refresh()
    },300);
    data_editor_is_show = false;
    }
}


function show_pre_script_editor(){
    if(pre_script_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".pre-script-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
        window.pre_script_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        pre_script_editor.setOption("value", initValue);
        pre_script_editor.on("keypress", function() {
            pre_script_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
    },300);
    pre_script_editor_is_show = false;
    }
}


function show_post_script_editor(){
    if(post_script_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".post-script-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
        window.post_script_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        post_script_editor.setOption("value", initValue);
        post_script_editor.on("keypress", function() {
            post_script_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
    },300);
    post_script_editor_is_show = false;
    }
}


function show_response_body_editor(){
    if(response_body_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".response-body-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
        window.response_body_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        pre_script_editor.setOption("value", initValue);
        response_body_editor.on("keypress", function() {
            response_body_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
    },1000);
    response_body_editor_is_show = false;
    }
}


function show_response_headers_editor(){
    if(response_headers_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".response-headers-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
        window.response_headers_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        pre_script_editor.setOption("value", initValue);
        response_headers_editor.on("keypress", function() {
            response_headers_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
    },1000);
    response_headers_editor_is_show = false;
    }
}


function show_test_results_editor(){
    if(test_results_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".test-results-editor")[0];
//        var initValue = "# -*-coding:utf-8 -*-";
        window.test_results_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
        });
//        pre_script_editor.setOption("value", initValue);
        test_results_editor.on("keypress", function() {
            test_results_editor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
        });
    },1000);
    test_results_editor_is_show = false;
    }
}


window.onload = function(){
	if(response_body_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".response-body-editor")[0];
        window.response_body_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
			readOnly: "nocursor"
        });
    },10);
    response_body_editor_is_show = false;
    }
}


function show_response_cookies_editor(){
    if(response_cookies_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".response-cookies-editor")[0];
        window.response_cookies_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
			readOnly: "nocursor"
        });
    },300);
    response_cookies_editor_is_show = false;
    }
}


function show_response_headers_editor(){
    if(response_headers_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".response-headers-editor")[0];
        window.response_headers_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
			readOnly: "nocursor"
        });
    },300);
    response_headers_editor_is_show = false;
    }
}


function show_test_results_editor(){
    if(test_results_editor_is_show){
    setTimeout(function(){
        var codeEditor = $(".test-results-editor")[0];
        window.test_results_editor = CodeMirror.fromTextArea(codeEditor, {
            mode: "python",
            theme: "dracula",
            keyMap: "sublime",
            lineNumbers: true,
            smartIndent: true,
            indentUnit: 4,
            indentWithTabs: true,
            lineWrapping: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
            foldGutter: true,
            autofocus: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
			readOnly: "nocursor"
        });
    },300);
    test_results_editor_is_show = false;
    }
}