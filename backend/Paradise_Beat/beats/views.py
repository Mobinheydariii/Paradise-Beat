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

# Accepted Beats
class AcceptedBeats(APIView):
    def get(self, request):
        instance = Beat.accepted.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProducerAcceptedBeats(APIView):
    def get(self, request):
        producer = request.user
        instance = Beat.accepted.get(producer=producer)
        if not instance:
            return Response({"error":"You dont have any accepted beats."}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProducerAcceptedBeatDetail(APIView):
    def get(self, request, slug):
        instance = Beat.accepted.get(slug=slug)
        if not instance:
            return Response({"error":"There is no beat with this slug"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Draft Beats
class DraftBeats(APIView):
    def get(self, request):
        instance = Beat.drafts.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerDraftBeats(APIView):
    def get(self, request):
        instance = Beat.drafts.all()
        queryset = instance.filter(producer=request.user)
        if not queryset:
            return Response({"error": "You do not have any draft beats."}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = serializers.BeatSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProducerDraftBeatDetail(APIView):
    def get(self, request, slug):
        instance = Beat.drafts.get(slug=slug)
        if not instance:
            return Response({"error":"There is no beat with this slug"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

# Rejected Beat
class RejectedBeats(APIView):
    def get(self, request):
        instance = Beat.rejected.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerRejectedBeats(APIView):
    def get(self, request):
        instance = Beat.rejected.all()
        queryset = instance.filter(producer=request.user)
        if not queryset:
            return Response({"error": "You do not have any rejected beats."}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = serializers.BeatSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProducerRejectedBeatDetail(APIView):
    def get(self, request, slug):
        instance = Beat.rejected.get(slug=slug)
        if not instance:
            return Response({"error":"There is no beat with this slug"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

# Published Beat
class PublishedBeats(APIView):
    def get(self, request):
        instance = Beat.published.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerPublishedBeats(APIView):
    def get(self, request):
        instance = Beat.published.all()
        queryset = instance.filter(producer=request.user)
        if not queryset:
            return Response({"error": "You do not have any published beats."}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = serializers.BeatSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProducerPublishedBeatDetail(APIView):
    def get(self, request, slug):
        instance = Beat.published.get(slug=slug)
        if not instance:
            return Response({"error":"There is no beat with this slug"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

# Checking Beat    
class CheckingBeats(APIView):
    def get(self, request):
        instance = Beat.checking.all()
        serializer = serializers.BeatSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerCheckingBeats(APIView):
    def get(self, request):
        instance = Beat.checking.all()
        queryset = instance.filter(producer=request.user)
        if not queryset:
            return Response({"error": "You do not have any checking beats."}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = serializers.BeatSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProducerCheckingBeatDetail(APIView):
    def get(self, request, slug):
        instance = Beat.checking.get(slug=slug)
        if not instance:
            return Response({"error":"There is no beat with this slug"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)



class Categories(APIView):
    def get(self, request):
        instance = Category.objects.all()
        serializer = serializers.CategorySerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BeatDetail(APIView):
    def get(self, request, slug, pk):
        try:
            instance = Beat.objects.get(slug=slug, id=pk)
            serializer = serializers.BeatSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Beat.DoesNotExist:
            return Response({'error': 'This beat does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class AddCommentView(APIView):
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