from django import forms
from .models import Thesis, ThesisRequest  

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis

        fields = ['topic_number', 'title', 'description', 'category', 'supervisor', 'course', 'campus']

        labels = { 'topic_number': 'Thesis Number', 'description': 'Thesis Description', 'title': 'Thesis Title', 'category': 'Category', 'supervisor': 'Supervisor', 'course': 'Course', 'campus': 'Campus' }
        
        widgets = {
            'topic_number': forms.NumberInput(attrs={'class': 'field', 'placeholder': 'Enter thesis number'}),
            'title': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter thesis title'}),
            'description': forms.Textarea(attrs={'class': 'field', 'placeholder': 'Enter thesis description'}),
            'category': forms.Select(attrs={'class': 'field'}),
            'supervisor': forms.Select(attrs={'class': 'field', 'placeholder': 'Enter supervisor name'}),
            'course': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter course name', 'multiple': ''}),
            'campus': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter campus name', 'multiple': ''}),
        }

class RequestChange(forms.ModelForm):
    class Meta:
        model = ThesisRequest

        fields = ['requested_by', 'thesis_request']

        labels = { 'requested_by': 'Requested By', 'thesis_request': 'Thesis Request'} 
        
        # fields = ['requested_by', 'topic_number', 'title', 'description', 'category', 'supervisor', 'course', 'campus']

        # labels = { 'requested_by': 'Requested By', 'topic_number': 'Thesis Number', 'description': 'Thesis Description', 'title': 'Thesis Title', 'category': 'Category', 'supervisor': 'Supervisor', 'course': 'Course', 'campus': 'Campus' }
        
        # widgets = {
        #     'topic_number': forms.NumberInput(attrs={'class': 'field', 'placeholder': 'Enter thesis number'}),
        #     'title': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter thesis title'}),
        #     'description': forms.Textarea(attrs={'class': 'field', 'placeholder': 'Enter thesis description'}),
        #     'category': forms.Select(attrs={'class': 'field'}),
        #     'supervisor': forms.Select(attrs={'class': 'field', 'placeholder': 'Enter supervisor name'}),
        #     'course': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter course name', 'multiple': ''}),
        #     'campus': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter campus name', 'multiple': ''}),
        # }
