from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView

from jobs_portal.jobs.models import JobModel
from jobs_portal.payments.models import UserSubscriptionPlan, Payments
from jobs_portal.profiles.forms import ProfileEditForm, CustomPasswordChangeForm
from jobs_portal.profiles.models import ProfileModel

import stripe

from datetime import datetime

from utils.find_stripe_info import find_stripe_customer

stripe.api_key = settings.STRIPE_SECRET_KEY

UserModel = get_user_model()


class ShowProfilePage(DetailView):
    model = UserModel
    template_name = 'profile/profile.html'

    def get_context_data(self, *args, **kwargs):
        SUBSCRIPTION_PLAN = {
            1: 'Безплатен',
            2: 'Стандартен',
            3: 'Премиум',
            6: 'Ейй най-големия си ей!',
        }

        context = super(ShowProfilePage, self).get_context_data(**kwargs)
        user = UserModel.objects.get(pk=self.kwargs['pk'])
        profile_jobs = JobModel.objects.filter(user_id=user.id).order_by('-id')
        user_subscription_plan = UserSubscriptionPlan.objects.get(user=self.kwargs['pk']).subscription_plan_id
        subscription_plan = SUBSCRIPTION_PLAN.get(user_subscription_plan)

        current_customer_id = find_stripe_customer(current_user_email=user.email)

        if current_customer_id != '':
            next_invoice = stripe.Invoice.upcoming(
                customer=current_customer_id,
            )['period_end']

            next_invoice_date = datetime.fromtimestamp(next_invoice).strftime('%d %B %Y')
        else:
            next_invoice_date = ''

        context['profile'] = user
        context['page_user'] = user.profilemodel
        context['jobs'] = profile_jobs
        context['subscription_plan'] = subscription_plan
        context['is_subscription_plan_paid'] = True if current_customer_id else False
        context['next_invoice_date'] = next_invoice_date
        return context


@method_decorator(login_required, name='dispatch')
class UpdateProfilePage(UpdateView):
    form_class = ProfileEditForm
    model = ProfileModel
    template_name = 'profile/update_profile.html'

    def get_success_url(self, **kwargs):
        return reverse("profile", kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class DeleteProfile(DeleteView):
    model = UserModel
    success_url = reverse_lazy('home')
    template_name = 'profile/delete-profile.html'


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'profile/password-change.html'

    def get_success_url(self, **kwargs):
        return reverse("profile", kwargs={'pk': self.request.user.pk})
