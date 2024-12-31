from django import forms
from .models import Entry, Example
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['example_text']

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description']
    
    # Add examples field dynamically in the formset
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a field for examples
        self.fields['examples'] = forms.CharField(
            widget=forms.Textarea(attrs={'placeholder': 'Example text...'}), 
            required=False
        )

"""
class UserCreationFormMail(UserCreationForm):
    #mail = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        #user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

"""

class UserCreationFormMail(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')  # Include the email field

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # Include the email field in the Meta fields

    def save(self, commit=True):
        # Call the parent class's save method to get the user instance
        user = super(UserCreationFormMail, self).save(commit=False)
        # Assign the email from the cleaned data to the user instance
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()  # Save the user instance to the database
        return user
