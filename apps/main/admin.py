from django.contrib import admin
from .models import *

admin.site.register(Language)
admin.site.register(QuestionOption)

class ProjectCategoryTranslationAdmin(admin.TabularInline):
    model = ProjectCategoryTranslation

class ProjectCategoryAdmin(admin.ModelAdmin):
    inlines = [ProjectCategoryTranslationAdmin]


class QuestionGroupTranslationAdmin(admin.TabularInline):
    model = QuestionGroupTranslation

class QuestionGroupAdmin(admin.ModelAdmin):
    inlines = [QuestionGroupTranslationAdmin]

class QuestionTranslationAdmin(admin.TabularInline):
    model = QuestionTranslation

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionTranslationAdmin]

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
