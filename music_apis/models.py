from django.db import models
import uuid

class Artist(models.Model):
    """
    Model representing an artist.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Album(models.Model):
    """
    Model representing an album, associated with an Artist.
    """
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} by {self.artist.name}'

class Track(models.Model):
    """
    Model representing a track, associated with an Album.
    """
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.album.name})'

class Playlist(models.Model):
    """
    Model representing a playlist, containing PlaylistTracks.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PlaylistTrack(models.Model):
    """
    Model representing a track within a playlist, with a specific order.
    """
    playlist = models.ForeignKey(Playlist, related_name='playlist_tracks', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['playlist', 'track', 'order']

    def __str__(self):
        return f'{self.track.name} - Order {self.order} in {self.playlist.name}'
