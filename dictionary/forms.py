from django import forms
from .models import Entry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description']

class UserCreationFormMail(UserCreationForm):
    mail = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
