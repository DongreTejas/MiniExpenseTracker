from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
# Define your choices as a list of tuples
CHOICES = [
    ('Grocery', 'Grocery'),
    ('Food', 'Food'),
    ('Travel', 'Travel'),
    ('Utilities', 'Utilities'),
    ('Entertainment', 'Entertainment'),
    ('Other', 'Other'),
]

class MyForm(forms.Form):
    category = forms.ChoiceField(choices=CHOICES)
    cost =  forms.IntegerField(label="Amount Spent")
    description = forms.CharField(max_length = 100, label = "Description", required=False)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user_profile = UserProfile(user=user, email=self.cleaned_data['email'])
        if commit:
            user.save()
            user_profile.save()
        return user
