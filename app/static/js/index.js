
window.onload = function(){
    var codeEditor1 = $(".requests-data-editor")[0];
    window.request_data_editor = show_request_editor(codeEditor1);

    var codeEditor2 = $(".pre-script-editor")[0];
    window.pre_script_editor = show_request_editor(codeEditor2);

    var codeEditor3 = $(".post-script-editor")[0];
    window.post_script_editor = show_request_editor(codeEditor3);

    var codeEditor4 = $(".response-body-editor")[0];
    window.response_body_editor = show_response_editor(codeEditor4);

    var codeEditor5 = $(".response-cookies-editor")[0];
    window.response_cookies_editor = show_response_editor(codeEditor5);

    var codeEditor6 = $(".response-headers-editor")[0];
    window.response_headers_editor = show_response_editor(codeEditor6);

    var codeEditor7 = $(".test-results-editor")[0];
    window.test_results_editor = show_response_editor(codeEditor7);
}


function show_request_editor(editor){
    var codeEditor = CodeMirror.fromTextArea(editor, {
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

    codeEditor.on("keypress", function(){
        codeEditor.showHint(); // 注意，注释了CodeMirror库中show-hint.js第131行的代码（阻止了代码补全，同时提供智能提示）
    });
    return codeEditor;
}


function show_response_editor(editor){
    var codeEditor = CodeMirror.fromTextArea(editor, {
        mode: "python",
        theme: "dracula",
        keyMap: "sublime",  //使用sublime中的快捷键
        lineNumbers: true,
        smartIndent: true,
        indentUnit: 4,
        indentWithTabs: true,
        lineWrapping: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
        foldGutter: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        styleActiveLine: true,
	    readOnly: "nocursor"
    });
    codeEditor.setSize("auto","450px");
    return codeEditor;
}


function refresh_request_data_editor(){
    setTimeout(function(){
        window.request_data_editor.refresh();
    },300);
}


function refresh_pre_script_editor(){
    setTimeout(function(){
        window.pre_script_editor.refresh();
    },300);
}


function refresh_post_script_editor(){
    setTimeout(function(){
        window.post_script_editor.refresh();
    },300);
}


function refresh_response_body_editor(){
    setTimeout(function(){
        window.response_body_editor.refresh();
    },300);
}


function refresh_response_cookies_editor(){
    setTimeout(function(){
        window.response_cookies_editor.refresh();
    },300);
}


function refresh_response_headers_editor(){
    setTimeout(function(){
        window.response_headers_editor.refresh();
    },300);
}


function refresh_test_results_editor(){
    setTimeout(function(){
        window.test_results_editor.refresh();
    },300);
}


