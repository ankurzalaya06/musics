from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Artist, Album, Track, Playlist, PlaylistTrack
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer

class ArtistViewSetTestCase(TestCase):
    """
    Test case for testing ArtistViewSet functionalities.
    """

    def setUp(self):
        """
        Set up necessary data for each test.
        """
        self.client = APIClient()
        self.artist1 = Artist.objects.create(name='Artist 1')
        self.artist2 = Artist.objects.create(name='Artist 2')

    def test_list_artists(self):
        """
        Test retrieving a list of artists via API.
        """
        response = self.client.get('/api/artists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_artist(self):
        """
        Test retrieving a single artist via API.
        """
        response = self.client.get(f'/api/artists/{self.artist1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        artist = Artist.objects.get(id=self.artist1.id)
        serializer = ArtistSerializer(artist)
        self.assertEqual(response.data, serializer.data)

class AlbumViewSetTestCase(TestCase):
    """
    Test case for testing AlbumViewSet functionalities.
    """

    def setUp(self):
        """
        Set up necessary data for each test.
        """
        self.client = APIClient()
        self.artist = Artist.objects.create(name='Artist 1')
        self.album1 = Album.objects.create(name='Album 1', artist=self.artist)
        self.album2 = Album.objects.create(name='Album 2', artist=self.artist)

    def test_list_albums(self):
        """
        Test retrieving a list of albums via API.
        """
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_album(self):  
        """
        Test retrieving a single album via API.
        """
        response = self.client.get(f'/api/albums/{self.album1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        album = Album.objects.get(id=self.album1.id)
        serializer = AlbumSerializer(album)
        self.assertEqual(response.data, serializer.data)

class TrackViewSetTestCase(TestCase):
    """
    Test case for testing TrackViewSet functionalities.
    """

    def setUp(self):
        """
        Set up necessary data for each test.
        """
        self.client = APIClient()
        self.artist = Artist.objects.create(name='Artist 1')
        self.album = Album.objects.create(name='Album 1', artist=self.artist)
        self.track1 = Track.objects.create(name='Track 1', album=self.album)
        self.track2 = Track.objects.create(name='Track 2', album=self.album)

    def test_list_tracks(self):
        """
        Test retrieving a list of tracks via API.
        """
        response = self.client.get('/api/tracks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_track(self):
        """
        Test retrieving a single track via API.
        """
        response = self.client.get(f'/api/tracks/{self.track1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        track = Track.objects.get(id=self.track1.id)
        serializer = TrackSerializer(track)
        self.assertEqual(response.data, serializer.data)

class PlaylistViewSetTestCase(TestCase):
    """
    Test case for testing PlaylistViewSet functionalities.
    """

    def setUp(self):
        """
        Set up necessary data for each test.
        """
        self.client = APIClient()

        # Create an Artist
        self.artist = Artist.objects.create(name='Artist 1')

        # Create an Album for the Artist
        self.album = Album.objects.create(name='Album 1', artist=self.artist)

        # Create Tracks associated with the Album
        self.track1 = Track.objects.create(name='Track 1', album=self.album)
        self.track2 = Track.objects.create(name='Track 2', album=self.album)

        # Create Playlist instances
        self.playlist1 = Playlist.objects.create(name='Playlist 1')
        self.playlist2 = Playlist.objects.create(name='Playlist 2')

        # Create PlaylistTrack instances associating Tracks with Playlists
        self.playlist_track1 = PlaylistTrack.objects.create(playlist=self.playlist1, track=self.track1, order=1)
        self.playlist_track2 = PlaylistTrack.objects.create(playlist=self.playlist1, track=self.track2, order=2)

    def test_list_playlists(self):
        """
        Test retrieving a list of playlists via API.
        """
        response = self.client.get('/api/playlists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_playlist(self):
        """
        Test retrieving a single playlist via API.
        """
        response = self.client.get(f'/api/playlists/{self.playlist1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        playlist = Playlist.objects.get(id=self.playlist1.id)
        serializer = PlaylistSerializer(playlist)
        self.assertEqual(response.data, serializer.data)

    def test_create_playlist(self):
        """
        Test creating a new playlist via API.
        """
        data = {
            'name': 'New Playlist',
            'tracks': [
                {'track': self.track1.id, 'order': 1},
                {'track': self.track2.id, 'order': 2},
            ]
        }
        response = self.client.post('/api/playlists/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 3)  # Check if playlist was created
        new_playlist = Playlist.objects.get(name='New Playlist')
        self.assertEqual(new_playlist.playlist_tracks.count(), 2)  # Check if tracks were added to playlist

    def test_update_playlist(self):
        """
        Test updating an existing playlist via API.
        """
        data = {
            'name': 'Updated Playlist',
            'tracks': [
                {'track': self.track2.id, 'order': 1},  # Changed order of track2
                {'track': self.track1.id, 'order': 2},  # Changed order of track1
            ]
        }
        response = self.client.put(f'/api/playlists/{self.playlist1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_playlist = Playlist.objects.get(id=self.playlist1.id)
        self.assertEqual(updated_playlist.name, 'Updated Playlist')

        # Check if tracks were updated correctly
        updated_tracks = updated_playlist.playlist_tracks.all().order_by('order')
        self.assertEqual(updated_tracks[0].track_id, self.track2.id)
        self.assertEqual(updated_tracks[1].track_id, self.track1.id)

    def test_delete_playlist(self):
        """
        Test deleting an existing playlist via API.
        """
        response = self.client.delete(f'/api/playlists/{self.playlist1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Playlist.objects.filter(id=self.playlist1.id).exists())
