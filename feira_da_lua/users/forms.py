from django import forms

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '********',
            'id': 'password-field'
        })
    )

class UserRegistrationForm(forms.Form):
    complete_name = forms.CharField(
        max_length=255,
        required=True,
        label='Nome Completo',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Fulano de Tal'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nome de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'fulano123'
        })
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '********',
            'id': 'password-field'
        })
    )

class MarketerRegistrationForm(forms.Form):
    complete_name = forms.CharField(
        max_length=255,
        required=True,
        label='Nome Completo',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Fulano de Tal'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nome de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'fulano123'
        })
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '********',
            'id': 'password-field'
        })
    )
    cellphone = forms.CharField(
        max_length=20,
        required=True,
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '(99) 99999-9999'
        })
    )

class AvaliationForm(forms.Form):
     marketplace_id = forms.IntegerField(required=True)
     grade = forms.IntegerField(min_value=1, max_value=5, required=True)
     comment = forms.CharField(widget=forms.Textarea, required=False)