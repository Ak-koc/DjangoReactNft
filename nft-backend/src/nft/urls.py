from django.urls import re_path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    re_path(r'^user/registration$', views.user_registration),
    re_path(r'^user/login$', views.CustomTokenObtainPairView.as_view()),
    re_path(r'^artwork/list$', views.list_artworks),
    re_path(r'^artwork/detail$', views.artwork_detail),
]
