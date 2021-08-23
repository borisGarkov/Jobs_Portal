from django.contrib.auth import get_user_model

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, FormView, TemplateView

from jobs_portal.jobs.models import JobModel
from jobs_portal.main.forms import ContactForm

UserModel = get_user_model()


class HomeView(ListView):
    model = JobModel
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobModel.objects.order_by('-id')[:4]


class AllJobsPageView(ListView):
    model = JobModel
    template_name = 'all-jobs-page.html'
    context_object_name = 'jobs'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [cat[0] for cat in JobModel.WORK_CATEGORIES]
        return context


class ContactsView(FormView):
    form_class = ContactForm
    template_name = 'contacts.html'

    def form_valid(self, form):
        subject = "Website Inquiry"
        body = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email_address'],
            'message': form.cleaned_data['message'],
        }
        message = "\n".join(body.values())

        try:
            send_mail(subject, message, from_email=form.cleaned_data['email_address'],
                      recipient_list=['boris.garkov@abv.bg', 'rentahandbg@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('contacts')


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


class PricingListView(TemplateView):
    template_name = 'pricing-list.html'
