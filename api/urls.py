from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


# router = routers.DefaultRouter()
# router.register(r'blogs', views.BlogViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
