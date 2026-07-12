from django.urls import path
from . import views

urlpatterns = [

    path("upload/", views.upload_dataset, name="upload"),

    path("delete/<int:id>/", views.delete_dataset, name="delete_dataset"),

    path("download/<int:id>/", views.download_dataset, name="download_dataset"),

    path("details/<int:id>/", views.file_details, name="file_details"),

]