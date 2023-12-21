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
    path('simular/beat/<int:pk>/', views.SimularBeatView.as_view(), name='simular_beats'),
    path('related/producer/beat/<int:pk>/', views.ProducerRelatedBeatView.as_view(), name="related_producer_beats"),

    # Comments urls
    path('comments/beat/<int:beat_id>/', views.CommentViewSet.as_view({"get":"list"}), name='list_beat_comments'),
    path('add/comment/<int:beat_id>/', views.CommentViewSet.as_view({"post":"create"}), name="create_comment"),
    path('update/comment/<int:pk>/', views.CommentViewSet.as_view({"post":"update"}), name="update_comment")
]

router = DefaultRouter()
router.register(r'beat', views.BeatViewSet, basename='beat')
urlpatterns += router.urls