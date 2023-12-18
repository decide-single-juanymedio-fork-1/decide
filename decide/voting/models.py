from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validador_palabras_ofensivas
from django.core.exceptions import ValidationError

from base import mods
from base.models import Auth, Key


class Question(models.Model):
    desc = models.TextField(validators=[validador_palabras_ofensivas])

    def clean(self):
        validador_palabras_ofensivas(self.desc)

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField(validators=[validador_palabras_ofensivas])

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def clean(self):
        validador_palabras_ofensivas(self.option)

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200, validators=[validador_palabras_ofensivas])
    desc = models.TextField(blank=True, null=True, validators=[validador_palabras_ofensivas])
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == 'a':
                    votes_format.append(vote[info])
                if info == 'b':
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def reset_voting(self, token=''):
        auth = self.auths.first()
        self.start_date = None
        self.end_date = None
        self.pub_key = None
        self.tally = None
        self.postproc = None
        self.save()

    def clean(self):
        validador_palabras_ofensivas(self.name)
        validador_palabras_ofensivas(self.desc)

    def __str__(self):
        return self.name

# Modelos de count

class Preference(models.Model):
    voting_id = models.PositiveIntegerField()
    solution = models.TextField(blank=True, null=True)

    def sort(self, voting):
        if not voting.postproc:
            raise ValidationError("No postprocessing data available.")
        postproc_list = voting.postproc if voting.postproc else []
        postproc_dict = {option['option']+'('+ str(option['number']) +')': option['postproc'] for option in postproc_list}
        solution_dict = dict(sorted(postproc_dict.items(), key=lambda item: item[1], reverse=True))
        formatted_solution = ',\n '.join([f'{i+1}- {key}: {value}' for i, (key, value) in enumerate(solution_dict.items())])
        self.solution = formatted_solution
        self.save()

    class Meta:
        unique_together = (('voting_id',),)

    def __str__(self):
        return 'Voting: {}'.format(self.voting_id)

class Apportionment(models.Model):
    voting_id = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    method = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)

    def generate_postproc_dict(self, voting):
        postproc_list = voting.postproc if voting.postproc else []
        postproc_dict = {option['option']+'('+ str(option['number']) +')': float(option['postproc']) for option in postproc_list}
        return postproc_dict

    def dhondt(self, voting):
        if not voting.postproc:
            raise ValidationError("No postprocessing data available.")
        self.method = 'D\'Hondt'
        postproc_dict = self.generate_postproc_dict(voting)
        seats_count_dicc = postproc_dict.copy()
        solution_dict = {key: 0 for key in postproc_dict.keys()}
        seats_number = self.seats
        for _ in range(seats_number):
            # Actualizar seats_count_dicc dividiendo el número de votos originales entre el nuevo número de escaños asignados hasta entonces
            seats_count_dicc = {key: postproc_dict[key] / (solution_dict[key] + 1) for key in seats_count_dicc.keys()}
            # Encontrar la opción con el máximo valor en el postproc_dict
            max_option = max(seats_count_dicc, key=seats_count_dicc.get)
            # Incrementar el valor correspondiente en el solution_dict
            solution_dict[max_option] += 1
        formatted_solution = ', '.join([f'{key}: {value}' for key, value in solution_dict.items()])
        self.solution = formatted_solution
        self.save()

    def sainte_lague(self, voting):
        if not voting.postproc:
            raise ValidationError("No postprocessing data available.")
        self.method = 'Sainte-Laguë'
        postproc_dict = self.generate_postproc_dict(voting)
        seats_count_dicc = postproc_dict.copy()
        solution_dict = {key: 0 for key in postproc_dict.keys()}
        seats_number = self.seats
        for _ in range(seats_number):
            # Actualizar seats_count_dicc dividiendo el número de votos originales entre el nuevo número de escaños asignados hasta entonces
            seats_count_dicc = {key: postproc_dict[key] / (2*(solution_dict[key]+1) - 1) for key in seats_count_dicc.keys()}
            # Encontrar la opción con el máximo valor en el postproc_dict
            max_option = max(seats_count_dicc, key=seats_count_dicc.get)
            # Incrementar el valor correspondiente en el solution_dict
            solution_dict[max_option] += 1
        formatted_solution = ', '.join([f'{key}: {value}' for key, value in solution_dict.items()])
        self.solution = formatted_solution
        self.save()

    class Meta:
        unique_together = (('voting_id', 'seats', 'method'),)

    def __str__(self):
        return 'Voting: {} - Seats: {}'.format(self.voting_id, self.seats)
