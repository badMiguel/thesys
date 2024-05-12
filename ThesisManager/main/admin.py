from django.contrib import admin
from .models import Campus, Course, Category, Supervisor, Thesis, ThesisRequest, GroupApplication

# Register your models here.

admin.site.register(Campus)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Supervisor)
admin.site.register(Thesis)
admin.site.register(ThesisRequest)
admin.site.register(GroupApplication)