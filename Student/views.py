from django.contrib.sites import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Student



@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        username = request.POST.get('username')

        # Сохраняем данные в базу
        if telegram_id and username:
            user, created = Student.objects.get_or_create(telegram_id=telegram_id, defaults={'username': username})
            if created:
                return JsonResponse({'status': 'success', 'message': 'User registered'})
            else:
                return JsonResponse({'status': 'success', 'message': 'User already registered'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def dashboard_view(request):
    # Получаем telegram_id пользователя из параметра запроса
    telegram_id = request.GET.get('telegram_id')  # telegram_id передается через URL параметр

    try:
        # Ищем пользователя по telegram_id
        student = Student.objects.get(telegram_id=telegram_id)
    except Student.DoesNotExist:
        student = None

    # Передаем информацию о пользователе в шаблон
    context = {
        'student': student
    }

    return render(request, 'dashboard.html', context)


def get_user_data(telegram_id):
    response = requests.get(f'https://your-ngrok-url/get_user_data/{telegram_id}/')
    print(telegram_id)
    if response.status_code == 200:
        return response.json()  # Возвращает данные пользователя
    return None

def index(request):
    return render(request, "lessons.html", )


@csrf_exempt
def register_or_update_student(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        username = request.POST.get('username')
        coins = request.POST.get('coins', 0)

        # Логика для сохранения данных пользователя
        if telegram_id and username:
            student, created = Student.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={'username': username, 'coins': coins}
            )
            if not created:
                # Если студент уже существует, обновляем данные
                student.username = username
                student.coins = coins
                student.save()

            return JsonResponse({'status': 'success', 'message': 'User registered or updated', 'coins': student.coins})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def navbar_view(request):
    # Получаем telegram_id пользователя из параметра запроса
    telegram_id = request.GET.get('telegram_id')  # или получить из сессии request.session.get('telegram_id')

    # Найдем пользователя в базе данных
    try:
        user = Student.objects.get(telegram_id=telegram_id)
    except Student.DoesNotExist:
        user = None

    context = {
        'username': user.username if user else 'Гость',
    }
    return render(request, 'home.html', context)


