const results = document.getElementsByClassName("print-result");


for (let i = 0; i < results.length; i++) {
    var id = results.item(i).id;
    var result_container = document.getElementById(id);

    if (id.substr(4) == "답변 스크립트") {
        Print_Script(result_container);
    }
    else if (id.substr(4) == "시선 추적") {
        Print_Eye(id.substr(0, 4), result_container);
    }
    else if (id.substr(4) == "표정 인식")
        Print_Face(id.substr(0, 4), result_container);
}


function Print_Script(result) {
    var stt_text = document.getElementById(id.substr(0, 4) + "stt-text").innerText;
    result.innerHTML = "<span>" + stt_text + "</span>";
}


function Print_Eye(iden, result) {
    var good = parseInt(document.getElementById(id.substr(0, 4) + "eye-tracking").innerText);
    var innerhtml = '<canvas id="' + iden + 'eye-bar-chart"></canvas>';
//    `;
    result.innerHTML = innerhtml;
    Eye_Bar_Chart(iden, good);
}


function Print_Face(iden, result) {
    var face = document.getElementById(id.substr(0, 4) + "face-recog").innerText;
    face = JSON.parse(face);
    var innerhtml = '<canvas id="' + iden + 'face-bar-chart"></canvas>';
    result.innerHTML = innerhtml;
    Face_Bar_Chart(iden, face.positive, face.neutral, face.negative);
}


function Eye_Bar_Chart(iden, good) {
    var ctxB = document.getElementById(iden + "eye-bar-chart").getContext('2d');
    var myBarChart = new Chart(ctxB, {
        type: 'bar',
        data: {
            labels: ["중앙", "외각"],
            datasets: [{
                label: '시선 추적 결과',
                data: [good, 100-good],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}


function Face_Bar_Chart(iden, positive, neutral, negative) {
    var ctxB = document.getElementById(iden + "face-bar-chart").getContext('2d');
    var myBarChart = new Chart(ctxB, {
        type: 'bar',
        data: {
            labels: ["긍정", "중립", "부정"],
            datasets: [{
                label: '표정 인식 결과',
                data: [positive, neutral, negative],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}