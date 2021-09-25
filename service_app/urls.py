from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import DocumentUploadView, DocumentViewset

router = SimpleRouter()
router.register("documents", DocumentViewset)

urlpatterns = [
    path('upload', DocumentUploadView.as_view()),
]

urlpatterns += router.urls
