# task_manager/rollbar_test_view.py
from django.http import HttpResponse

def trigger_error(request):
    division_by_zero = 1 / 0  # намеренная ошибка
    return HttpResponse(f"Result: {division_by_zero}")
