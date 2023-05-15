from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.views import View
import random
import string
import time

from accounts.model_forms import RegistrationForm, AuthenticationForm


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user': user})


class UpdatePhoneView(View):
    template_name = 'registration/update_phone.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        confirmation_code = cache.get('confirmation_code')
        current_time = int(time.time())

        if not confirmation_code or \
                (current_time - cache.get('code_generated_time', 0)) >= 60:
            confirmation_code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=6))
            cache.set('confirmation_code', confirmation_code, 60)
            cache.set('code_generated_time', current_time, 60)

        context = {
            'confirmation_code': confirmation_code
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        confirmation_code = cache.get('confirmation_code')

        if code == confirmation_code:
            user.phone = phone
            user.save()
            return redirect('profile')
        else:
            cache.delete('confirmation_code')
            cache.delete('code_generated_time')
            context = {
                'confirmation_code': confirmation_code,
                'error_message': 'Invalid confirmation code. Please try again.'
            }
            return render(request, self.template_name, context)
