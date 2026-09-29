from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import timedelta

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, CategoryForm, EmailRegisterForm, ProfileForm

RESEND_COOLDOWN_SECONDS = 60


# --- Базовые страницы ---

def home(request):
    categories = Category.objects.all()
    context = {'title': 'Главная страница блога', 'categories': categories}
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def rules(request):
    return render(request, 'blog/rules.html')


def search(request):
    query = request.GET.get('q', '')
    return HttpResponse(f"Вы искали: {query}")


# --- Список / поиск / фильтр / пагинация постов ---

def post_list(request):
    posts = Post.objects.filter(is_published=True)

    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    selected_category = request.GET.get('category', '')
    if selected_category:
        posts = posts.filter(category__id=selected_category)

    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['-created_at', 'created_at', '-views_count']
    if sort not in allowed_sorts:
        sort = '-created_at'
    posts = posts.order_by(sort)

    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 5

    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_category': selected_category,
        'sort': sort,
    })


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(is_published=True, category=category).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/posts_by_category.html', {'page_obj': page_obj, 'category': category})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


# --- CRUD Post ---

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать чужой пост.")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить чужой пост.")
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# --- CRUD Comment ---

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})


@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать чужой комментарий.")
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form, 'post': comment.post, 'comment': comment})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить чужой комментарий.")
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})


# --- CRUD Category ---

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form})


@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_form.html', {'form': form, 'category': category})


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'blog/category_confirm_delete.html', {'category': category})


# --- Аутентификация, профиль ---

def register(request):
    if request.method == 'POST':
        form = EmailRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_confirmation_email(request, user)
            return redirect('registration_pending')
    else:
        form = EmailRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def send_confirmation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirm_url = request.build_absolute_uri(f'/blog/confirm-email/{uid}/{token}/')
    message = render_to_string('blog/email_confirmation_message.html', {
        'user': user,
        'confirm_url': confirm_url,
    })
    send_mail(
        subject='Подтверждение регистрации в Blog System',
        message=message,
        from_email=None,
        recipient_list=[user.email],
    )
    user.profile.last_confirmation_sent = timezone.now()
    user.profile.save()


def registration_pending(request):
    return render(request, 'blog/registration_pending.html')


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'blog/email_confirmed.html')
    return render(request, 'blog/email_confirmation_invalid.html')


def resend_confirmation(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            last_sent = user.profile.last_confirmation_sent
            if last_sent and timezone.now() < last_sent + timedelta(seconds=RESEND_COOLDOWN_SECONDS):
                seconds_left = int((last_sent + timedelta(seconds=RESEND_COOLDOWN_SECONDS) - timezone.now()).total_seconds())
                error = f'Письмо уже отправлялось недавно. Попробуйте снова через {seconds_left} сек.'
            else:
                send_confirmation_email(request, user)
                return redirect('registration_pending')
        except User.DoesNotExist:
            error = 'Пользователь с таким email не найден или уже активирован.'
    return render(request, 'blog/resend_confirmation.html', {'error': error})


@login_required
def profile_view(request):
    return render(request, 'blog/profile.html', {'profile_user': request.user})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'form': form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})