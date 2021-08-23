from django import forms
from django.core.validators import MinLengthValidator

from utils.forms import BootstrapFormMixin


class ContactForm(BootstrapFormMixin, forms.Form):
    first_name = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
        widget=forms.TextInput(attrs={'label': 'Съобщение', 'placeholder': 'Име'}),
    )
    last_name = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
        widget=forms.TextInput(attrs={'label': 'Съобщение', 'placeholder': 'Фамилия'}),
    )
    email_address = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'label': 'Съобщение', 'placeholder': 'Имейл'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'label': 'Съобщение', 'placeholder': 'Съобщение'}),
        max_length=2000,
    )
