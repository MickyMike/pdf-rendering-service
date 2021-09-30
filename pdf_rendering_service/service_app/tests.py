from unittest import mock

from django.test import TestCase, Client, override_settings
from django.core.files import File
from PIL import Image, ImageChops

from .models import Document, Page
from .tasks import render, render_images


TEST_PDF = "tests/files/pdf_test.pdf"
TEST_IMG = "tests/files/image_test.png"


class DocumentTest(TestCase):
    def test_file_field(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'pdf_test.pdf'
        file_model = Document(pdf_file=file_mock)
        self.assertEqual(file_model.pdf_file.name, file_mock.name)

    def test_document(self):
        document = Document(pdf_file=TEST_PDF, status=Document.Status.PROCESSING, pages=1)
        document.save()
        self.assertEqual(document.pdf_file.name, TEST_PDF)


class ViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.document = Document(pdf_file=TEST_PDF, status=Document.Status.PROCESSING, pages=1)
        self.document.save()

    def test_get_document_valid(self):
        response = self.client.get(f"/api/documents/{self.document.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '{"status": "processing", "n_pages": 1}')

    def test_get_document_invalid(self):
        response = self.client.get(f"/api/documents/{self.document.pk + 1}/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), '{"detail":"Not found."}')


class RenderTaskTest(TestCase):
    def setUp(self) -> None:
        self.template_img = Image.open(TEST_IMG)
        self.document = Document(pdf_file=TEST_PDF, status=Document.Status.PROCESSING, pages=1)
        self.document.save()

    def assert_images_different(self, img1, img2):
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            raise AssertionError("Images are different")

    def test_render(self):
        rendered_img = render(TEST_PDF)[0]
        self.assert_images_different(self.template_img, rendered_img)

    def test_render_images(self):
        render_images(self.document.pk)
        rendered_img = Image.open(Page.objects.get(pk=1).page_img)
        self.assert_images_different(self.template_img, rendered_img)
