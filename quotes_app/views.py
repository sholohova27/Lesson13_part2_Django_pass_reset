from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from .forms import AuthorForm, QuoteForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm


def index(request):
    return render(request, 'index.html')


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def quotes(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes.html', {'quotes': quotes})

#функциональное представление
@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})


#классовое представление
class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_update.html'
    success_url = '/authors/'


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author_detail.html'


# функциональное представление
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Автоматический вход после регистрации
            return redirect('quotes_app:index')  # Перенаправление на домашнюю страницу
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


# функциональное представление
def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('quotes_app:index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('quotes_app:index')