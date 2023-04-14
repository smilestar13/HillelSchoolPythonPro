from django.urls import path

from feedbacks.views import FeedbacksView, FeedbacksList

urlpatterns = [
    path('create/', FeedbacksView.as_view(), name='feedback_create'),
    path('', FeedbacksList.as_view(), name='feedbacks')

]
