from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            "class": "form-control rounded-3",
            "placeholder": "Enter your email",
            "autocomplete": "email"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control rounded-3",
            "placeholder": "Choose a username",
            "autocomplete": "username"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control rounded-3",
            "placeholder": "Create a password",
            "autocomplete": "new-password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control rounded-3",
            "placeholder": "Confirm your password",
            "autocomplete": "new-password"
        })

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username