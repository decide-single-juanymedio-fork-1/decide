from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
import csv
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from .forms import ImportarCensoForm
from django.shortcuts import render
from rest_framework import generics
from django.views import View
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census

def is_admin_user(user):
    return user.is_authenticated and user.is_staff

class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')


class CensusExport(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        census_data = Census.objects.filter(voting_id=voting_id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=censo_exportado.csv'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Votacion ID', 'Votante ID'])

        for censo in census_data:
            csv_writer.writerow([censo.voting_id, censo.voter_id])
        return response

@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class ImportCensus(View):
    template_name = 'importar_censo.html'

    def get(self, request, *args, **kwargs):
        form = ImportarCensoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ImportarCensoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            if archivo and archivo.name.endswith('.csv'):
                try:
                    contenido_texto = archivo.read().decode('utf-8').splitlines()
                    csv_reader = csv.reader(contenido_texto)
                    for row in csv_reader:
                        voting_id, voter_id = row
                        Census.objects.create(voting_id=voting_id, voter_id=voter_id)
                    return JsonResponse({'mensaje': 'Censos importados con éxito'}, status=ST_201)
                except IntegrityError:
                    return JsonResponse({'mensaje': 'Error ya hay un censo con ese id de votacion y ese id de votante'}, status=ST_409)
            else:
                return JsonResponse({'error': 'El archivo que intentas importar no tiene el formato correcto'}, status=400)
        else:
            form = ImportarCensoForm()

        return render(request, 'importar_censo.html', {'form': form})
