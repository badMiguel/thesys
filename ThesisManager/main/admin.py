from django.contrib import admin
from .models import Campus, Course, Category, Supervisor, Thesis, GroupApplication, GroupApplicationAccepted, ThesisRequestAdd, ThesisRequestModify, ThesisRequestDelete 

# Register your models here.

admin.site.register(Campus)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Supervisor)
admin.site.register(Thesis)
admin.site.register(GroupApplication)
admin.site.register(GroupApplicationAccepted)
admin.site.register(ThesisRequestAdd)
admin.site.register(ThesisRequestModify)
admin.site.register(ThesisRequestDelete)