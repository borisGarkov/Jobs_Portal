from django.contrib import messages
from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, FormView

from jobs_portal.jobs.models import WORK_CATEGORIES, WORK_TYPE

from jobs_portal.jobs.models import JobModel
from jobs_portal.main.forms import ContactForm
from jobs_portal.jobs.forms import JobFilterForm

UserModel = get_user_model()


class HomeView(ListView):
    model = JobModel
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobFilterForm()
        return context


class JobsPageBaseView(ListView):
    model = JobModel
    template_name = 'all_jobs_pages/show-all-jobs-template.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if len(self.request.GET) > 0:
            form = JobFilterForm(data={
                'work_category': self.request.GET['work_category'],
                'work_type': self.request.GET['work_type'],
            })
        else:
            form = JobFilterForm()

        context['form'] = form
        context['jobs'] = sorted(context['jobs'], key=lambda job: -job.user.usersubscriptionplan.subscription_plan_id)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        if len(self.request.GET) > 0:
            work_categories = [tuple_[0] for tuple_ in WORK_CATEGORIES]
            work_types = [tuple_[0] for tuple_ in WORK_TYPE]

            selected_work_category = self.request.GET['work_category']
            selected_work_type = self.request.GET['work_type']

            return qs.filter(
                work_type__in=work_types if selected_work_type in ['Покажи всички', ''] else [selected_work_type],
                work_category__in=work_categories if selected_work_category in ['Покажи всички',
                                                                                ''] else [selected_work_category],
                is_validated=True,
            )

        return qs.filter(is_validated=True, )


class ContactsView(FormView):
    form_class = ContactForm
    template_name = 'contacts.html'

    def form_valid(self, form):
        email_subject = "Website Inquiry"

        message = render_to_string('messages/website_question_form.html', {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email_address'],
            'message': form.cleaned_data['message'],
        })

        email = EmailMessage(
            subject=email_subject,
            body=message,
            to=['rentahandbg@gmail.com'],
            cc=['boris.garkov@abv.bg'],
        )

        email.send()
        messages.info(self.request, 'Благодарим Ви за имейла!')
        return HttpResponseRedirect(reverse('contacts'))


class BusinessClientsView(FormView):
    form_class = ContactForm
    template_name = 'business-clients.html'

    def form_valid(self, form):
        email_subject = "Website Inquiry"

        message = render_to_string('messages/website_question_form.html', {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email_address'],
            'message': form.cleaned_data['message'],
        })

        email = EmailMessage(
            subject=email_subject,
            body=message,
            to=['rentahandbg@gmail.com'],
            cc=['boris.garkov@abv.bg'],
        )

        email.send()
        messages.info(self.request, 'Благодарим Ви за имейла!')
        return HttpResponseRedirect(reverse('contacts'))


def search(request):
    if request.method == 'POST':
        searched_text = request.POST['searched'].lower().strip()
        if not searched_text == '':
            in_title = JobModel.objects.filter(
                title__icontains=searched_text,
            )
            in_description = JobModel.objects.filter(
                description__icontains=searched_text,
            )
            in_city = JobModel.objects.filter(
                city__icontains=searched_text,
            )

            result = set(in_title | in_description | in_city)
        else:
            searched_text = ''
            result = ''
    else:
        searched_text = ''
        result = ''

    context = {
        'searched_text': searched_text,
        'jobs': result
    }

    return render(request, 'search-page.html', context)


class FooterView(ListView):
    model = JobModel
    template_name = 'shared/footer.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobModel.objects.count()
