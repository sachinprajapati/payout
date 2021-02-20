from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView

from .models import Transaction

class AddTrans(CreateView):
    model = Transaction
