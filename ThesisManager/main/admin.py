from django.contrib import admin
from .models import Campus, Course, Category, Supervisor, Thesis, GroupApplication, ThesisRequestAdd, ThesisRequestModify, ThesisRequestDelete, GroupApplicationStatus

# Register your models here.

admin.site.register(Campus)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Supervisor)
admin.site.register(Thesis)
admin.site.register(GroupApplication)
admin.site.register(GroupApplicationStatus)
admin.site.register(ThesisRequestAdd)
admin.site.register(ThesisRequestModify)
admin.site.register(ThesisRequestDelete)