from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
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

            