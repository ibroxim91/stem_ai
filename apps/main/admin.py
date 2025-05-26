from django.contrib import admin
from .models import *

admin.site.register(Language)



class ProjectCategoryTranslationAdmin(admin.TabularInline):
    model = ProjectCategoryTranslation


class ProjectPromptTranslationAdmin(admin.TabularInline):
    model = ProjectPromptTranslation


class ProjectCategoryAdmin(admin.ModelAdmin):
    inlines = [ProjectCategoryTranslationAdmin, ProjectPromptTranslationAdmin]


class QuestionGroupTranslationAdmin(admin.TabularInline):
    model = QuestionGroupTranslation

class QuestionGroupAdmin(admin.ModelAdmin):
    inlines = [QuestionGroupTranslationAdmin]

class QuestionTranslationAdmin(admin.TabularInline):
    model = QuestionTranslation



class QuestionPromptTranslationAdmin(admin.TabularInline):
    model = QuestionPromptTranslation

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionTranslationAdmin, QuestionPromptTranslationAdmin]


class QuestionOptionTranslationAdmin(admin.TabularInline):
    model = QuestionOptionTranslation


class QuestionOptionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionTranslationAdmin]

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionOption, QuestionOptionAdmin)
