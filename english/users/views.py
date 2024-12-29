from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.db import IntegrityError
from django.contrib import messages

from first_app.models import *
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    # Это нужно, чтобы каждому п-лю отображался его профиль
    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

def my_words(request):
    words = WordsToLearn.objects.filter(user=request.user.id)
    # В отдельную переменную можно записать даты, соответствующие нужному слову. Соответствие брать по id из таблицы Dictionary
    my_words = Dictionary.objects.filter(id__in=list(words.values_list('word', flat=True)))

    if request.method == 'POST':
        word = Dictionary.objects.get(id=request.POST.get('word_id'))
        WordsToLearn.objects.get(user=request.user, word=word).delete()
        messages.success(request, 'Слово удалено из вашего списка')

    data = {
        'my_words': my_words,
        'title': 'My words'
    }

    return render(request, 'users/words.html', context=data)

def add_words(request):
    words_to_add = Dictionary.objects.all()

    if request.method == 'POST':
        try:
            word = Dictionary.objects.get(id=request.POST.get('word_id'))
            WordsToLearn.objects.create(user=request.user, word=word)
            messages.success(request, 'Слово добавлено в ваш список')
        except IntegrityError:
            messages.info(request, 'Это слово уже есть в вашем списке')

    data = {
        'words': words_to_add,
        'title': 'Add words'
    }

    return render(request, 'users/add_words.html', context=data)
