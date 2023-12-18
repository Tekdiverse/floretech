from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import UserComplaints


PROBLEMS = (
    ("", "I have a problem with..."),
    ("Account", "Account"),
    ("Registering/Authorizing", "Registering/Authorizing"),
    ("Using Website", "Using Website"),
    ("Troubleshooting", "Troubleshooting"),
    ("Other", "Other"),
)



class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name","class": "form-control","id":"sppb-form-builder-field-1"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Account Email", "class": "form-control ","id":"sppb-form-builder-field-2"}))
    question = forms.ChoiceField(choices=PROBLEMS, widget=forms.Select(attrs={"placeholder": "This question is about..", "class": "form-control","id":"sppb-form-builder-field-0"}))
    question_details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',"id":"sppb-form-builder-field-3"}))
    
    class Meta:
        model = UserComplaints
        fields = ['name','email','question','question_details']


