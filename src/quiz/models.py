from django.db import models
from course.models import Chapter, CustomUser


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    chapter = models.OneToOneField(
        Chapter, on_delete=models.CASCADE, related_name="quiz"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        setattr(self, "title", getattr(self, "title", False).title())
        super(Quiz, self).save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    label = models.TextField()

    def __str__(self):
        return self.label


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    label = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class UserAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
