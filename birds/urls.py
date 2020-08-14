from django.conf.urls import url
from django.urls import path, include
from allauth.account.views import confirm_email


from birds import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.Birds.as_view()),
    path('<int:pk>', views.SingleBird.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
