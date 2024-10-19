from django.contrib.sites import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student  # Предполагаем, что у вас есть модель для хранения пользователей
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
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



def get_user_data(telegram_id):
    response = requests.get(f'https://your-ngrok-url/get_user_data/{telegram_id}/')
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
    # Получаем telegram_id пользователя (в реальном случае это должно приходить от Telegram)
    telegram_id = request.GET.get('telegram_id')  # Получаем telegram_id через параметры запроса для примера

    try:
        # Ищем пользователя по telegram_id
        student = Student.objects.get(telegram_id=telegram_id)
    except Student.DoesNotExist:
        student = None

    # Передаем информацию о пользователе в шаблон
    context = {
        'student': student
    }

    return render(request, 'navbar.html', context)

