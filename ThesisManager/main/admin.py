from django.contrib import admin
from .models import Campus, Course, Category, Supervisor, Thesis

# Register your models here.

admin.site.register(Campus)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Supervisor)
admin.site.register(Thesis)