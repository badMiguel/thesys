from django import forms
from .models import Campus, Course, Category, Supervisor, Thesis

# class ThesisForm(forms.ModelForm):
#     class Meta:
#         model = Thesis
#         fields = ['campus', 'course', 'category', 'supervisor', 'thesis']
#     campus = forms.ModelChoiceField(queryset=Campus.objects.all(), empty_label=None)
#     course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
#     supervisor = forms.ModelChoiceField(queryset=Supervisor.objects.all(), empty_label=None)
#     thesis = forms.ModelChoiceField(queryset=Thesis.objects.all(), empty_label=None)
    

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis

        fields = ['topic_number', 'title', 'category', 'supervisor', 'course', 'campus']

        labels = { 'topic_number': 'Thesis Number', 'title': 'Thesis Title', 'category': 'Category', 'supervisor': 'Supervisor', 'course': 'Course', 'campus': 'Campus' }
