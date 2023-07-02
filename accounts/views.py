from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, RedirectView
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.http import urlsafe_base64_decode
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
import random
import string
import time

from accounts.model_forms import RegistrationForm, AuthenticationForm

User = get_user_model()


class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')
    email_template_name = "registration/registration_email.html"
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    token_generator = default_token_generator

    def form_valid(self, form):
        messages.success(self.request,
                         _('We will send email with registration link. '
                           'Please follow link and continue your '
                           'registration flow.'))
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
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


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )
        self.user = self.get_user(kwargs["uidb64"])
        if self.user is None:
            raise Http404
        if not default_token_generator.check_token(self.user, kwargs["token"]):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user

    def get(self, request, *args, **kwargs):
        self.user.is_active = True
        self.user.save()
        return super().get(request, *args, **kwargs)
