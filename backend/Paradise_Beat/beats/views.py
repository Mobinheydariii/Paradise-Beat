from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework import status
from . import serializers
from .models import(
    Beat,
    Category,
    Comment,
    Tag,
)


class CategoryList(APIView):
    def get(self, request):
        instance = Category.objects.all()
        serializer = serializers.CategorySerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AcceptedBeatsList(APIView):
    def get(self, request):
        instance = Beat.accepted.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DraftBeats(APIView):
    def get(self, request):
        instance = Beat.drafts.all()
        queryset = instance.filter(producer=request.user)
        if not queryset:
            return Response({"error": "You do not have any draft beats."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.BeatSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class BeatDetail(APIView):
    def get(self, request, slug, pk):
        try:
            instance = Beat.objects.get(slug=slug, id=pk)
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Beat.DoesNotExist:
            return Response({'error': 'This beat does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
class CommentsView(APIView):
    def post(self, request, slug, pk):
        user = request.user
        beat = get_object_or_404(Beat, slug=slug, pk=pk)
        serializer = serializers.Commntserializer(request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            Comment.objects.create(comment=data['text'], user=user, beat=beat)
            return Response("comment added", status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, slug, pk):
        user = request.user
        comment = get_object_or_404(Comment,id=pk, beat__slug=slug, user=user)
        serializer = serializers.EditCommentsSerializer(comment, data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)