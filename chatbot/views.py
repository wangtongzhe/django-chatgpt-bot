import datetime

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import ChatMessage
from .tools import ask_with_chat_completion, ask_with_completion


# Create your views here.


class ChatBotView(View):

    def get_history(self):
        history = []
        if self.request.user.is_authenticated:
            history = ChatMessage.objects.filter(user=self.request.user).order_by('created_at')
        return history

    def get(self, request, *args, **kwargs):
        return render(request, 'chatbot.html', {"history": self.get_history()})

    def post(self, request, *args, **kwargs):
        message = request.POST.get("message")
        history = self.get_history()
        if self.request.user.is_authenticated:
            response = ask_with_chat_completion(history, message)
            chat_message = ChatMessage(user=request.user, message=message, response=response,
                                       created_at=datetime.datetime.now())
            chat_message.save()
        else:
            response = ask_with_completion(message)
        return JsonResponse({"message": message, "response": response})


def login(request):
    return render(request, 'login.html')


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('chatbot')
        else:
            return render(request, self.template_name, {'form': form})


class RegisterView(View):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('chatbot')
        else:
            return render(request, self.template_name, {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('login')
