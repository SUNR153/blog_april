from django import forms
from .models import Post, Comment, Category


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
                raise forms.ValidationError(f'Размер картинки не должен превышать {max_size_mb} МБ.')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']

    def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                max_size_mb = 5
                if image.size > max_size_mb * 1024 * 1024:
                    raise forms.ValidationError(f'Размер картинки не должен превышать {max_size_mb} МБ.')
            return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']