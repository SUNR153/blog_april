from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, CategoryForm
from django.core.paginator import Paginator


# --- Урок 2: базовые views ---

def post_detail(request, post_id):
    return HttpResponse(f"Пост номер {post_id}")


def search(request):
    query = request.GET.get('q', '')
    return HttpResponse(f"Вы искали: {query}")


# --- Урок 3: templates ---

def home(request):
    categories = ['Django', 'Python', 'Веб-разработка']
    context = {
        'title': 'Главная страница блога',
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def rules(request):
    return render(request, 'blog/rules.html')


# --- Урок 5: ORM-демонстрация ---

def orm_demo(request):
    result = "Все посты:\n"
    for post in Post.objects.all():
        result += f"- {post.title}\n"

    result += "\nТолько опубликованные посты:\n"
    for post in Post.objects.filter(is_published=True):
        result += f"- {post.title}\n"

    result += "\nПосты, отсортированные по дате создания (новые сначала):\n"
    for post in Post.objects.order_by('-created_at'):
        result += f"- {post.title} ({post.created_at})\n"

    result += f"\nОбщее количество постов: {Post.objects.count()}\n"

    category = Category.objects.first()
    if category:
        result += f"\nПосты категории {category.name}:\n"
        for post in category.posts.all():
            result += f"- {post.title}\n"

    first_post = Post.objects.first()
    if first_post:
        result += f"\nКомментарии к посту {first_post.title}:\n"
        for comment in first_post.comments.all():
            result += f"- {comment.text}\n"

    result += "\nПосты с просмотрами больше 0, по убыванию просмотров:\n"
    for post in Post.objects.filter(views_count__gt=0).order_by('-views_count'):
        result += f"- {post.title} ({post.views_count} просмотров)\n"

    result += "\nКоличество постов по категориям:\n"
    for cat in Category.objects.all():
        result += f"- {cat.name}: {cat.posts.count()}\n"

    only_titles = Post.objects.values_list('title', flat=True)
    result += f"\nТолько заголовки всех постов: {list(only_titles)}\n"

    return HttpResponse(f"<pre>{result}</pre>", content_type="text/html; charset=utf-8")


# --- Урок 6: формы ---

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form})


# --- Урок 7: CRUD операции и пагинация ---

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    per_page = request.GET.get('per_page', 5)
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(is_published=True, category=category).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/posts_by_category.html', {'page_obj': page_obj, 'category': category})