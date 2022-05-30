let scale = ['전혀 그렇지 않다', '그렇지 않다', '그렇지 않은 편이다', '그런 편이다', '그렇다', '매우 그렇다'];

const results = document.getElementsByClassName("print-result");
const tendencies = document.getElementsByClassName("tendency-list");


for (let i = 0; i < results.length; i++) {
    var id = results.item(i).id;
    var result_container = document.getElementById(id);

    if (id.substr(4) == "답변 스크립트")
        Print_Script(result_container);
    else if (id.substr(4) == "시선 추적")
        Print_Eye(id.substr(0, 4), result_container);
    else if (id.substr(4) == "표정 인식")
        Print_Face(id.substr(0, 4), result_container);
    else if (id.substr(4) == "키워드 카운트") {
        if (id.substr(2, 2) == "2_")
            Print_Corp(id, result_container);
        else
            Print_Dept(id, result_container);
    }
}

for (let i = 0; i < tendencies.length; i++) {
    var answer = tendencies.item(i).id.substr(3, 4);
    tendencies.item(i).innerText = scale[answer-1];
}


function Print_Script(result) {
    var stt_text = document.getElementById(id.substr(0, 4) + "stt-text").innerText;
    result.innerHTML = '<div class="mb-3">' + stt_text + '</div>';
}


function Print_Eye(iden, result) {
    var good = parseInt(document.getElementById(id.substr(0, 4) + "eye-tracking").innerText);
    var bad = good != 0? 100 - good: 0;
    console.log(bad);
    var innerhtml = '<canvas id="' + iden + 'eye-bar-chart" height="80"></canvas>';
    result.innerHTML = innerhtml;
    Eye_Bar_Chart(iden, good, bad);
}


function Print_Face(iden, result) {
    var face = document.getElementById(id.substr(0, 4) + "face-recog").innerText;
    face = JSON.parse(face);
    var innerhtml = '<canvas id="' + iden + 'face-bar-chart" height="80"></canvas>';
    result.innerHTML = innerhtml;
    Face_Bar_Chart(iden, face.positive, face.neutral, face.negative);
}


function Print_Corp(id, result) {
    var corp = document.getElementById(id.substr(0, 4) + "keyword-count").innerText;
    corp = JSON.parse(corp);
    var corp_name = Object.keys(corp)[0];
    var innerhtml = `
        <div class="mt-3 mb-2">선택 회사&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;{{corp_name}}</div>
        <div class="mb-3">카운트된 인재상 횟수&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;{{corp_count}}회</div>
    `;
    innerhtml = innerhtml.replace('{{corp_name}}', corp_name);
    innerhtml = innerhtml.replace('{{corp_count}}', corp[corp_name]);
    result.innerHTML = innerhtml;
}


function Print_Dept(id, result) {
    var dept = document.getElementById(id.substr(0, 4) + "keyword-count").innerText;
    dept = JSON.parse(dept);
    var dept_name = Object.keys(dept)[0];
    var innerhtml = `
        <div class="mt-3 mb-2">선택 직무&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;{{dept_name}}</div>
        <div class="mb-3">카운트된 직무 키워드&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;{{dept_count}}회</div>
    `;
    innerhtml = innerhtml.replace('{{dept_name}}', dept_name);
    innerhtml = innerhtml.replace('{{dept_count}}', dept[dept_name]);
    result.innerHTML = innerhtml;
}


function Eye_Bar_Chart(iden, good, bad) {
    var ctxB = document.getElementById(iden + "eye-bar-chart").getContext('2d');
    var myBarChart = new Chart(ctxB, {
        type: 'bar',
        data: {
            labels: ["중앙", "외각"],
            datasets: [{
                label: '시선 추적 결과',
                data: [good, bad],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1,
                maxBarThickness: 40
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
                borderWidth: 1,
                maxBarThickness: 40
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