from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Artist, Album, Track, Playlist
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, PlaylistSerializer
from django.shortcuts import render


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for handling read-only operations on Artist objects.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for handling read-only operations on Album objects.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for handling read-only operations on Track objects.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Playlist objects.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a playlist instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """
        Perform the deletion of the playlist instance.
        """
        instance.delete()


def mainpage(request):
    """
    View function for rendering the main homepage.
    """
    return render(request, 'home.html')
