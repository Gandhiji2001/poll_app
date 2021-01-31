import datetime
import json


from django.utils import timezone
from django.db import models

class QuestionTags(models.Model):
    tags_text = models.CharField(max_length=20)

    class Meta:
        ordering = ['tags_text']
    def __str__(self):
        return self.tags_text


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = models.ManyToManyField(QuestionTags)         #type this in the shell

    class Meta:
        ordering = ['question_text']

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
#after this, errors may occur

class createQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    optionget = models.CharField(max_length=100)
    tagsget = models.CharField(max_length=200)
    voteget = models.CharField(max_length=50)

    def __str__(self):
        return self.choice_text
