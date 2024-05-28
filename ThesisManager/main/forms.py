from django import forms
from .models import Thesis, ThesisRequestAdd, ThesisRequestModify, ThesisRequestDelete, Campus, Category, Course, Supervisor, GroupApplication

class ThesisFormBase(forms.ModelForm):    
    class Meta:
        fields = ['topic_number', 'title', 'description', 'category', 'supervisor', 'course', 'campus', 'group_taker_limit']

        labels = { 'topic_number': 'Thesis Number', 'description': 'Thesis Description', 'title': 'Thesis Title', 'category': 'Category', 'supervisor': 'Supervisor', 'course': 'Course', 'campus': 'Campus', 'group_taker_limit': 'Maximum Groups' }
        
        widgets = {
            'topic_number': forms.NumberInput(attrs={'class': 'field', 'placeholder': 'Enter thesis number'}),
            'title': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter thesis title'}),
            'description': forms.Textarea(attrs={'class': 'field', 'placeholder': 'Enter thesis description'}),
            'category': forms.Select(attrs={'class': 'field'}),
            'supervisor': forms.Select(attrs={'class': 'field', 'placeholder': 'Enter supervisor name'}),
            'course': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter course name', 'multiple': ''}),
            'campus': forms.CheckboxSelectMultiple(attrs={'class': 'field-checkbox', 'placeholder': 'Enter campus name', 'multiple': ''}),
            'group_taker_limit': forms.NumberInput(attrs={'class': 'field', 'placeholder': 'Enter maximum groups - No limit by default'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_taker_limit'].required = False
        
class ThesisForm(ThesisFormBase):    
    class Meta(ThesisFormBase.Meta):
        model = Thesis
    
        
class ThesisRequestFormAdd(ThesisFormBase):
    class Meta(ThesisForm.Meta): 
        model = ThesisRequestAdd
        
    def topic_number_exist(self):
        r_topic_number = self.cleaned_data.get('topic_number')
        if Thesis.objects.filter(topic_number=r_topic_number).exists():
            raise forms.ValidationError('Topic number already exists in the database.')
        
    def clean_topic_number(self):
        self.topic_number_exist()
        return self.cleaned_data['topic_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['supervisor']
class ThesisRequestFormModify(ThesisFormBase):
    class Meta(ThesisForm.Meta): 
        model = ThesisRequestModify

class ThesisRequestFormDelete(ThesisFormBase):
    class Meta(ThesisForm.Meta): 
        model = ThesisRequestDelete

class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        
        fields = ['campus']

        labels = {'campus': 'Campus'}

        widgets = {'campus': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter campus name'}),}
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        
        fields = ['category']

        labels = {'category': 'Category'}

        widgets = {'category': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter category name'}),}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        
        fields = ['course']

        labels = {'course': 'Course'}

        widgets = {'course': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter course name'}),}

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        
        fields = ['supervisor']

        labels = {'supervisor': 'Supervisor'}

        widgets = {'supervisor': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Enter supervisor name'}),}

class GroupApplicationForm(forms.ModelForm):
    class Meta:
        model = GroupApplication
        fields = ['thesis', 'group', 'status']