from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import Census


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )
    actions = ['exportar_censo']

    def exportar_censo(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=censo_exportado.csv'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['Votacion ID', 'Votante ID'])

        for censo in queryset:
            csv_writer.writerow([censo.voting_id, censo.voter_id])
        return response

    exportar_censo.short_description = 'Exportar censo'


admin.site.register(Census, CensusAdmin)
