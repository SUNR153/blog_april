from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name=_('Заголовок'))
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, allow_unicode=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts_authored', null=True, blank=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_authored', null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='comments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    last_confirmation_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username