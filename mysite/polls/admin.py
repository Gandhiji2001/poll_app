from django.contrib import admin
from .models import Question
from .models import Choice
from .models import QuestionTags

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']




admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(QuestionTags)
