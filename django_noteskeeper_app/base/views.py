from contextlib import redirect_stdout
from typing import ContextManager
import typing_extensions
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Board, Note
from .forms import BoardForm, NoteForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # userd = form.save()
            # # user.username = user.username.lower()
            # userd.save()
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')
    
    context = {"page": page, "form": form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    boards = Board.objects.filter(
        Q(owner__username__icontains=q) | 
        Q(name__icontains=q)
    )
    context = {"boards": boards}
    return render(request, 'base/home.html', context)

def board(request, pk):
    user_board = Board.objects.get(id=pk)
    notes = user_board.note_set.all()
    context = {"user_board": user_board, "notes": notes}
    return render(request, 'base/board.html', context)

@login_required(login_url='/login')
def create_board(request):
    form = BoardForm()
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            Board.objects.create(
                owner = request.user,
                name = request.POST.get('name')
            )
            return redirect('home')
    context = {"form": form}
    return render(request, 'base/board_form.html', context)

@login_required(login_url='/login')
def update_board(request, pk):
    board = Board.objects.get(id=pk)
    form = BoardForm(instance=board)

    if request.method == "POST":
        board.name = request.POST.get('name')
        board.save()
        return redirect('home')

    context = {"form": form}
    return render(request, 'base/board_form.html', context)

@login_required(login_url='/login')
def delete_board(request, pk):
    board = Board.objects.get(id=pk)

    if request.user != board.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        board.delete()
        return redirect('home')

    context = {"obj": board}
    return render(request, 'base/delete.html', context)

def note(request, pk):
    current_note = Note.objects.get(id=pk)
    context = {"current_note": current_note}
    return render(request, 'base/note.html', context)

@login_required(login_url='/login')
def create_note(request, pk):
    form = NoteForm()
    main_board = Board.objects.get(id=pk)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            Note.objects.create(
                owner = request.user,
                board = main_board,
                topic = request.POST.get('topic'),
                body = request.POST.get('body'),
            )
            return redirect('board', pk=main_board.id)
    context = {"form": form}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='/login')
def update_note(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)

    if request.method == "POST":
        note.topic = request.POST.get('topic')
        note.body = request.POST.get('body')
        note.save()
        return redirect('board', note.board.id)

    context = {"form": form, "note": note}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='/login')
def delete_note(request, pk):
    note = Note.objects.get(id=pk)

    if request.user != note.owner:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        note.delete()
        return redirect('home')

    context = {"obj": note}
    return render(request, 'base/delete.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    user_boards = Board.objects.filter(
        Q(owner__id=pk)
    )
    user_notes = user.note_set.all()
    # user_notes = Note.objects.filter(
    #     Q(owner__id=pk)
    # )
    context = {"user_boards": user_boards, "user": user, "user_notes": user_notes}
    return render(request, 'base/profile.html', context)
