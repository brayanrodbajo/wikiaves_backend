from django.conf.urls import url
from django.urls import path, include
from allauth.account.views import confirm_email


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
]

urlpatterns = format_suffix_patterns(urlpatterns)
