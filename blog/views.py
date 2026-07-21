from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Главная страница блога')

def post_detail(request, post_id):
    return HttpResponse(f'Пост номер {post_id}')

def search(request):
    query = request.GET.get('q', '')
    return HttpResponse(f'Вы искали: {query}')
