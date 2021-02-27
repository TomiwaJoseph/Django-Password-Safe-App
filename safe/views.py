from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import SavedPassword
import pyperclip
from random import shuffle, sample

# Create your views here.
def index(request):
    return render(request, 'safe/index.html')


class SavedListView(LoginRequiredMixin, ListView):
    model = SavedPassword
    template_name = 'safe/saved.html'
    ordering = ['-date_created']

    def get_queryset(self):
        return SavedPassword.objects.filter(saver_id=self.request.user.id).order_by('-date_created')

def generate_password(request):
    passwords = []
    number = [chr(i) for i in range(48,65)]
    cap_letters = [chr(i) for i in range(65,91)]
    small_letters = [chr(i) for i in range(97,123)]

    while len(passwords) != 5:
        a,b,c = sample(number,4),sample(cap_letters,4),sample(small_letters,4)
        d = a+b+c
        shuffle(d)
        passwords.append(''.join(d))

    print(passwords)
    return render(request, 'safe/generate_password.html', {'password1': passwords})


class PasswordAddView(LoginRequiredMixin, CreateView):
    model = SavedPassword
    template_name = 'safe/add_password.html'
    fields = ['website', 'password']
    success_url = reverse_lazy('saved')

    def form_valid(self, form):
        form.instance.saver = self.request.user
        return super().form_valid(form)