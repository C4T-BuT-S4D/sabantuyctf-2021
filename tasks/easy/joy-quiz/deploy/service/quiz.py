#!/usr/bin/env python3

import json
import typing
import random
import difflib
import pydantic


def are_fuzzy_equal(expected: str, actual: str, max_delta=1) -> bool:
    diff = ''.join(difflib.ndiff(
        expected.lower().strip(),
        actual.lower().strip()
    ))

    delta = max(diff.count('-'), diff.count('+'))

    return delta <= max_delta


class TextAnswer(pydantic.BaseModel):
    text: str = pydantic.Field(...)


class Variant(pydantic.BaseModel):
    text: str = pydantic.Field(...)
    correct: bool = pydantic.Field(False)


class VariantAnswer(pydantic.BaseModel):
    variants: typing.List[Variant] = pydantic.Field(...)
    shuffle: bool = pydantic.Field(False)

    @pydantic.validator('variants')
    def validate_variants(cls, variants) -> bool:
        if sum(variant.correct for variant in variants) != 1:
            raise ValueError('should be only one correct variant')

        return variants


class Question(pydantic.BaseModel):
    text: str = pydantic.Field(...)
    answer: typing.Union[TextAnswer, VariantAnswer] = pydantic.Field(...)
    fuzzy: bool = pydantic.Field(False)

    @property
    def variants(self) -> typing.Optional[typing.List[str]]:
        if not isinstance(self.answer, VariantAnswer):
            return None

        result = [variant.text for variant in self.answer.variants]

        if self.answer.shuffle:
            random.shuffle(result)

        return result

    @property
    def correct_answer(self) -> str:
        if isinstance(self.answer, TextAnswer):
            return self.answer.text
        elif isinstance(self.answer, VariantAnswer):
            return next(variant.text for variant in self.answer.variants if variant.correct)

    def is_answer_correct(self, answer: str) -> bool:
        if not self.fuzzy:
            return answer.strip() == self.correct_answer

        return are_fuzzy_equal(self.correct_answer, answer)


def load_questions(data: typing.List[dict]) -> typing.List[Question]:
    return [Question.parse_obj(obj) for obj in data]


def load_questions_from_file(filename: str) -> typing.List[Question]:
    with open(filename, 'r') as file:
        return load_questions(json.load(file))
