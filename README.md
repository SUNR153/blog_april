Команда	                    Правильный пример	                                  Пояснение
Создание venv	            python -m venv venv	                                  Создаёт папку с изолированным окружением
Активация                   (Windows)	venv\Scripts\activate	                  Включает окружение, появляется (venv)
Активация                   (macOS/Linux)	source venv/bin/activate	          То же самое для Unix-систем
Установка Django	        pip install django	                                  Устанавливает Django внутрь активного venv
Проверка версии	            pip show django	                                      Показывает установленную версию пакета
Создание проекта	        django-admin startproject blog_system .	              Точка в конце — без лишней вложенной папки
Запуск сервера	            python manage.py runserver	                          Запускает сервер на порту 8000 по умолчанию
Запуск на другом порту	    python manage.py runserver 8080	                      Меняет порт запуска
Деактивация venv	        deactivate	                                          Выключает виртуальное окружение
Создание приложения	        python manage.py startapp blog	                      Создаёт папку blog/ с базовыми файлами
Регистрация приложения	    INSTALLED_APPS = [..., 'blog']	                      Без этого Django не учитывает приложение
Простая view	            def home(request): return HttpResponse("Текст")	      Возвращает текстовый ответ
Маршрут без параметра	    path('', views.home, name='home') 	                  Корневой маршрут приложения
Маршрут с path parameter	path('post/<int:post_id>/', views.post_detail, name='post_detail')	Целочисленный обязательныйпараметр
Query parameter в view	    request.GET.get('q', '')	                          Необязательный параметр из ?q=...
Подключение приложения	    path('blog/', include('blog.urls'))	                  Подключает urls.py приложения с префиксом
view с render	            return render(request, 'blog/home.html', {'title': '...'})	Возвращает HTML вместо простого текста
Наследование	            {% extends 'blog/base.html' %}	                      Первая строка дочернего шаблона
Блок	                    {% block content %}...{% endblock %}	              Место, переопределяемое в дочернем шаблоне
Вывод переменной	        {{ title }}	                                          Подставляет значение из контекста
Подключение static	        {% load static %} + {% static 'blog/css/style.css' %} Правильный способ подключения CSS



all() - получить все записи
filter(поле=значение)
exclude(поле=значение)
get(поле=значение)
first()/last()
exists()
count()
order_by('поле')
order_by('-поле')

Post.objects.all()
Post.objects.filter(is_published=True).order_by('created_at')

<a style = {}>


<form method="post">
    {% csrf_token %}

</form>

is_valid()
