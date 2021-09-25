from django.urls import path
from django.conf.urls import url

from .views import DocumentUploadView, view_document


urlpatterns = [
    path('document', DocumentUploadView.as_view()),
    path(r"document/^(?P<pk>\d+)$", view_document),
]
