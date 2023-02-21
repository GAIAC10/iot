from django.urls import path
from . import views

urlpatterns = [
    path('sms', views.sms_view),
    path('<str:username>', views.UsersViews.as_view()),
    path('<str:username>/avatar', views.users_views),
    path('<str:username>/password', views.change_passwords),
]