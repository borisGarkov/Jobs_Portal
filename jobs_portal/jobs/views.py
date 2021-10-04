from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django.contrib import messages

from jobs_portal.jobs.forms import JobForm, UpdateJobForm, JobApplicationForm, JobConnectWithJobPoster
from jobs_portal.jobs.models import JobModel, Comments

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class CreateJob(CreateView):
    model = JobModel
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('home')
    form_class = JobForm

    def form_valid(self, form):
        if self.request.user.jobmodel_set.count() + 1 \
                <= self.request.user.usersubscriptionplan.subscription_plan.max_job_posts:
            job = form.save(commit=False)
            job.user = self.request.user
            job.save()
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Достигнахте лимита на обяви, които можете да споделите!')
            return HttpResponseRedirect(reverse('profile', args=[self.request.user.pk]))


@method_decorator(login_required, name='dispatch')
class UpdateJob(UpdateView):
    model = JobModel
    template_name = 'jobs/update_job.html'
    form_class = UpdateJobForm

    def get_success_url(self, **kwargs):
        return reverse("details job", kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class DeleteJob(DeleteView):
    model = JobModel
    success_url = reverse_lazy('home')
    template_name = 'jobs/delete_job.html'


class JobDetails(DetailView):
    model = JobModel
    template_name = 'jobs/job_details.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_job = get_object_or_404(JobModel, id=self.kwargs['pk'])
        current_user = get_object_or_404(UserModel, id=current_job.user.id)
        is_liked = False

        try:
            if current_job.likes.filter(pk=self.request.user.profilemodel.pk).exists():
                is_liked = True
        except Exception:
            pass

        context['total_likes'] = self.request.POST.get('total_likes')
        context['is_liked'] = is_liked
        context['current_user'] = current_user
        return context


def like_job_post(request, pk):
    current_post = get_object_or_404(JobModel, pk=pk)

    if current_post.likes.filter(pk=request.user.profilemodel.pk).exists():
        current_post.likes.remove(request.user.profilemodel)
    else:
        current_post.likes.add(request.user.profilemodel)

    return HttpResponseRedirect(reverse('details job', args=[str(pk)]))


def post_comment(request, pk):
    try:
        current_post = get_object_or_404(JobModel, pk=pk)
        current_comment = request.POST['comment']
        current_user = request.user

        if current_comment.strip() == '':
            return HttpResponseRedirect(reverse('details job', args=[str(pk)]))

        current_post.comments_set.create(
            job=current_post,
            comment=current_comment,
            user=current_user,
        )
    except Exception:
        raise ValidationError('Невалиден коментар..')

    return HttpResponseRedirect(reverse('details job', args=[str(pk)]))


def delete_comment(request, pk):
    current_comment = Comments.objects.get(pk=pk)
    current_job = current_comment.job_id
    current_comment.delete()

    return HttpResponseRedirect(reverse('details job', args=[str(current_job)]))


@method_decorator(login_required, name='dispatch')
class JobApplicationView(FormView):
    form_class = JobApplicationForm
    template_name = 'jobs/job_application_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        current_job = JobModel.objects.get(pk=self.kwargs['pk'])

        job_creator_email = current_job.user.email
        job_creator_username = current_job.user.username

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email_address = form.cleaned_data['email_address']
        cv_file = form.cleaned_data['cv_file']
        phone_number = form.cleaned_data['telephone']

        phone_number = f'0{phone_number}' if ~str(phone_number).startswith('0') else phone_number

        mail_subject = 'Кандидатура за ваша обява'

        message = render_to_string('jobs/send_job_application_email.html', {
            'job_creator_username': job_creator_username,
            'title': current_job.title,
            'first_name': first_name,
            'last_name': last_name,
            'email': email_address,
            'phone_number': phone_number,
            'cv_file': True if cv_file else False,
        })

        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=email_address,
            to=[job_creator_email],
            bcc=['rentahandbg@gmail.com'],
        )

        if cv_file:
            email.attach(cv_file.name, cv_file.read(), cv_file.content_type)

        email.send()

        messages.success(self.request, 'Успешно кандидатствахте за тази позиция!')
        return HttpResponseRedirect(reverse('home'))


@method_decorator(login_required, name='dispatch')
class JobConnectWithJobPosterView(FormView):
    form_class = JobConnectWithJobPoster
    template_name = 'jobs/job_connect_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        current_job = JobModel.objects.get(pk=self.kwargs['pk'])

        job_creator_email = current_job.user.email
        job_creator_username = current_job.user.username

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email_address = form.cleaned_data['email_address']
        text_message = form.cleaned_data['text_message']
        phone_number = form.cleaned_data['telephone']

        phone_number = f'0{phone_number}' if ~str(phone_number).startswith('0') else phone_number

        mail_subject = 'Изпратено запитване за ваша обява'

        message = render_to_string('jobs/send_job_connect_email.html', {
            'job_creator_username': job_creator_username,
            'title': current_job.title,
            'first_name': first_name,
            'last_name': last_name,
            'email': email_address,
            'phone_number': phone_number,
            'text_message': text_message,
        })

        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=email_address,
            to=[job_creator_email],
            bcc=['rentahandbg@gmail.com'],
        )

        email.send()

        messages.success(self.request, 'Успешно изпратихте запитване за тази позиция!')
        return HttpResponseRedirect(reverse('home'))
