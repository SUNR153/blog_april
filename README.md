Команда	                Правильный пример	                        Пояснение
Создание                venv	python -m venv venv	                Создаёт папку с изолированным окружением
Активация               (Windows)	venv\Scripts\activate	        Включает окружение, появляется (venv)
Активация               (macOS/Linux)	source venv/bin/activate	То же самое для Unix-систем
Установка               Django	pip install django	                Устанавливает Django внутрь активного venv
Проверка                версии	pip show django	                    Показывает установленную версию пакета
Создание проекта	    django-admin startproject blog_system .	    Точка в конце — без лишней вложенной папки
Запуск сервера	        python manage.py runserver	                Запускает сервер на порту 8000 по умолчанию
Запуск на другом порту	python manage.py runserver 8080	            Меняет порт запуска
Деактивация venv	    deactivate	                                Выключает виртуальное окружение