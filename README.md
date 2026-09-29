# Blog System — сводные таблицы примеров кода по урокам 1–7

Ниже собраны разделы «Примеры кода — сводная таблица» из каждого пройденного урока курса.

---

## Урок 1. Основы веб-разработки. Установка Django. Создание проекта

| Команда | Правильный пример | Пояснение |
|---|---|---|
| Создание venv | `python -m venv venv` | Создаёт папку с изолированным окружением |
| Активация (Windows) | `venv\Scripts\activate` | Включает окружение, появляется `(venv)` |
| Активация (macOS/Linux) | `source venv/bin/activate` | То же самое для Unix-систем |
| Установка Django | `pip install django` | Устанавливает Django внутрь активного venv |
| Проверка версии | `pip show django` | Показывает установленную версию пакета |
| Создание проекта | `django-admin startproject blog_system .` | Точка в конце — без лишней вложенной папки |
| Запуск сервера | `python manage.py runserver` | Запускает сервер на порту 8000 по умолчанию |
| Запуск на другом порту | `python manage.py runserver 8080` | Меняет порт запуска |
| Деактивация venv | `deactivate` | Выключает виртуальное окружение |

---

## Урок 2. Структура Django. Приложения. URL и views

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| Создание приложения | `python manage.py startapp blog` | Создаёт папку `blog/` с базовыми файлами |
| Регистрация приложения | `INSTALLED_APPS = [..., 'blog']` | Без этого Django не учитывает приложение |
| Простая view | `def home(request): return HttpResponse("Текст")` | Возвращает текстовый ответ |
| Маршрут без параметра | `path('', views.home, name='home')` | Корневой маршрут приложения |
| Маршрут с path parameter | `path('post/<int:post_id>/', views.post_detail, name='post_detail')` | Целочисленный обязательный параметр |
| Query parameter в view | `request.GET.get('q', '')` | Необязательный параметр из `?q=...` |
| Подключение приложения | `path('blog/', include('blog.urls'))` | Подключает `urls.py` приложения с префиксом |

---

## Урок 3. Templates. Template inheritance. Static

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| view с render | `return render(request, 'blog/home.html', {'title': '...'})` | Возвращает HTML вместо простого текста |
| Наследование | `{% extends 'blog/base.html' %}` | Первая строка дочернего шаблона |
| Блок | `{% block content %}...{% endblock %}` | Место, переопределяемое в дочернем шаблоне |
| Вывод переменной | `{{ title }}` | Подставляет значение из контекста |
| Подключение static | `{% load static %}` + `{% static 'blog/css/style.css' %}` | Правильный способ подключения CSS |

---

## Урок 4. Models. Migrations. Django Admin

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| Модель | `class Post(models.Model): title = models.CharField(max_length=200)` | Описание структуры данных |
| Создание миграции | `python manage.py makemigrations` | Составляет план изменений БД |
| Применение миграции | `python manage.py migrate` | Реально изменяет структуру БД |
| Регистрация в админке | `admin.site.register(Post)` | Делает модель видимой в панели администратора |
| Создание суперпользователя | `python manage.py createsuperuser` | Создаёт учётную запись с полным доступом |

---

## Урок 5. Django ORM. Связи моделей

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| Получить все записи | `Post.objects.all()` | Возвращает QuerySet со всеми постами |
| Фильтрация | `Post.objects.filter(is_published=True)` | Записи, подходящие под условие |
| Одна запись | `Post.objects.get(id=1)` | Ровно одна запись или ошибка |
| Сортировка | `Post.objects.order_by('-created_at')` | По убыванию даты создания |
| Связь один-ко-многим | `category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')` | Пост принадлежит категории |
| Обратный доступ | `category.posts.all()` | Все посты этой категории |

---

## Урок 6. Forms и ModelForm

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| ModelForm | `class PostForm(forms.ModelForm): class Meta: model = Post; fields = [...]` | Форма на основе модели |
| CSRF в шаблоне | `{% csrf_token %}` | Обязателен внутри `<form method="post">` |
| Обработка GET/POST | `if request.method == 'POST': ... else: form = PostForm()` | Разное поведение для показа и приёма формы |
| Проверка валидности | `if form.is_valid(): form.save()` | Сохранение только корректных данных |
| Вывод формы | `{{ form.as_p }}` | Быстрый вывод всех полей с ошибками |

---

## Урок 7. CRUD публикаций: создание и список

| Элемент | Правильный пример | Пояснение |
|---|---|---|
| Ссылка по имени маршрута | `{% url 'post_create' %}` | Строит URL из `name=` в `urls.py` |
| Ссылка с параметром | `{% url 'post_detail' post_id=post.id %}` | Параметр должен совпадать с именем в `path()` |
| Пагинатор | `Paginator(posts, 5)` | Разбивает QuerySet по 5 записей на страницу |
| Получение страницы | `paginator.get_page(page_number)` | Безопасно обрабатывает некорректный номер |



or |
and &