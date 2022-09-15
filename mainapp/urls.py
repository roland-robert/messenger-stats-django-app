from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('personal_stats/', views.personal_stats_view, name='personal_stats'),
    path('progress', views.progress_view, name='progress'),
    path('progress_versus', views.progress_versus_view, name='progress_versus'),
    path('feedback', views.feedback_view, name='feedback'),
    path('best_message', views.best_message_view, name='best_message')
]
