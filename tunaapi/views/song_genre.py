from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre, Artist

class SongGenreView(ViewSet):
  
    def retrieve(self, request, pk):
      try:
        song_genre = SongGenre.objects.get(pk=pk)
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data)
      except SongGenre.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
      song_genres = SongGenre.objects.all()
      serializer = SongGenreSerializer(song_genres, many=True)
      return Response(serializer.data)
    
    def create(self, request):
        songId = Song.objects.get(pk=request.data["song_id"])
        genreId = Genre.objects.get(pk=request.data["genre_id"])
        
        songGenre = SongGenre.objects.create(
          genre_id=genreId,
          song_id=songId
        )
        
        serializer = SongGenreSerializer(songGenre)
        return Response(serializer.data)
      
    def destroy(self, request, pk):
      
        songgenre = SongGenre.objects.get(pk=pk)
        songgenre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre_id')
        depth = 1 
