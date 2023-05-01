from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, RedirectView

from wishes.forms import WishesForm, WishActionForm
from wishes.mixins import GetCurrentWishMixin


class WishView(GetCurrentWishMixin, FormView):
    form_class = WishesForm
    template_name = 'wishlist/index.html'
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('favourites')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wish = self.get_object()
        context.update({
            'wish': wish,
            'wish_items': wish.wish_list_items.all()
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.get_object()})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WishActionView(GetCurrentWishMixin, RedirectView):
    url = reverse_lazy('products')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = WishActionForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.action(kwargs.get('action'))
        return self.get(request, *args, **kwargs)
