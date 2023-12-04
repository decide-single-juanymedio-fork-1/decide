from rest_framework import serializers
from .validators import validador_palabras_ofensivas
from .models import Question, QuestionOption, Voting
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        option = serializers.CharField(validators=[validador_palabras_ofensivas])
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('desc', 'options')

    def validate_desc(self, value):
        validador_palabras_ofensivas(value)
        return value


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(validators=[validador_palabras_ofensivas])
    desc = serializers.CharField(validators=[validador_palabras_ofensivas])
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    name = serializers.CharField(validators=[validador_palabras_ofensivas])
    desc = serializers.CharField(validators=[validador_palabras_ofensivas])

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')
