
function changeaction(v) {
    if (v == 0) {
        document.main.action = "translate";
    }
    else if (v == 1) {
        document.main.action = "listening";
    }
    else if (v == 2) {
        document.main.action = "play1";
    }
    else {
        document.main.action = "play2";
    }

    main.submit();
}

  
  
function fun_word(elem){
    document.getElementById("input_word").value = elem.value;
}

function fun_result(elem){
    document.getElementById("input_result").value = elem.value;
}

function CopyTextToClipboard(id) {

    var TextRange = document.createRange();

    TextRange.selectNode(document.getElementById(id));

    sel = window.getSelection();

    sel.removeAllRanges();

    sel.addRange(TextRange);

    document.execCommand("copy");

    alert("複製完成！")  //此行可加可不加

}
