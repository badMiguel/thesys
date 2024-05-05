from django import forms
from .models import Campus, Course, Category, Supervisor, Thesis

class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ['campus']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course']