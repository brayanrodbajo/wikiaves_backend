from django.conf.urls import url
from django.urls import path, include
from allauth.account.views import confirm_email


from birds import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.Birds.as_view()),
    path('<int:pk>', views.SingleBird.as_view()),
    path('orders', views.Orders.as_view()),
    path('images', views.Images.as_view()),
    path('bird_images', views.BirdImages.as_view()),
    path('bird_images/<int:pk>', views.SingleBirdImage.as_view()),
    path('videos', views.Videos.as_view()),
    path('videos/<int:pk>', views.SingleVideo.as_view()),
    path('audios', views.Audios.as_view()),
    path('audios/<int:pk>', views.SingleAudio.as_view()),
    path('orders/<int:pk>', views.SingleOrder.as_view()),
    path('families', views.Families.as_view()),
    path('families/<int:pk>', views.SingleFamily.as_view()),
    path('authors', views.Authors.as_view()),
    path('authors/<int:pk>', views.SingleAuthor.as_view()),
    path('get_names', views.get_names),
]

urlpatterns = format_suffix_patterns(urlpatterns)
