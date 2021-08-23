from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField

from utils.forms import BootstrapFormMixin
from jobs_portal.profiles.models import ProfileModel


class ProfileEditForm(BootstrapFormMixin, UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=("Парола"),
        help_text=(
            'Моля натиснете върху линка отдолу, за да промените паролата си. '
            '<a href="{}">Промени Парола</a>.'
        ),
    )

    class Meta:
        model = ProfileModel
        exclude = ('user',)

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Име'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'profession': forms.TextInput(attrs={'placeholder': 'Професия'}),
            'website_url': forms.TextInput(attrs={'placeholder': 'Линк към личен уебсайт'}),
            'facebook_url': forms.TextInput(attrs={'placeholder': 'Фейсбук линк'}),
            'instagram_url': forms.TextInput(attrs={'placeholder': 'Инстаграм линк'}),
            'twitter_url': forms.TextInput(attrs={'placeholder': 'Туитър линк'}),
        }

        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'profession': 'Професия',
            'profile_photo': 'Профилна Снимка',
            'website_url': 'Линк към личен уебсайт',
            'facebook_url': 'Фейсбук линк',
            'instagram_url': 'Инстаграм линк',
            'twitter_url': 'Туитър линк',
        }


class CustomPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'

    old_password = forms.CharField(
        label=("Предишна парола"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    error_messages = {
        'password_mismatch': ('Има разлика в двете пароли, които въведохте.'),
    }
    new_password1 = forms.CharField(
        label=("Нова Парола"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Потвърдете Новата Парола"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ('user',)
