const results = document.getElementsByClassName("print-result");

for (let i = 0; i < results.length; i++) {
    var id = results.item(i).id;
    if (id.substr(4) == "답변 스크립트")
        Print_Script(id);
    else if (id.substr(4) == "시선 추적")
        Print_Eye(id);
    else if (id.substr(4) == "표정 인식")
        Print_Face(id);
}

function Print_Script(id) {
    var result_container = document.getElementById(id);
    result_container.innerHTML = document.getElementById(id.substr(0, 4) + "stt-text").innerText;
}

function Print_Eye() {

}

function Print_Face() {

}