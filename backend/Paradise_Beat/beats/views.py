from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from .models import(
    Category, 
    Comment,
    Beat,
    Tag
)
from . import serializers
from.paginations import BeatPagination



class BeatViewSet(ViewSet, BeatPagination):
    """
    A viewset for working with beat instances.
    """
    def list(self, request, category_slug=None, status=None):
        queryset = Beat.objects.all()
        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        if status is not None:
            queryset = queryset.filter(status=status)
        result = self.paginate_queryset(queryset, request)
        serializer = serializers.BeatSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)
    

    def retrieve(self, request, slug, pk):
        queryset = get_object_or_404(Beat,slug=slug, pk=pk)
        serializer = serializers.BeatDetailSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                serializer = serializers.BeatSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    slug = get_random_string(50)
                    beat = Beat.drafts.create(
                        producer = user,
                        title = serializer.validated_data['title'],
                        slug = str(slug),
                        main_status = "DF",
                        status = "CH"
                    )
                    beat.save()
                    return Response({"Response":"Created."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"invalid user type."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unauthorized user."},status=status.HTTP_401_UNAUTHORIZED)


    def update(self, request, slug, pk):
        queryset = get_object_or_404(Beat, slug=slug, pk=pk)
        if request.user.is_authenticated == True:
            if request.user == queryset.producer:
                serializer = serializers.BeatSerializer(queryset, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"you are not the main producer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"you are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    

    def delete(self, request, slug, pk):
        queryset = get_object_or_404(Beat, slug=slug, pk=pk)
        if request.user.is_authenticated == True:
            if request.user == queryset.producer:
                queryset.delete()
                return Response({"Response":"Deleted."}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"you are not the main producer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"you are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

            