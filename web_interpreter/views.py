import json

from django.shortcuts import render
from django.http import JsonResponse

from tools import secure_execute_program

# API
def execute_code(request):
    data = json.loads(request.body)
    lang = data.get('language')
    code = data.get('code')
    stdin = data.get('input')
    stdout, stderr = secure_execute_program.start_program(code, stdin, lang)
    return JsonResponse({'stdout': stdout, 'stderr': stderr})

# Create your views here.
def interpreter(request):
    if request.method == "POST":
        return execute_code(request)
    return render(request, 'interpreter.html')
    
