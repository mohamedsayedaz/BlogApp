from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post


# Create your tests here.


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=self.user,
        )

    def test_post_createview(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "Test Post",
                "body": "This is a test post.",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Test Post")
        self.assertEqual(Post.objects.last().body, "This is a test post.")

    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "Updated Test Post",
                "body": "This is an updated test post.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated Test Post")
        self.assertEqual(Post.objects.last().body, "This is an updated test post.")

    def test_post_deleteview(self):
        response = self.client.post(
            reverse("post_delete", args="1"),
        )
        self.assertEqual(response.status_code, 302)
