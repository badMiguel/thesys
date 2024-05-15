from django import forms
from .models import Campus, Course, Category, Supervisor, Thesis  

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis

        fields = ['topic_number', 'title', 'description', 'category', 'supervisor', 'course', 'campus']

        labels = { 'topic_number': 'Thesis Number', 'description': 'Thesis Description', 'title': 'Thesis Title', 'category': 'Category', 'supervisor': 'Supervisor', 'course': 'Course', 'campus': 'Campus' }
