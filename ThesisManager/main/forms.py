from django import forms
from .models import Thesis, ThesisRequestAdd, ThesisRequestModify, ThesisRequestDelete

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

class ThesisRequestFormModify(ThesisFormBase):
    class Meta(ThesisForm.Meta): 
        model = ThesisRequestModify

class ThesisRequestFormDelete(ThesisFormBase):
    class Meta(ThesisForm.Meta): 
        model = ThesisRequestDelete

