from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView  # Проверить работает ли без .edit

from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback


class FeedbacksView(FormView):
    template_name = 'feedbacks/create.html'
    form_class = FeedbackModelForm
    success_url = '/feedbacks/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FeedbacksList(ListView):
    template_name = 'feedbacks/index.html'
    model = Feedback
