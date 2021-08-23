from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView

from jobs_portal.jobs.models import JobModel
from jobs_portal.profiles.forms import ProfileEditForm, CustomPasswordChangeForm
from jobs_portal.profiles.models import ProfileModel

UserModel = get_user_model()


class ShowProfilePage(DetailView):
    model = UserModel
    template_name = 'profile/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePage, self).get_context_data(**kwargs)
        user = UserModel.objects.get(pk=self.kwargs['pk'])
        profile_jobs = JobModel.objects.filter(user_id=user.id).order_by('-id')

        context['profile'] = user
        context['page_user'] = user.profilemodel
        context['jobs'] = profile_jobs
        return context


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
