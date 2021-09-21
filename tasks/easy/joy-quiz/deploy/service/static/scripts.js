async function getQuestions() {
    return await fetch('/api/questions/', {
        method: 'GET'
    }).then(response => response.json());
}


async function checkAnswers(answers) {
    return await fetch('/api/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(answers)
    }).then(response => response.json());
}

async function drawQuestion(questionId, text) {
    let questionElement = document.createElement('div');
    questionElement.className = 'question';
    questionElement.id = `question_${questionId}`;

    let questionTextElement = document.createElement('p');
    questionTextElement.innerText = `${questionId + 1}. ${text}`;

    questionElement.appendChild(questionTextElement);

    return questionElement;
}


async function drawVariantAnswer(questionId, variantId, variant) {
    let answerElement = document.createElement('div');
    answerElement.className = 'answer';

    let variantRadioElement = document.createElement('input');
    variantRadioElement.type = 'radio';
    variantRadioElement.name = `answer_${questionId}`;
    variantRadioElement.id = `variant_${questionId}_${variantId}`;
    variantRadioElement.value = variant;

    let variantLabelElement = document.createElement('label');
    variantLabelElement.htmlFor = `variant_${questionId}_${variantId}`;
    variantLabelElement.innerText = variant;

    answerElement.appendChild(variantRadioElement);
    answerElement.appendChild(variantLabelElement);

    return answerElement;
}


async function drawTextAnswer(questionId) {
    let answerElement = document.createElement('div');
    answerElement.className = 'answer';

    let answerTextElement = document.createElement('input');
    answerTextElement.type = 'text';
    answerTextElement.name = `answer_${questionId}`;

    answerElement.appendChild(answerTextElement);

    return answerElement;
}


async function drawForm(questions) {
    for (let questionId = 0; questionId < questions.length; questionId++) {
        const question = questions[questionId];

        const questionElement = await drawQuestion(questionId, question.text);

        if (question.variants) {
            for (let variantId = 0; variantId < question.variants.length; variantId++) {
                const answerElement = await drawVariantAnswer(
                    questionId,
                    variantId,
                    question.variants[variantId]
                );

                questionElement.appendChild(answerElement);
            }
        }
        else {
            const answerElement = await drawTextAnswer(questionId);

            questionElement.appendChild(answerElement);
        }

        document.forms.quiz.appendChild(questionElement);
    }
}


async function gatherAnswers(count) {
    const answers = [];

    for (let i = 0; i < count; i++) {
        let answerElement = document.forms.quiz[`answer_${i}`];
        answers.push(answerElement.value);
    }

    return answers;
}


async function reanimateElement(element) {
    element.style.animation = 'none';
    element.offsetHeight;
    element.style.animation = null;
}


async function submitForm(answers) {
    let prizeElement = document.getElementById('prize');

    prizeElement.hidden = true;

    const response = await checkAnswers(answers);

    for (let i = 0; i < response.verdicts.length; i++) {
        let questionElement = document.getElementById(`question_${i}`);

        if (response.verdicts[i]) {
            questionElement.className = 'question correct';
        }
        else {
            questionElement.className = 'question wrong';
        }

        await reanimateElement(questionElement);
    }

    if (response.prize) {
        prizeElement.hidden = false;
        prizeElement.innerText = response.prize;

        window.scrollTo(0, 0);
    }
}


async function init() {
    const questions = await getQuestions();

    await drawForm(questions);

    const submitFunction = async () => {
        const answers = await gatherAnswers(questions.length);

        await submitForm(answers);
    };

    document.getElementById('submit').addEventListener('click', submitFunction);

    document.body.addEventListener('keyup', async (event) => {
        if (event.key === 'Enter') {
            await submitFunction();
        }
    });
}


init();
