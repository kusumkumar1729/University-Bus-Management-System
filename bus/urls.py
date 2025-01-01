from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('routes/',views.routes,name = 'routes'),
    path('login/', views.login, name='login'),
    path('vacancy/',views.vacancy,name='vacancy'),
    path('apply/', views.apply, name='apply'),
    path('BusInfo/',views.busInfo,name='Info'),
    path('remarks/',views.feedback,name='Remarks'),
    path('contact/', views.contact, name='contact'),
    path('studentPage/<str:student_id>/',views.studentPage,name='studentPage'),
    path('logout/', views.logout_view, name='logout'),
    path('withdrawl/', views.withdrawl, name='withdrawl'),
    path('checkout/<str:student_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<str:student_id>/', views.payment_success, name='payment_success'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),
]


