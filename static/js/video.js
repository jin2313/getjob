let time = null;
let timer = null;
let video_flag = null;
let audio_flag = null;
let redirect_btn = null;

const timer_text = document.getElementById("timer-text");
const interview_video = document.querySelector("#video");
const start_btn = document.querySelector("#video-start");
const stop_btn = document.querySelector("#video-stop");
const quest_num = document.getElementById("quest_id").innerText;
const level = document.getElementById("quest_level").innerText;

let mediaRecorder = null; // MediaRecorder(녹화기) 변수 선언
const arrVideoData = []; // 영상 데이터를 담아줄 배열 선언


function Timer(condition) {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    timer_text.innerText = minutes + ":" + seconds;
    timer--;

    if (timer < 0 && condition == "initial") {
        start_btn.click();
    }

//    if (timer == 69 && condition == "introduce") {
    if (timer == 87 && condition == "introduce") {
        stop_btn.style.backgroundColor = "#b6c1dd";
        stop_btn.disabled = false;
    }

//    if (timer == 39 && condition == "else") {
    if (timer == 57 && condition == "else") {
        stop_btn.style.backgroundColor = "#b6c1dd";
        stop_btn.disabled = false;
    }

    if (timer < 0 && condition == "introduce") {
        stop_btn.click();
    }

    if (timer < 0 && condition == "else") {
        stop_btn.click();
    }
}


function Button_Activate() {
    start_btn.style.backgroundColor = "#a4a4a4";
    start_btn.disabled = true;
    if (level == "1") {
        timer = 90;
        time = setInterval("Timer('introduce')", 1000);
    }
    else {
        timer = 60;
        time = setInterval("Timer('else')", 1000);
    }
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


// 시작 버튼 이벤트 처리
start_btn.onclick = async function(event) {
    clearInterval(time);
    Button_Activate();

    const mediaStream = await navigator.mediaDevices.getUserMedia({ // 카메라 입력영상 스트림 생성
        audio: true,
        video: true
    });

    interview_video.srcObject = mediaStream; // 실시간 영상 재생 처리: 첫번째 video태그에서 재생
    interview_video.onloadedmetadata = (event)=> {
        interview_video.play();
    }

    mediaRecorder = new MediaRecorder(mediaStream, {mimeType: 'video/webm;codecs=h264'}); // mediaRecorder객체(녹화기) 생성

    mediaRecorder.ondataavailable = (event)=> { // 녹화 데이터 입력 이벤트 처리
        const data = event.data;
        if (data && data.size > 0) {
            arrVideoData.push(data); // 녹화 데이터(Blob)가 들어올 때마다 배열에 담아두기
        }
    }

    mediaRecorder.onstop = (event)=> { // 녹화 종료 이벤트 처리
        videoBlob = new Blob(arrVideoData, {type: 'video/webm'}); // 배열에 담아둔 녹화 데이터들을 통합한 Blob객체 생성
        SendVideo(videoBlob);
        arrVideoData.splice(0); // 기존 녹화 데이터 제거
    }

    mediaRecorder.start(); // 녹화 시작
}


// 종료 버튼 이벤트 처리
stop_btn.onclick = (event)=> {
    clearInterval(time);
    mediaRecorder.stop(); // 녹화 종료
}


const SendVideo = blob => {
    if (blob == null) {
        console.log("No Blob Data");
        return;
    }

    var today = new Date();
    var date_string = today.getFullYear() + '_' + ('0' + (today.getMonth() + 1)).slice(-2)  + '_' + ('0' + today.getDate()).slice(-2);
    var time_string = ('0' + today.getHours()).slice(-2) + '_' + ('0' + today.getMinutes()).slice(-2);

    let filename = date_string + '_' + time_string + '.webm';
    const file = new File([blob], filename);
    var csrf_token = getCookie('csrftoken');

    let fd = new FormData();
    fd.append("fname", filename);
    fd.append("file", file);
    fd.append("csrfmiddlewaretoken", csrf_token);
    fd.append("corp_name", document.getElementById("corp_name").innerText);
    fd.append("dept_name", document.getElementById("dept_name").innerText);
    fd.append("quest_id", document.getElementById("quest_id").innerText);
    fd.append("quest_level", document.getElementById("quest_level").innerText);
    fd.append("report_num", document.getElementById("report_num").innerText);

    $.ajax({
        url: "http://127.0.0.1:8000/interviews/result/",
        type: "POST",
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        data: fd,
        success: function (data) {
            redirect_btn.click()
        },
//        error: function (errorMessage) {
//            console.log("ERROR: " + errorMessage);
//        }
    });
}


window.onload = function() {
    timer = 30;
    time = setInterval("Timer('initial')", 1000);
    if (quest_num == "7") {
        redirect_btn = document.getElementById("home_redirect");
    }
    else {
        redirect_btn = document.getElementById("quest_redirect");
    }
};