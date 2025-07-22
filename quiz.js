import * as CONSTANTS from './constants.js';

//const lang = "ITA";




const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const input_topic = urlParams.get('topic');
const input_random_topic = urlParams.get('random_topic');
const input_num_of_questions = urlParams.get('num_of_questions');
const input_num_of_replies = urlParams.get('num_of_replies');
const input_language = urlParams.get('language');

if (input_language == ("italian")) {
    var CONST = CONSTANTS.ITA;
} else if (input_language == ("english")) {
    var CONST = CONSTANTS.ENG;
} else
    var CONST = CONSTANTS.ENG;


document.getElementById('about_img').style.display = 'none';
document.getElementById('section1').style.display = 'none';
document.getElementById('section2').style.display = 'none';
document.getElementById('h1_1').innerHTML += CONST.INTRODUCTION;
document.getElementById('h1_1').style.display = 'none';
document.getElementById('go_to_test').innerHTML = CONST.GO_TO_TEST;
loader.style.display = 'block'; // mostra l'animazione loading

document.getElementById('headerQuestionary').innerHTML += CONST.QUESTIONARY;
document.getElementById('submit1').innerHTML += CONST.SUBMIT;

const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic: input_topic, random_topic: input_random_topic, num_of_questions: input_num_of_questions, num_of_replies: input_num_of_replies, language: input_language })
};

//Recupera il JSON dal servizio REST e visualizza i dati nella pagina HTML
fetch('http://127.0.0.1:8080/api/v.1.0/middleware_chatgpt', requestOptions)
    .then(response => response.json())
    //Promise.resolve(data)
    .then(data => {
        document.getElementById('section_topic').innerHTML = data.sintesi;

        loader.style.display = 'none'; // nasconde l'animazione
        document.getElementById('about_img').style.display = 'block';
        document.getElementById('section1').style.display = 'block';
        document.getElementById('section2').style.display = 'block';
        document.getElementById('h1_1').style.display = 'block';
        document.getElementById('header_topic').innerHTML = data.topic;
        document.getElementById('header_topic1').innerHTML = data.topic;



        // Questionario
        const ourMainDiv = document.getElementById('work');
        const questionsDiv = document.querySelector('.questions');

        var num = 0;
        var questionNum = 1;
        data.questionario.forEach((question, index) => {
            if (num == 7) {
                num = 1
            } else {
                num += 1;
            }
            const questionDivFluid = document.createElement('div');
            questionDivFluid.classList.add('container-fluid');

            const questionDivRow = document.createElement('div');
            questionDivRow.classList.add('row');
            questionDivRow.classList.add('d_flex');

            const questionForm = document.createElement('div');
            questionForm.classList.add('questionForm');

            const imageCol = document.createElement('div');
            imageCol.classList.add('col-md-6');
            imageCol.classList.add('verticalAlign');


            const line = document.createElement('div');
            line.classList.add('line');

            const imageDiv = document.createElement('div');
            imageDiv.classList.add('work_img');
            imageDiv.innerHTML = "<img src='images/work_img" + num + ".png'></img>";

            const questionDivCol = document.createElement('div');
            questionDivCol.classList.add('col-md-6');
            questionDivCol.classList.add('questions');

            const questionDivTitle = document.createElement('div');
            questionDivTitle.classList.add('titlepage');
            questionDivTitle.classList.add('question');

            const questionDivLast = document.createElement('div');

            const questionTitle = document.createElement('h2');
            questionTitle.textContent = `${index + 1}. ${question.domanda}`;
            questionDivTitle.appendChild(questionTitle);

            const answersDiv = document.createElement('p');
            answersDiv.classList.add('answer');
            Object.entries(question.risposte).forEach(([key, value]) => {
                const label = document.createElement('label');
                const br = document.createElement('br');
                const radio = document.createElement('input');
                radio.classList.add('radioCircle');
                radio.type = 'radio';
                radio.name = `question-${index}`;
                radio.value = key;
                label.appendChild(radio);
                label.appendChild(document.createTextNode(`${value}`));
                answersDiv.appendChild(label);
                label.parentNode.insertBefore(br, label.nextSibling);
            });

            ourMainDiv.appendChild(questionDivFluid);
            questionDivFluid.appendChild(questionDivRow);
            questionDivRow.appendChild(questionForm);

            if (questionNum % 2 == 1) {
                questionNum += 1;

                questionForm.appendChild(questionDivCol);
                questionDivCol.appendChild(questionDivTitle);
                questionDivTitle.appendChild(questionDivLast);
                questionDivLast.appendChild(answersDiv);

                questionForm.appendChild(imageCol);
                imageCol.appendChild(imageDiv);

            } else {
                questionNum += 1;
                questionForm.appendChild(imageCol);
                imageCol.appendChild(imageDiv);

                questionForm.appendChild(questionDivCol);
                questionDivCol.appendChild(questionDivTitle);
                questionDivTitle.appendChild(questionDivLast);
                questionDivLast.appendChild(answersDiv);
            }

            if (index < data.questionario.length - 1) {
                questionDivFluid.appendChild(line);

            }
        });
        document.getElementById('aboutImage').src = data.imageUrl;
        // Gestione del submit del form
        const form = document.querySelector('form');

        form.addEventListener('submit', (event) => {
            event.preventDefault();

            // Calcola il punteggio e indica le risposte corrette e sbagliate
            let punteggio = 0;
            let correctAnswers = 0;
            let wrongAnswers = 0;
            const questionDivs = document.querySelectorAll('.question');

            questionDivs.forEach((questionDivTitle, index) => {
                const selectedAnswer = document.querySelector(`input[name="question-${index}"]:checked`);
                if (selectedAnswer && selectedAnswer.value === data.questionario[index].risposta_corretta) {
                    questionDivTitle.classList.add('correct');
                    punteggio++;
                } else {
                    questionDivTitle.classList.add('incorrect');
                }
            });

            // Stampa il punteggio
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const threshold = urlParams.get('threshold_percent');
            const punteggioDiv = document.createElement('div');
            punteggioDiv.classList.add('section2');
            const punteggioTitle2 = document.createElement('span');
            punteggioTitle2.classList.add('bluTitle');
            punteggioTitle2.textContent = CONST.RESULT;
            const punteggioTitle = document.createElement('span');
            punteggioTitle.classList.add('blackTitle');
            punteggioTitle.textContent = CONST.QUIZ;
            punteggioDiv.appendChild(punteggioTitle2);
            punteggioTitle2.parentNode.insertBefore(punteggioTitle, punteggioTitle2.nextSibling);
            const punteggioText = document.createElement('p');
            if (((punteggio / data.questionario.length) * 100) >= threshold) {
                punteggioText.textContent = CONST.SCORE_OK1 + threshold + '%. ' + CONST.SCORE_OK2 + ((punteggio / data.questionario.length) * 100).toFixed(2) + '%.';
                const coccarda = document.createElement('div');
                coccarda.classList.add('resultImage');
                coccarda.innerHTML = "<img src='images/coccarda.png'></img>";
                punteggioText.appendChild(coccarda);
            } else {
                punteggioText.textContent = CONST.SCORE_KO1 + threshold + '%. ' + CONST.SCORE_KO2 + ((punteggio / data.questionario.length) * 100).toFixed(2) + '%.';
                const sadFace = document.createElement('div');
                sadFace.classList.add('resultImage');
                sadFace.innerHTML = "<img src='images/sadFace.png'></img>";
                punteggioText.appendChild(sadFace);
            }
            punteggioDiv.appendChild(punteggioText);
            ourMainDiv.parentNode.insertBefore(punteggioDiv, ourMainDiv.nextSibling);

            // Mostra le risposte corrette
            const corretteDiv = document.createElement('div');
            corretteDiv.classList.add('section');
            const corretteTitle = document.createElement('h2');
            corretteTitle.textContent = CONST.CORRECT_ANSW;
            corretteDiv.appendChild(corretteTitle);

            data.questionario.forEach((question, index) => {
                const correttaDiv = document.createElement('div');
                correttaDiv.classList.add('question');
                correttaDiv.classList.add('correct');
                const correttaTitle = document.createElement('h3');
                correttaTitle.textContent = `${index + 1}. ${question.domanda}`;
                correttaDiv.appendChild(correttaTitle);
                const rispostaCorrettaText = document.createElement('p');

            })

            // Gestione della risposta del questionario
            const form = document.querySelector('form');

            const questions = document.querySelectorAll('.question');

            questions.forEach((question, index) => {
                const selectedAnswer = form.elements[`question-${index}`].value;
                const correctAnswer = data.questionario[index].risposta_corretta;
                if (selectedAnswer === correctAnswer) {
                    question.classList.add('correct');
                    correctAnswers++;
                } else {
                    question.classList.add('wrong');
                    wrongAnswers++;
                }
            });

            // Stampa dei risultati
            const resultDiv = document.createElement('div');
            resultDiv.innerHTML = CONST.RESULT_CORRECT1 + correctAnswers + CONST.RESULT_CORRECT2 + data.questionario.length + ' .';

            if (wrongAnswers > 0) {
                resultDiv.innerHTML += CONST.RESULT_WRONG1 + wrongAnswers + CONST.RESULT_WRONG2;
            }

            if (correctAnswers === data.questionario.length) {
                resultDiv.classList.add('correct');
            } else {
                resultDiv.classList.add('wrong');
            }

            punteggioDiv.appendChild(resultDiv);

            document.getElementById('submit1').style.display = 'none';
        });

    })

    .catch(error => {
        // gestisci l'errore
        console.log("errore nell'invocazione del servizio");
        loader.style.display = 'none'; // nasconde l'animazione
    });
