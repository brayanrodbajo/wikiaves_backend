from django.conf.urls import url
from django.urls import path, include, reverse_lazy
from allauth.account.views import confirm_email
from django.contrib.auth import views as auth_views


from users import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'custom/login/', views.CustomLoginView.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account', include('allauth.urls')),
    url('assign-bird', views.BirdEditorView.as_view()),
    path('', views.Users.as_view()),
    path('<int:pk>', views.SingleUser.as_view()),
    path('get_token_status', views.get_token_status),
    path(
        'password-reset/<uidb64>/<token>/',
        views.PasswordTokenCheckView.as_view(),
        name='password-reset-confirm'
    ),
    path(
        'password-reset/',
        views.PasswordResetView.as_view(),
        name='reset_password'
    ),
    path('password-reset-done/', views.SetNewPasswordView.as_view(),
         name="password-reset-done"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
