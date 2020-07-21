# from django.db import models
# from course.models import Course, Lesson, CustomUser

# # Create your models here.


# class Quiz(models.Model):
#     title = models.CharField(max_length=100)
#     course = models.ForeignKey(
#         Course, on_delete=models.CASCADE, related_name='quizzes')
#     lesson = models.OneToOneField(
#         Lesson, on_delete=models.CASCADE, related_name='quizzes')

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         setattr(self, 'title', getattr(self, 'title', False).title())
#         super(Quiz, self).save(*args, **kwargs)


# class Question(models.Model):
#     quiz = models.ForeignKey(
#         Quiz, on_delete=models.CASCADE, related_name='questions')
#     text = models.CharField('Question', max_length=500)

#     def __str__(self):
#         return self.text


# class Answer(models.Model):
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE, related_name='answers')
#     text = models.CharField('', max_length=500)
#     is_correct = models.BooleanField('Correct answer', default=False)

#     def __str__(self):
#         return self.text


# class TakenQuiz(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name='taken_quizzes')
#     quiz = models.ForeignKey(
#         Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
#     course = models.ForeignKey(
#         Course, on_delete=models.CASCADE, related_name='taken_quizzes')
#     score = models.FloatField()
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.student.user.email}: {self.quiz.title}'


# class StudentAnswer(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name='quiz_answers')
#     answer = models.ForeignKey(
#         Answer, on_delete=models.CASCADE, related_name='+')
