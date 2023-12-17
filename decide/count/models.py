from django.db import models

# Create your models here.


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
        self.method = 'D\'Hondt'
        postproc_dict = self.generate_postproc_dict(voting)
        seats_count_dicc = postproc_dict.copy()
        solution_dict = {key: 0 for key in postproc_dict.keys()}
        seats_number = self.seats
        for seat in range(seats_number):
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
        self.method = 'Sainte-Laguë'
        postproc_dict = self.generate_postproc_dict(voting)
        seats_count_dicc = postproc_dict.copy()
        solution_dict = {key: 0 for key in postproc_dict.keys()}
        seats_number = self.seats
        for seat in range(seats_number):
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
        return 'Voting: {} - Seats: ({})'.format(self.voting_id, self.seats)