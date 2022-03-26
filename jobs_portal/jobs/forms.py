from django import forms
from django.core.validators import MinLengthValidator
from .models import WORK_CATEGORIES, WORK_TYPE

from utils.forms import BootstrapFormMixin
from jobs_portal.jobs.models import JobModel


class JobForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('user', 'likes', 'last_modified')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Позиция'}),
            'description': forms.Textarea(attrs={'rows': 5,
                                                 'placeholder': 'Описание на работата'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Очаквана заплата'}),
        }

        labels = {
            'image': 'Снимка на дейност / фирма',
            'title': 'Позиция',
            'description': 'Описание на позиция',
            'city': 'Град',
            'salary': 'Заплата',
            'salary_type': 'Вид заплата',
            'work_category': 'Категория',
            'work_type': 'Тип Работа',
        }


class UpdateJobForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('user', 'likes', 'last_modified')

        labels = {
            'image': 'Снимка на дейност / фирма',
            'title': 'Позиция',
            'description': 'Описание на позиция',
            'city': 'Град',
            'salary': 'Заплата',
            'salary_type': 'Вид заплата',
            'work_category': 'Категория',
        }


class JobBaseForm(BootstrapFormMixin, forms.Form):
    first_name = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
        widget=forms.TextInput(attrs={'placeholder': 'Име'}),
        label='Име'
    )
    last_name = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        label='Фамилия'
    )
    email_address = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'placeholder': 'Имейл'}),
        label='Имейл адрес'
    )
    telephone = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Телефонен номер'}),
        label='Телефонен номер',
    )


class JobApplicationForm(JobBaseForm):
    cv_file = forms.FileField(
        widget=forms.FileInput(attrs={'label': 'CV', 'placeholder': 'CV'}),
        label='CV',
        required=False,
    )


class JobConnectWithJobPoster(JobBaseForm):
    text_message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Съобщение'}),
        label='Съобщение',
        required=False,
    )


class JobFilterForm(forms.Form):
    show_all_list = [('Покажи всички', 'Покажи всички')]

    WORK_CATEGORIES = show_all_list + WORK_CATEGORIES
    WORK_TYPE = show_all_list + WORK_TYPE

    work_category = forms.CharField(
        label='Категория',
        widget=forms.Select(
            choices=WORK_CATEGORIES,
        ),
    )
    work_type = forms.CharField(
        label='Тип обява',
        widget=forms.Select(choices=WORK_TYPE)
    )
