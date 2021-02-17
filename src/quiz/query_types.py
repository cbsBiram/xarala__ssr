from graphene_django import DjangoObjectType
from .models import Quiz, Question, Answer, UserAnswer


class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        convert_choices_to_enum = False


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        convert_choices_to_enum = False


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        convert_choices_to_enum = False


class UserAnswerType(DjangoObjectType):
    class Meta:
        model = UserAnswer
