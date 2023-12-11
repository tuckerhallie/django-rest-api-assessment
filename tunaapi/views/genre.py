from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre
from django.db.models import Count

class GenreView(ViewSet):
    
    def retrieve(self, request, pk):
      try:
        genre = Genre.objects.annotate(song_count=Count('songs')).get(pk=pk)
        serializer = SongGenreSerializer(genre)
        return Response(serializer.data)
      except Genre.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
      genres = Genre.objects.annotate(song_count=Count('songs')).all()
      serializer = SongGenreSerializer(genres, many=True)
      return Response(serializer.data)
    
    def create(self, request):
        genre = Genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class SongsGenreSerializer(serializers.ModelSerializer):
  class Meta:
      model = SongGenre
      fields = ('song_id', )
      depth = 1
      
class SongGenreSerializer(serializers.ModelSerializer):
  songs = SongsGenreSerializer(many=True, read_only=True)
  song_count = serializers.SerializerMethodField()
  
  class Meta:
      model = Genre
      fields = ('id', 'description', 'songs', 'song_count')
      depth = 2
      
  def get_song_count(self, obj):
        return obj.song_count
      
class GenreSerializer(serializers.ModelSerializer):
  songs = SongsGenreSerializer(many=True, read_only=True)
