from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from .models import Apportionment
from .models import Preference

from .filters import StartedFilter
from django.utils.translation import ngettext


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)

def reset(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.reset_voting()

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally,reset ]



admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)

# Admin de count

class ApportionmentAdmin(admin.ModelAdmin):
    list_display = (['voting_id','seats', 'method', 'solution'])
    readonly_fields = (['method','solution'])

    list_filter = (['voting_id'])
    search_fields = (['voter_id', 'method'])

    actions = ['dhondt','sainte_lague']

    # pylint: disable=arguments-differ
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'seats':
            formfield.help_text = "It is recommended that the seats be a multiple of the total votes."

        return formfield

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

class PreferenceAdmin(admin.ModelAdmin):

    list_display = (['voting_id', 'solution'])
    readonly_fields = (['solution'])

    list_filter = (['voting_id'])
    search_fields = (['voter_id'])

    actions = ['sort']

    def sort(self, request, queryset):
        for preference in queryset:
            voting_id = preference.voting_id
            try:
                voting = Voting.objects.get(id=voting_id)
                if voting.tally is not None:
                    preference.sort(voting)
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
            except Voting.DoesNotExist:
                self.message_user(
                    request,
                    f"Voting with ID {voting_id} does not exist.",
                    level='ERROR'
                )

    sort.short_description = 'Sort'


admin.site.register(Apportionment, ApportionmentAdmin)
admin.site.register(Preference, PreferenceAdmin)