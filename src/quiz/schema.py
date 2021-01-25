import graphene
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Quiz, Question, Answer, UserAnswer
from course.models import Chapter
from .query_types import QuizType, QuestionType, AnswerType, UserAnswerType


class Query(graphene.ObjectType):
    quiz = graphene.Field(QuizType, chapterSlug=graphene.String(), required=True)
    allQuizzesUser = graphene.List(UserAnswerType)
    quizQuestions = graphene.List(QuestionType, quizId=graphene.Int(), required=True)
    quizAnswers = graphene.List(AnswerType, questionId=graphene.Int(), required=True)
    userAnswer = graphene.List(
        UserAnswerType, chapterSlug=graphene.String(), required=True
    )

    @login_required
    def resolve_quiz(self, info, chapterSlug):
        print(chapterSlug)
        quiz = Quiz.objects.get(chapter__slug=chapterSlug)
        return quiz

    @login_required
    def resolve_allQuizzesUser(self, info):
        user = info.context.user
        if not user.is_student:
            raise GraphQLError("Vous n'avez pas le droit de voir les quizzes")
        return (
            UserAnswer.objects.filter(student__id=user.id)
            .order_by("quiz__id")
            .distinct("quiz__id")
        )

    @login_required
    def resolve_quizQuestions(self, info, quizId):
        return Question.objects.filter(quiz__id=quizId)

    @login_required
    def resolve_quizAnswers(self, info, questionId):
        return Answer.objects.filter(question__id=questionId)

    @login_required
    def resolve_userAnswer(self, info, chapterSlug):
        student = info.context.user
        if not student.is_anonymous and not student.is_student:
            raise GraphQLError("You must be authenticated as a student!")

        quiz = Quiz.objects.get(chapter__slug=chapterSlug)
        userAnswers = UserAnswer.objects.filter(Q(student=student) & Q(quiz=quiz))
        return userAnswers


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


class UpdateQuiz(graphene.Mutation):
    quiz = graphene.Field(QuizType)

    class Arguments:
        quizId = graphene.Int()
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, quizId, title, description):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to update a quiz!")

        quiz = Quiz.objects.get(pk=quizId)
        quiz.title = title
        quiz.description = description
        quiz.save()
        return UpdateQuiz(quiz=quiz)


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


class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        questionId = graphene.Int()
        label = graphene.String()

    def mutate(self, info, questionId, label):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to update a question!")

        question = Question.objects.get(pk=questionId)
        question.label = label
        question.save()
        return UpdateQuestion(question=question)


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
        answers = question.answers
        if answers:
            condition = [ans for ans in answers.all() if ans.is_correct == True]
            if condition:
                isCorrect = False
        answer = Answer(label=label, is_correct=isCorrect, question=question)
        answer.save()
        return CreateAnswer(answer=answer)


class UpdateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        questionId = graphene.Int()
        answerId = graphene.Int()
        label = graphene.String()
        isCorrect = graphene.Boolean()

    def mutate(self, info, questionId, answerId, label, isCorrect):
        user = info.context.user
        if not user.is_teacher:
            raise GraphQLError("You must be a teacher to update an answer!")

        answer = Answer.objects.get(pk=answerId)
        question = Question.objects.get(pk=questionId)
        answers = question.answers
        if answers:
            condition = [ans for ans in answers.all() if ans.is_correct == True]
            if condition:
                isCorrect = False
        answer.label = label
        answer.is_correct = isCorrect
        answer.save()
        return UpdateAnswer(answer=answer)


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
        print(quizId, questionId, answerId)
        quiz = Quiz.objects.get(pk=quizId)
        question = Question.objects.get(pk=questionId)
        answer = Answer.objects.get(pk=answerId)

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
    update_quiz = UpdateQuiz.Field()
    update_question = UpdateQuestion.Field()
    update_answer = UpdateAnswer.Field()