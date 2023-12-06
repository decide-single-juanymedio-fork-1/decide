import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


from base import mods



# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

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
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/booth/1/')
        else:
            form = UserCreationForm()
        return render(request, 'register.html')
#{'form':form}, context_instance=RequestContext(request))