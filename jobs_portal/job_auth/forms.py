from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from utils.forms import BootstrapFormMixin

UserModel = get_user_model()


class SignInForm(BootstrapFormMixin, AuthenticationForm):
    class Meta:
        model = UserModel
        fields = '__all__'

        labels = {
            'email': 'Имейл',
            'password1': 'Парола',
        }


class ChangeUsernameEmailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

        labels = {
            'email': 'Имейл',
            'username': 'Потребителско Име',
        }


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=("Парола"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Потвърди Парола"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = UserModel
        fields = ('email', 'username')

        labels = {
            'email': 'Имейл',
            'username': 'Потребителско Име',
        }


class PasswordResetFormCustom(BootstrapFormMixin, PasswordResetForm):
    pass


class SetPasswordFormCustom(BootstrapFormMixin, SetPasswordForm):
    pass
