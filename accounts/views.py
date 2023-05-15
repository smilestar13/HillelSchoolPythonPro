from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.views import View

from accounts.model_forms import RegistrationForm, AuthenticationForm, UserProfileForm


class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _('Welcome in our Family!'))
        return super().form_valid(form)


class LoginView(AuthLoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, _('Welcome back!'))
        return super().form_valid(form)


class ProfileView(View):
    template_name = 'registration/profile.html'

    def get(self, request):
        user = request.user
        form = UserProfileForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})