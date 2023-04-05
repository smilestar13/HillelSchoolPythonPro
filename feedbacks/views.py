from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    form = FeedbackModelForm(user=user)
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'feedbacks/feedbacks.html', context={
        'feedbacks': Feedback.objects.iterator(),
        'form': form
    })
