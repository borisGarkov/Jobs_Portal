from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.shortcuts import redirect

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView

from jobs_portal.job_auth.forms import RegisterForm, SignInForm, PasswordResetFormCustom, SetPasswordFormCustom, \
    ChangeUsernameEmailForm

UserModel = get_user_model()


class RegisterUser(FormView):
    form_class = RegisterForm
    template_name = 'profile/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активирайте акаунта си.'

        message = render_to_string('profile/account_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        to_email = form.cleaned_data.get('email')

        email = EmailMessage(
            subject=mail_subject,
            body=message,
            to=[to_email],
            bcc=['rentahandbg@gmail.com', 'boris.garkov@abv.bg'],
        )

        email.send()

        messages.success(self.request, 'Моля затворете тази страница и активирайте акаунта през имейла си!')
        return HttpResponseRedirect(reverse('home'))


class UpdateEmailUsernamePage(UpdateView):
    model = UserModel
    form_class = ChangeUsernameEmailForm
    template_name = 'profile/update_email_username.html'

    def get_success_url(self, **kwargs):
        return reverse("profile", kwargs={'pk': self.object.pk})


class LoginUser(LoginView):
    form_class = SignInForm
    template_name = 'profile/login.html'
    success_url = reverse_lazy('profile')


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Благодаря за потвърждението! Сега можете да влезете в акаунта си!')
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Активационният линк е невалиден!')


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    form_class = SetPasswordFormCustom


class PasswordResetRequest(FormView):
    form_class = PasswordResetFormCustom
    template_name = 'profile/password_reset.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        associated_user = UserModel.objects.filter(email=user_email)
        current_site = get_current_site(self.request)

        if associated_user.exists():
            user = associated_user[0]
            email_subject = "Password Reset Requested"
            email_template_name = "profile/password_reset_email.html"

            message = render_to_string(email_template_name, {
                "email": user.email,
                'domain': current_site.domain,
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            })

            email = EmailMessage(
                subject=email_subject,
                body=message,
                to=[user.email],
                bcc=['rentahandbg@gmail.com'],
            )

            email.send()

            return redirect('password_reset_done')
        else:
            messages.warning(self.request, 'Потребител с този имейл не съществува!')
            return HttpResponseRedirect(reverse('password_reset'))
