import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from store.models import Vote as StoreVote
from census.models import Census

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            voting_data = r[0]
            
            vote_count = StoreVote.objects.filter(voting_id=vid).count()
            
            census_count = Census.objects.filter(voting_id=vid).count()
            
            if census_count > 0:
                voting_data['voting_percentage'] = (vote_count/census_count) * 100
            else:
                voting_data['voting_percentage'] = 0
                
            voting_data['vote_count'] = vote_count
            voting_data['census_count'] = census_count
            
            context['voting'] = json.dumps(voting_data)
            
        except:
            raise Http404

        return context
