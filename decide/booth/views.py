import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.contrib import messages

from base import mods
from .models import *
from .forms import OrderForm, CreateUserForm



# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get(self, request, *args, **kwargs):
        language = request.POST.get('language', None)
        if language and language in [lang[0] for lang in settings.LANGUAGES]:
            activate(language)

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context


    def registerPage(request):
        if request.method=='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('thanks')
        else:
            form = CreateUserForm()
        return render(request, 'register.html',{"form": form})
    
    def loginPage(request):
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('thanks')
            else:
                messages.info(request, 'Nombre de usuario o contraseña incorrectos')
        return render(request, 'login.html',{"form": form})
    
    def logoutUser(request):
        logout(request)
        return redirect('login')

class StaticViews(TemplateView):
    template_name = 'thanks.html'
    def GiveThanks(request):
        return render(request,'thanks.html')