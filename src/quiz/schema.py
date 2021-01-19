import graphene
from django.db.models import Q
from django.shortcuts import get_object_or_404
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Quiz, Question, Answer, UserAnswer
from course.models import CustomUser, Chapter
from .query_types import QuizType, QuestionType, AnswerType, UserAnswerType



class Query(graphene.ObjectType):
    allQuizzesChapter = graphene.List(QuizType, chapterId=graphene.Int())
    allQuizzesUser = graphene.List(QuizType, userId=graphene.Int())
    quizQuestions = graphene.List(QuestionType, quizId=graphene.Int())
    quizAnswers = graphene.List(AnswerType, questionId=graphene.Int())
    userAnswer = graphene.List(UserAnswerType, questionId=graphene.Int())

    @login_required
    def resolve_allQuizzesChapter(self, info, chapterId):
        quizzes = Quiz.objects.filter(chapter__id=chapterId)
        return quizzes

    @login_required
    def resolve_allQuizzesUser(self, info):
        user = info.context.user
        if user.is_student:
            quizzes = Quiz.objects.filter(student__id=user.id)
        else:
            quizzes = {}
        return quizzes
    
    @login_required
    def resolve_quizQuestions(self, info, quizId):
        questions = Question.objects.filter(quiz__id=quizId)
        return questions

    @login_required
    def resolve_quizAnswers(self, info, questionId):
        answers = Answer.objects.filter(question__id=questionId)
        return answers

    @login_required
    def resolve_userAnswer(self, info, questionId):
        user = info.context.user
        if not user.is_anonymous and not user.is_student:
            raise GraphQLError("You must be authenticated as a student!")
        userAnswer = Result.objects.filter(Q(student__id=user.id) & Q(question__id=questionId))
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
        
        chapter = get_object_or_404(Chapter, pk=chapterId)

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
        
        quiz = get_object_or_404(Quiz, pk=quizId)

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
        
        question = get_object_or_404(Question, pk=questionId)

        all_answers = Answer.objects.filter(question__id=questionId)
        for ans in all_answers:
            if ans.is_correct == True:
                raise GraphQLError("There is already a correct answer for this question!")
        
        answer = Answer(label=label, is_correct=isCorrect, question=question)
        answer.save()
        return CreateAnswer(answer=answer)


class CreateUserAnswer(graphene.Mutation):
    userAnswer = graphene.Field(userAnswerType)

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

        userAnswer = UserAnswer(student=user, quiz=quiz, question=question, answer=answer)
        userAnswer.save()
        return CreateUserAnswer(userAnswer=userAnswer)

    
class Mutation(graphene.ObjectType):
    create_quiz = CreateQuiz.Field()
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
    create_user_answer = CreateUserAnswer.Field()