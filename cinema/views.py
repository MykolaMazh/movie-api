from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from cinema.models import Movie
from cinema.serializers import MovieSerializer


def create_movie_or_400(data, instance=None):
    if instance:
        serializer = MovieSerializer(instance, data)
    else:
        serializer = MovieSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return create_movie_or_400(request.data)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail(request, pk):
    if request.method == "GET":
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        try:
            movie = Movie.objects.get(pk=pk)
            return create_movie_or_400(request.data, movie)
        except ObjectDoesNotExist:
            return create_movie_or_400(request.data)
    else:
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
