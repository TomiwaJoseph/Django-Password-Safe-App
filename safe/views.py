from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import SavedPassword
import pyperclip
from random import shuffle, sample


current_password = ''

# Create your views here.
def index(request):
    return render(request, 'safe/index.html')


class SavedListView(LoginRequiredMixin, ListView):
    model = SavedPassword
    template_name = 'safe/saved.html'
    ordering = ['-date_created']

    def de_encrypt(self, message, key):
        SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:;<=>?@'
        key = -key
        translated = ''

        for symbol in message:
            symbolIndex = SYMBOLS.find(symbol)
            if symbolIndex == -1:
                translated += symbol
            else:
                symbolIndex += key

                if symbolIndex >= len(SYMBOLS):
                    symbolIndex -= len(SYMBOLS)
                elif symbolIndex < 0:
                    symbolIndex += len(SYMBOLS)

                translated += SYMBOLS[symbolIndex]
        return translated

    def get_queryset(self):
        return SavedPassword.objects.filter(saver=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = SavedPassword.objects.filter(saver=self.request.user).order_by('-date_created')

        bad = []
        for i in queryset:
            bad.append(self.de_encrypt(i.password, 13))

        context['passwords'] = bad
        context['length'] = range(len(bad))
        return context


@login_required
def generate_password(request):
    global current_password
    current_password = ''
    passwords = []
    number = [chr(i) for i in range(48,65)]
    cap_letters = [chr(i) for i in range(65,91)]
    small_letters = [chr(i) for i in range(97,123)]

    while len(passwords) != 5:
        a,b,c = sample(number,4),sample(cap_letters,4),sample(small_letters,4)
        d = a+b+c
        shuffle(d)
        passwords.append(''.join(d))

    return render(request, 'safe/generate_password.html', {'password': passwords})


@login_required
def use_pass(request):
    global current_password
    current_password = request.POST.get('passw')
    return redirect('add_pass')

class PasswordAddView(LoginRequiredMixin, CreateView):
    model = SavedPassword
    template_name = 'safe/add_password.html'
    fields = ['website', 'password']
    success_url = reverse_lazy('saved')

    def form_valid(self, form):
        form.instance.saver = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {'password': current_password}