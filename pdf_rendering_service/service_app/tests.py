from unittest import mock

from django.test import TestCase, Client, override_settings
from django.core.files import File
from PIL import Image, ImageChops

from .models import Document, Page
from .tasks import render, render_images


class DocumentTest(TestCase):
    def test_file_field(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        file_model = Document(pdf_file=file_mock)
        self.assertEqual(file_model.pdf_file.name, file_mock.name)


class ViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.document = Document(pdf_file="tests/files/pdf_test.pdf", status=Document.Status.PROCESSING, pages=1)
        self.document.save()
        self.page = Page(page_img="tests/files/image_test.png", document=self.document, page_num=1)
        self.page.save()

    def test_get_document_valid(self):
        response = self.client.get(f"/api/documents/{self.document.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '{"status": "processing", "n_pages": 1}')

    def test_get_document_invalid(self):
        response = self.client.get(f"/api/documents/{self.document.pk + 1}/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), '{"detail":"Not found."}')


class RenderTaskTest(TestCase):
    def assert_images_different(self, img1, img2):
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            raise AssertionError("Images are different")

    def test_render(self):
        template_img = Image.open("tests/files/image_test.png")
        rendered_img = render("tests/files/pdf_test.pdf")[0]
        self.assert_images_different(template_img, rendered_img)

    @override_settings(MEDIA_URL="/")
    def test_render_images(self):
        document = Document(pdf_file="tests/files/pdf_test.pdf", status=Document.Status.PROCESSING, pages=1)
        document.save()
        render_images(document.pk)
        rendered_img = Image.open("images/1_1.png")
        template_img = Image.open("tests/files/image_test.png")
        self.assert_images_different(template_img, rendered_img)
