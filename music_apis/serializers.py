from rest_framework import serializers
from .models import Artist, Album, Track, Playlist, PlaylistTrack
from django.db.models import F



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class PlaylistTrackSerializer(serializers.ModelSerializer):
    track_name = serializers.CharField(source="track.name", read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ['track', 'order', 'track_name']

class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(source='playlist_tracks', many=True)

    class Meta:
        model = Playlist
        fields = ['id','uuid', 'name', 'tracks' ]

    def create(self, validated_data):
        tracks_data = validated_data.pop('playlist_tracks')
        playlist_name = validated_data.get('name')
        
        playlist, created = Playlist.objects.get_or_create(name=playlist_name, defaults=validated_data)
        
        for track_data in tracks_data:
            order = track_data['order']
            track_id = track_data['track']
            
            # Check if the track is already in the playlist
            if PlaylistTrack.objects.filter(playlist=playlist, track=track_id).exists():
                continue  # Skip this track since it is already in the playlist
            
            if PlaylistTrack.objects.filter(order=order).exists():
                tracks_to_update = PlaylistTrack.objects.filter(playlist=playlist, order__gte=order)
                tracks_to_update.update(order=F('order') + 1)
            
            PlaylistTrack.objects.create(playlist=playlist, track=track_id, order=order)
        
        return playlist




    def update(self, instance, validated_data):
        breakpoint()
        tracks_data = validated_data.pop('playlist_tracks', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if tracks_data is not None:
            # Handle tracks update
            existing_tracks = instance.playlist_tracks.all()
            existing_track_ids = set(existing_track.track_id for existing_track in existing_tracks)

            # Remove tracks that are not in the updated data
            for existing_track in existing_tracks:
                if existing_track.track_id not in [track_data['track'] for track_data in tracks_data]:
                    existing_track.delete()

            # Update or create tracks based on the updated data
            for track_data in tracks_data:
                track_id = track_data['track']
                order = track_data['order']

                if track_id in existing_track_ids:
                    # Track already exists, update its order if necessary
                    existing_track = PlaylistTrack.objects.get(playlist=instance, track=track_id)
                    if existing_track.order != order:
                        existing_track.order = order
                        existing_track.save()
                else:
                    # Track doesn't exist, create a new one
                    PlaylistTrack.objects.create(playlist=instance, track=track_id, order=order)

        return instance
    
    def delete(self, instance):
        instance.delete()
