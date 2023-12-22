from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = "beats"


urlpatterns = [
    path('beat/<slug:slug>/<int:pk>/', views.BeatViewSet.as_view({'get':'retrieve'}), name="beat_detail"),

    # Producer View urls
    path('beat/create/', views.ProducerBeatView.as_view({'post':'create'}), name="create_new_beat"),
    path('beat/update/<slug:slug>/<int:pk>/', views.ProducerBeatView.as_view({'post':'update'}), name="update_beat"),
    path('beat/delete/<slug:slug>/<int:pk>/', views.ProducerBeatView.as_view({'post':'delete'}), name="delete_beat"),


    # Simular and ...
    path('simular-beat/<int:pk>/', views.SimularBeatView.as_view(), name='simular_beats'),
    path('related-producer-beat/<int:pk>/', views.ProducerRelatedBeatView.as_view(), name="related_producer_beats"),

    # Comments urls
    path('comments-beat/<int:beat_id>/', views.CommentViewSet.as_view({"get":"list"}), name='list_beat_comments'),
    path('add-comment/<int:beat_id>/', views.CommentViewSet.as_view({"post":"create"}), name="create_comment"),
    path('update-comment/<int:pk>/', views.CommentViewSet.as_view({"post":"update"}), name="update_comment"),

    # Private, Draft, Public Beat list
    path("private-beat-list/", views.PrivateBeatsView.as_view(), name="private_beats"),
    path("draft-beat-list/", views.DraftBeatsView.as_view(), name="draft_beats"),
    path("public-beat-list/", views.PublishedBeatsView.as_view(), name="public_beats"),

    # Accepted, Rejected, Checking
    path("accepted-beat-list/", views.AcceptedBeatsView.as_view(), name="accepted_beats"),
    path("rejected-beat-list/", views.RejectedBeatsView.as_view(), name="rejected_beats"),
    path("checking-beat-list/", views.CheckingBeatsView.as_view(), name="Checking_beats"),


    # Like & Dislike views
    path('beat-like/<int:pk>/', views.BeatLikeView.as_view(), name="beat_like"),
    path('beat-un-like/<int:pk>/', views.BeatUnLikeView.as_view(), name="beat_un_like"),
    path('beat-dislike/<int:pk>/', views.BeatDisLikeView.as_view(), name="beat_dislike"),
    path('beat-un-dislike/<int:pk>/', views.BeatUnDisLikeView.as_view(), name="beat_un_dislike")
]

router = DefaultRouter()
router.register(r'beat', views.BeatViewSet, basename='beat')
urlpatterns += router.urls