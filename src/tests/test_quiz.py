import pytest

from course.models import Chapter, Course
from quiz.models import Answer, Question, Quiz, UserAnswer
from users.models import CustomUser as User


@pytest.mark.django_db
def test_quiz_create():
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )

    quiz = Quiz.objects.create(
        title="Quiz Test", description="This is a test quiz", chapter=chapter
    )
    assert quiz.title == "Quiz Test"
    assert quiz.description == "This is a test quiz"
    assert quiz.chapter == chapter


@pytest.mark.django_db
def test_question_create():
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )
    quiz = Quiz.objects.create(
        title="Quiz test", description="This is a test quiz", chapter=chapter
    )

    question = Question.objects.create(
        label="Question for quiz 1",
        quiz=quiz,
    )
    assert question.label == "Question for quiz 1"
    assert question.quiz == quiz


@pytest.mark.django_db
def test_answer_create():
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )
    quiz = Quiz.objects.create(
        title="Quiz test", description="This is a test quiz", chapter=chapter
    )
    question = Question.objects.create(
        label="Question for quiz 1",
        quiz=quiz,
    )

    answer = Answer.objects.create(
        question=question, label="Answer for question 1", is_correct=True
    )
    assert answer.label == "Answer for question 1"
    assert answer.question == question
    assert answer.is_correct == True


@pytest.mark.django_db
def test_user_answer_create():
    student = User.objects.create(email="test@test.com", is_student=True)
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )
    quiz = Quiz.objects.create(
        title="Quiz test", description="This is a test quiz", chapter=chapter
    )
    question = Question.objects.create(
        label="Question for quiz 1",
        quiz=quiz,
    )
    answer = Answer.objects.create(
        question=question, label="Answer for question 1", is_correct=True
    )

    user_answer = UserAnswer.objects.create(
        student=student, quiz=quiz, question=question, answer=answer
    )

    assert user_answer.student == student
    assert user_answer.quiz == quiz
    assert user_answer.question == question
    assert user_answer.answer == answer
