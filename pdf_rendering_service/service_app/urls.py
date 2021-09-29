from django.urls import path

from .views import DocumentUploadView, DocumentView, PageView


urlpatterns = [
    path("documents/", DocumentUploadView.as_view()),
    path("documents/<int:pk>/", DocumentView.as_view()),
    path("documents/<int:pk>/pages/<int:num>", PageView.as_view()),
]
