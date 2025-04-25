from django import forms
from .models import Course, Subject, Topic, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['course', 'name']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'name']

# Registration Form
class UserRegistrationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False, label="Register as Admin")

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_admin']

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
