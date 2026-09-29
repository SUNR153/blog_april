from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Category
from .forms import PostForm


class PostModelTest(TestCase):
    def test_post_str(self):
        category = Category.objects.create(name='Django')
        post = Post.objects.create(title='Тестовый пост', content='Текст', category=category)
        self.assertEqual(str(post), 'Тестовый пост')


class PostListViewTest(TestCase):
    def test_post_list_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)


class PostDetail404Test(TestCase):
    def test_nonexistent_post_returns_404(self):
        response = self.client.get(reverse('post_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class PostFormTest(TestCase):
    def test_empty_title_invalid(self):
        form = PostForm(data={'title': '', 'content': 'Текст', 'is_published': False})
        self.assertFalse(form.is_valid())


class PostCreateLoginTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)


class PostPermissionTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='pass12345')
        self.other_user = User.objects.create_user(username='other', password='pass12345')
        self.post = Post.objects.create(title='Пост автора', content='Текст', author=self.author)

    def test_other_user_cannot_edit(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.get(reverse('post_update', args=[self.post.id]))
        self.assertEqual(response.status_code, 403)