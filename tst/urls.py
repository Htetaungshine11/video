from django.urls import path
from . import views as v
urlpatterns = [
    path('',v.index),
    path('stream/<str:name>/',v.stream_video.as_view(),name='stream'),
    path('upload/',v.upload1.as_view(),name='upload'),
    path('list/',v.listv.as_view(),name='list'),
    path('delete/<str:name>/',v.deletev.as_view(),name='delete'),
]
