from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import SavedPassword

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
    return render(request, 'safe/generate_password.html')


class PasswordAddView(LoginRequiredMixin, CreateView):
    model = SavedPassword
    template_name = 'safe/add_password.html'
    fields = ['website', 'password']
    success_url = reverse_lazy('saved')

    def form_valid(self, form):
        form.instance.saver = self.request.user
        return super().form_valid(form)