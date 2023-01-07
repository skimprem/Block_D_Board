from django.urls import path, include
from adverts.views import AdvertList, AdvertDetail, AdvertCreate, feedback_list, FeedbackList, FeedbackCreate, feedback_delete, feedback_accept, feedback_reject

urlpatterns = [
    path('', AdvertList.as_view(), name='adverts'),
    path('<int:pk>/', AdvertDetail.as_view(), name='advert'),
    path('create/', AdvertCreate.as_view(), name='create'),
    path('feedbacks/', FeedbackList.as_view(), name='feedbacks'),
    path('<int:pk>/feedback/', FeedbackCreate.as_view(), name='feedback'),
    path('feedbacks/delete/', feedback_delete, name='delete'),
    path('feedbacks/accept/', feedback_accept, name='accept'),
    path('feedbacks/reject/', feedback_reject, name='reject'),
]
