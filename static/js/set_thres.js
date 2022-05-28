const video = document.querySelector("#video");
const slide = document.getElementById("myRange");
const slider_value = document.getElementById("thres-value");
const set_btn = document.getElementById("set-btn");
const redirect_btn = document.getElementById("redirect");

window.onload = function() {
    slider_value.innerHTML = slide.value;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then (function (stream) {
                video.srcObject = stream;
                video.play()
            })
            .catch (function (error) {
                console.log("ERROR");
            });
    }
}


slide.oninput = function() {
    slider_value.innerHTML = this.value;
}


set_btn.onclick = function(event) {
    $.ajax({
        url: "http://127.0.0.1:8000/thres/",
        type: "POST",
        data: {
            "threshold": slider_value.innerText,
            "csrfmiddlewaretoken": getCookie('csrftoken')
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