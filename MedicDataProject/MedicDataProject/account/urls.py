from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('patient/', views.patient, name='patient'),
    path('doctor/', views.doctor, name='doctor'),
    path('logout/', views.logoutUser, name="logout"),
    path('expedienteg/', views.editorg, name="expedienteg"),
    path('delete_expedienteg/<int:expgid>/', views.delete_expedienteg, name='delete_expedienteg'),
]