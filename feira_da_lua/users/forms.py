from django import forms

class UserRegistrationForm(forms.Form):
     email = forms.EmailField(max_length=255, required=True)
     username = forms.CharField(max_length=150, required=True)
     complete_name = forms.CharField(max_length=255, required=True)
     password = forms.CharField(widget=forms.PasswordInput, max_length=128, required=True)

class UserLoginForm(forms.Form):
     email = forms.EmailField(max_length=255, required=True)
     password = forms.CharField(widget=forms.PasswordInput, max_length=128, required=True)

class MarketerRegistrationForm(forms.Form):
     email = forms.EmailField(max_length=255, required=True)
     username = forms.CharField(max_length=150, required=True)
     complete_name = forms.CharField(max_length=255, required=True)
     password = forms.CharField(widget=forms.PasswordInput, max_length=128, required=True)
     cellphone = forms.CharField(max_length=20, required=True)

class AvaliationForm(forms.Form):
     marketplace_id = forms.IntegerField(required=True)
     grade = forms.IntegerField(min_value=1, max_value=5, required=True)
     comment = forms.CharField(widget=forms.Textarea, required=False)