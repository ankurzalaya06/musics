from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Artist, Album, Track, Playlist
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, PlaylistSerializer
from django.shortcuts import render


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    # breakpoint()
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


def mainpaige(request):
    return render(request, 'home.html')