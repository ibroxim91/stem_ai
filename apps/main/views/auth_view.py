from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # O'zgartiring: sizda mavjud bo'lgan sahifaga
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri")
            return render(request, 'auth/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Parollar mos emas")
            return render(request, 'auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi band")
            return render(request, 'auth/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
