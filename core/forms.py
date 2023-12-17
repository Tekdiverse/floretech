from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import UserComplaints


PROBLEMS = (
    ("Account", "Account"),
    ("Registering/Authorizing", "Registering/Authorizing"),
    ("Using Website", "Using Website"),
    ("Troubleshooting", "Troubleshooting"),
    ("Other", "Other"),
)



class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "sppb-form-control","id":"sppb-form-builder-field-1"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Account Email", "class": "sppb-form-control","id":"sppb-form-builder-field-2"}))
    question = forms.ChoiceField(choices=PROBLEMS, widget=forms.Select(attrs={"placeholder": "This question is about..", "class": "sppb-form-control","id":"sppb-form-builder-field-0"}))
    question_details = forms.CharField(widget=forms.Textarea(attrs={"placeholder": 'I have a problem with...','class': 'sppb-form-control',"id":"sppb-form-builder-field-3"}))
    
    class Meta:
        model = UserComplaints
        fields = ['name','email','question','question_details']


