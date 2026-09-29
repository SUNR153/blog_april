from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'is_published', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 60}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_mb = 5
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(f'Размер изображения не должен превышать {max_size_mb} МБ.')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_mb = 3
            if image.size > max_size_mb * 1024 * 1024:
                raise forms.ValidationError(f'Размер изображения не должен превышать {max_size_mb} МБ.')
        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class EmailRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']