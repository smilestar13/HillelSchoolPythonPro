from django.urls import path

from feedbacks.views import FeedbacksView

urlpatterns = [
    path('', FeedbacksView.as_view(), name='feedbacks')
]
