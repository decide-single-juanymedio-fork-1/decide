import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required


from base import mods
from census.models import Census
from store.models import Vote
from voting.models import Voting
from .forms import CustomUserChangeForm, CreateUserForm



# TODO: check permissions and census

def get_user_by_email(user_email):
    try:
        user= User.objects.get(email=user_email)
        return user.username if user else None
    except User.DoesNotExist:
        return None


def get_new_votings(user):
    new_voting_ids = []
    census_with_user = Census.objects.filter(voter_id=user.id)
    for census in census_with_user:
        voting = Voting.objects.get(id=census.voting_id)
        if voting.start_date and not voting.end_date:
            try:
                Vote.objects.get(voting_id=voting.id, voter_id=user.id)
            except Vote.DoesNotExist:
                new_voting_ids.append(voting.id)

    return new_voting_ids

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
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, user)
                return redirect('thanks')
        else:
            form = CreateUserForm()
        return render(request, 'register.html',{"form": form})

    def loginPage(request):
        if request.method=='POST':
            username_or_email = request.POST.get('username')
            password = request.POST.get('password')

            #Intenta autenticar con el nombre de usuario
            user_by_username = authenticate(request, username=username_or_email, password=password)

            #Intenta aunteticar con el correo electrónico
            username_by_email = get_user_by_email(username_or_email)
            user_by_email = authenticate(request, username=username_by_email, password=password)
            if user_by_username is not None:
                if user_by_username.is_superuser:
                    login(request, user_by_username)
                    return redirect('/admin')
                else:
                    login(request, user_by_username)
                    return redirect('home')
            elif user_by_email is not None:
                if user_by_email.is_superuser:
                    login(request, user_by_email)
                    return redirect('/admin')
                else:
                    login(request, user_by_email)
                    return redirect('home')
            else:
                messages.info(request, 'Nombre de usuario/correo electrónico o contraseña incorrectos')
        return render(request, 'login.html', {})

    def logoutUser(request):
        logout(request)
        return redirect('login')

    def homePage(request):
        user = request.user
        filtered_votes = Vote.objects.filter(voter_id=user.id)
        my_votings = []

        for v in filtered_votes:
            voting_id = v.voting_id

            try:
                voting = Voting.objects.get(id=voting_id)
                my_votings.append(voting.name)
            except Voting.DoesNotExist:
                my_votings.append('')

            for vot in my_votings:
                if vot == '':
                    my_votings.remove(vot)

        new_voting_ids = get_new_votings(user)
        unique_new_voting_ids = list(set(new_voting_ids))  # Obtener IDs únicos
        for voting_id in unique_new_voting_ids:
            messages.success(request, format_html("Hay una nueva votación. Haga click <a href='/booth/{}'>aquí</a> para participar.", voting_id))

        return render(request, 'home.html', {'my_votings': my_votings})

    @login_required
    def change_user(request):
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('home')
        else:
            form = CustomUserChangeForm(instance=request.user)

        return render(request, 'change_user.html', {'form':form})


class StaticViews(TemplateView):
    template_name = 'thanks.html'
    def GiveThanks(request):
        return render(request,'thanks.html')