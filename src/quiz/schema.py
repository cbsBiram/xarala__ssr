import graphene
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Quiz, Question, Answer, UserAnswer
from course.models import Chapter
from .query_types import QuizType, QuestionType, AnswerType, UserAnswerType


class Query(graphene.ObjectType):
    allQuizzesChapter = graphene.List(QuizType, chapterId=graphene.Int(), required=True)
    allQuizzesUser = graphene.List(QuizType, userId=graphene.Int(), required=True)
    quizQuestions = graphene.List(QuestionType, quizId=graphene.Int(), required=True)
    quizAnswers = graphene.List(AnswerType, questionId=graphene.Int(), required=True)
    userAnswer = graphene.List(UserAnswerType, questionId=graphene.Int(), required=True)

    @login_required
    def resolve_allQuizzesChapter(self, info, chapterId):
        return Quiz.objects.filter(chapter__id=chapterId)

    @login_required
    def resolve_allQuizzesUser(self, info):
        user = info.context.user
        if not user.is_student:
            raise GraphQLError("Vous n'avez pas le droit de voir les quizzes")
        return Quiz.objects.filter(student__id=user.id)

    @login_required
    def resolve_quizQuestions(self, info, quizId):
        return Question.objects.filter(quiz__id=quizId)

    @login_required
    def resolve_quizAnswers(self, info, questionId):
        return Answer.objects.filter(question__id=questionId)

    @login_required
    def resolve_userAnswer(self, info, questionId):
        user = info.context.user
        if not user.is_anonymous and not user.is_student:
            raise GraphQLError("You must be authenticated as a student!")
        userAnswer = UserAnswer.objects.filter(
            Q(student__id=user.id) & Q(question__id=questionId)
        )
        return userAnswer


class CreateQuiz(graphene.Mutation):
    quiz = graphene.Field(QuizType)

    class Arguments:
        chapterId = graphene.Int()
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, chapterId, title, description):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to add a quiz!")

        chapter = Chapter.objects.get(pk=chapterId)
        quiz = Quiz(title=title, description=description, chapter=chapter)
        quiz.save()
        return CreateQuiz(quiz=quiz)


class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        quizId = graphene.Int()
        label = graphene.String()

    def mutate(self, info, quizId, label):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to add a question!")

        quiz = Quiz.objects.get(pk=quizId)
        question = Question(label=label, quiz=quiz)
        question.save()
        return CreateQuestion(question=question)


class CreateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        questionId = graphene.Int()
        label = graphene.String()
        isCorrect = graphene.Boolean()

    def mutate(self, info, questionId, label, isCorrect):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to add an answer!")

        question = Question.objects.get(pk=questionId)
        Answer.objects.filter(question__id=questionId).update(is_correct=False)
        answer = Answer(label=label, is_correct=isCorrect, question=question)
        answer.save()
        return CreateAnswer(answer=answer)


class CreateUserAnswer(graphene.Mutation):
    userAnswer = graphene.Field(UserAnswerType)

    class Arguments:
        quizId = graphene.Int()
        questionId = graphene.Int()
        answerId = graphene.Int()

    def mutate(self, info, quizId, questionId, answerId):
        user = info.context.user
        if not user.is_student:
            raise GraphQLError("You must be a student to apply to the quiz!")

        quiz = Quiz.object.get(pk=quizId)
        question = Question.object.get(pk=questionId)
        answer = Answer.object.get(pk=answerId)

        userAnswer = UserAnswer(
            student=user, quiz=quiz, question=question, answer=answer
        )
        userAnswer.save()
        return CreateUserAnswer(userAnswer=userAnswer)


class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
    create_user_answer = CreateUserAnswer.Field()