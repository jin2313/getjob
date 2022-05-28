let left = 10;
let scale = ['매우 그렇다', '그렇다', '그런 편이다', '그렇지<br>않은 편이다', '그렇지 않다', '전혀<br>그렇지 않다'];
let count_element = new Array();
let result_element = [];
let time = null;
let timer = null;

const x = document.getElementById("remain");
const timer_text = document.getElementById("timer-text");
const submit_btn = document.getElementById("submit-btn");
const radio_btn = document.getElementsByClassName("radio-btn");
const redirect_btn = document.getElementById("redirect");


function Set_Attribute() {
    for (let i = 0; i < 6; i++) {
        var scale_id = "scale_" + i;
        document.getElementById(scale_id).innerHTML = scale[i];
    }

    for (let i = 0; i < radio_btn.length; i++) {
        radio_btn.item(i).name = "scale_" + (parseInt(i/6)+1);
        var q_num = (parseInt(i/6)+1) % 10 == 0? (parseInt(i/6)+1): "0" + (parseInt(i/6)+1)
        radio_btn.item(i).id = q_num + "_" + (i%6+1);
    }
}


function change(name, id) {
    if (!count_element.includes(name)) {
        count_element.push(name);
        result_element.push(id);
        left -= 1;
        x.innerText = left;
    }
    else {
        for (let i = 0; i < result_element.length; i++) {
            if (result_element[i].substr(0, 2) == id.substr(0, 2)) {
                result_element.splice(i, 1);
                result_element.push(id);
                break;
            }
        }
    }
}


function Check_All() {
    if (count_element.length != 10) {
        window.alert("모든 문항에 대해 답을 해 주세요")
        return false
    }
    return true
}


function Timer(condition) {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    timer_text.innerText = minutes + ":" + seconds;
    timer--;

    if (timer < 0 && condition == "tendency") {
        submit_btn.disabled = true;
        for (let i = 0; i < radio_btn.length; i++) {
            radio_btn.item(i).disabled = "disabled";
        }
        Check_Tendency();
    }
}


function Check_Tendency() {
    clearInterval(time);
    result_element.sort();
    if ((result_element.length != 0) && (result_element[0].substr(0, 2) == "10")) {
        var last_element = result_element.shift();
        result_element.push(last_element);
    }
    if (result_element.length == 0) {
        result_element.push("None");
    }
    Send_Result();
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim(); // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function Send_Result() {
    $.ajax({
        url: "http://127.0.0.1:8000/interviews/result/",
        type: "POST",
        traditional: true,
        data: {
            "tendency": result_element,
            "csrfmiddlewaretoken": getCookie('csrftoken'),
            "corp_name": document.getElementById("corp_name").innerText,
            "dept_name": document.getElementById("dept_name").innerText,
            "quest_id": document.getElementById("quest_id").innerText,
            "quest_level": document.getElementById("quest_level").innerText,
            "report_num": document.getElementById("report_num").innerText
        },
        success: function (data) {
            console.log("SUCCESS");
            redirect_btn.click();
        },
        error: function (errorMessage) {
            console.log("ERROR: " + errorMessage);
        }
    });
}


submit_btn.onclick = function(event) {
    var all_flag = Check_All();
    if (all_flag)
        Check_Tendency();
}


window.onload = function() {
    Set_Attribute();
    timer = 60;
    time = setInterval("Timer('tendency')", 1000);
}