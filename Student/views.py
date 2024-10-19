from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student  # Предполагаем, что у вас есть модель для хранения пользователей

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
