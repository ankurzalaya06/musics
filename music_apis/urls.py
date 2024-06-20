from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import ArtistViewSet, AlbumViewSet, TrackViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'playlists', PlaylistViewSet)


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('api/', include(router.urls)),
   
]

