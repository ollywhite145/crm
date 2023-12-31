from django.urls import path
from django.contrib.auth import views as auth_views 

from . import views

#

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('tours/', views.tours, name="tours"),

    path('', views.home, name="home"),

    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),  # adding the <> makes the url dynamic
    path('create_order/<str:pk>', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('reset_password',
          auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
           name="reset_password"),  #submit email form
    
    path('reset_password_sent',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),  #email sent success message
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_form"),  #link to password rest form in email

    path('reset_password_complete', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"), #password successfully changed message
]


