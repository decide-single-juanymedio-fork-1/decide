from django.contrib import admin
from django.utils.translation import ngettext

from voting.models import Voting
from .models import Apportionment

# Register your models here.

class ApportionmentAdmin(admin.ModelAdmin):
    list_display = (['voting_id','seats', 'method', 'solution'])
    readonly_fields = (['method','solution'])

    list_filter = (['voting_id'])
    search_fields = (['voter_id', 'method'])

    actions = ['dhondt','sainte_lague']

    def dhondt(self, request, queryset):
        for apportionment in queryset:
            voting_id = apportionment.voting_id
            try:
                voting = Voting.objects.get(id=voting_id)
                if apportionment.method is None:
                    if voting.tally is not None:
                        apportionment.dhondt(voting)
                        # Mensaje de éxito
                        self.message_user(
                            request,
                            ngettext(
                                'voting %d was successfully processed.',
                                'votings %d were successfully processed.',
                                queryset.count()
                            ) % queryset.count(),
                            level='SUCCESS'
                        )
                    else:
                        self.message_user(
                            request,
                            f"Voting with ID {voting_id} has a null 'tally' field and will be skipped.",
                            level='WARNING'
                        )
                else:
                    self.message_user(
                        request,
                        f"Voting with ID {voting_id} already has a counting method applied and will be skipped.",
                        level='WARNING'
                    )
            except Voting.DoesNotExist:
                self.message_user(
                    request,
                    f"Voting with ID {voting_id} does not exist.",
                    level='ERROR'
                )

    dhondt.short_description = 'D\'Hondt Method'

    def sainte_lague(self, request, queryset):
        for apportionment in queryset:
            voting_id = apportionment.voting_id
            try:
                voting = Voting.objects.get(id=voting_id)
                if apportionment.method is None:
                    if voting.tally is not None:
                        apportionment.sainte_lague(voting)
                        # Mensaje de éxito
                        self.message_user(
                            request,
                            ngettext(
                                'voting %d was successfully processed.',
                                'votings %d were successfully processed.',
                                queryset.count()
                            ) % queryset.count(),
                            level='SUCCESS'
                        )
                    else:
                        self.message_user(
                            request,
                            f"Voting with ID {voting_id} has a null 'tally' field and will be skipped.",
                            level='WARNING'
                        )
                else:
                    self.message_user(
                        request,
                        f"Voting with ID {voting_id} already has a counting method applied and will be skipped.",
                        level='WARNING'
                    )
            except Voting.DoesNotExist:
                self.message_user(
                    request,
                    f"Voting with ID {voting_id} does not exist.",
                    level='ERROR'
                )

    sainte_lague.short_description = 'Sainte-Laguë Method'

admin.site.register(Apportionment, ApportionmentAdmin)