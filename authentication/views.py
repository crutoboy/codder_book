from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print(1)
            return redirect('/')
        else:
            print(2)
            return render(request, 'signin.html')
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        # Проверка на совпадение паролей
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            print('Пароли не совпадают')
            return redirect('register')

        # Проверка на уникальность имени пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            print('Пользователь с таким именем уже существует')
            return redirect('register')

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        messages.success(request, 'Регистрация прошла успешно! Вы можете войти в систему.')
        print('Регистрация прошла успешно! Вы можете войти в систему.')
        return redirect('login')  # Перенаправление после успешной регистрации

    return render(request, 'signup.html')

def logout_(request):
    logout(request)
    return redirect('/')