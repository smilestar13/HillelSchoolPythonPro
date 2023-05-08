from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView

from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback
from project.model_choices import FeedbackCacheKeys


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

    def get_queryset(self):
        queryset = cache.get(FeedbackCacheKeys.FEEDBACKS)
        if not queryset:
            print('TO CACHE')
            queryset = Feedback.objects.all()
            cache.set(FeedbackCacheKeys.FEEDBACKS, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset
