from django import forms
from .models import UserProfile, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class CombinedProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ["department", "manager"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["manager"].queryset = UserProfile.objects.exclude(id=user.id)

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return super().save(commit=commit)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "reviewee_strengths_text",
            "reviewee_improvements_text",
            "reviewee_growth_rating",
            "reviewee_execution_rating",
            "reviewee_collaboration_rating",
        ]

        widgets = {
            "reviewee_strengths_text": forms.Textarea(attrs={"rows": 3, "cols": 50}),
            "reviewee_improvements_text": forms.Textarea(attrs={"rows": 3, "cols": 50}),
        }

        labels = {
            "reviewee_strengths_text": "Strengths",
            "reviewee_improvements_text": "Improvements",
            "reviewee_growth_rating": "Work hard to grow",
            "reviewee_execution_rating": "Disrupt & Execute",
            "reviewee_collaboration_rating": "Collaborate",
        }
