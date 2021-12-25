from django.db.models.base import Model
from django.forms import ModelForm
from .models import Board, Note
from django.contrib.auth.models import User

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'body']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']