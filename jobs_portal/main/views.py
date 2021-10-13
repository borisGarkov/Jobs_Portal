from django.contrib import messages
from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, FormView, TemplateView

from jobs_portal.jobs.models import JobModel
from jobs_portal.main.forms import ContactForm

UserModel = get_user_model()


class HomeView(ListView):
    model = JobModel
    template_name = 'home.html'

    # context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['looking_for_people_jobs'] = [job for job in JobModel.objects.order_by('-id') if
                                              job.work_type == 'Търся Хора'][:4]
        context['offer_jobs'] = [job for job in JobModel.objects.order_by('-id') if
                                 job.work_type == 'Предлагам Услуга'][:4]
        return context


class AllJobsView(TemplateView):
    template_name = 'all_jobs_pages/all-jobs-page.html'


class JobsPageBaseView(ListView):
    model = JobModel
    template_name = ''
    context_object_name = 'jobs'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [cat[0] for cat in JobModel.WORK_CATEGORIES]
        context['jobs'] = sorted(context['jobs'], key=lambda job: -job.user.usersubscriptionplan.subscription_plan_id)
        return context


class LookingForJobsView(JobsPageBaseView):
    model = JobModel
    template_name = 'all_jobs_pages/show-all-jobs-template.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = JobModel.objects.filter(work_type='Търся Хора')
        return qs


class OfferJobsView(JobsPageBaseView):
    template_name = 'all_jobs_pages/show-all-jobs-template.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = JobModel.objects.filter(work_type='Предлагам Услуга')
        return qs


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
        'result': result
    }

    return render(request, 'search-page.html', context)


class FooterView(ListView):
    model = JobModel
    template_name = 'shared/footer.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobModel.objects.count()
