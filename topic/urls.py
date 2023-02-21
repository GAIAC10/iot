from django.urls import path
from . import views

urlpatterns = [
    path('<str:blog_delete_username>/<str:blog_delete_id>', views.TopicViews.as_view()),
    path('<str:author_id>',views.TopicViews.as_view())
]