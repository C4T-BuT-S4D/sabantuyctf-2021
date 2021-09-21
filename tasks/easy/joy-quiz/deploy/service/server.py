#!/usr/bin/env python3

import os
import quart
import asyncio

from quart import globals, helpers
from werkzeug import exceptions

import quiz


app = quart.Quart(__name__, static_url_path='/static/')
prize = os.getenv('PRIZE', 'No prize :(')
questions = quiz.load_questions_from_file('questions.json')


@app.route('/')
async def index() -> quart.Response:
    return await helpers.send_file('index.html')


@app.route('/api/questions/', methods=['GET'])
async def get_questions() -> quart.Response:
    result = []

    for question in questions:
        result.append({
            'text': question.text,
            'variants': question.variants
        })

    return quart.jsonify(result)


@app.route('/api/check/', methods=['POST'])
async def check_answers() -> quart.Response:
    answers = await globals.request.json

    if answers is None or not isinstance(answers, list):
        raise exceptions.BadRequest

    if len(answers) != len(questions):
        raise exceptions.BadRequest

    verdicts = []

    for question, answer in zip(questions, answers):
        verdicts.append(question.is_answer_correct(str(answer)))

    return quart.jsonify({
        'verdicts': verdicts,
        'prize': prize if all(verdicts) else None
    })


if __name__ == '__main__':
    asyncio.run(app.run_task())
