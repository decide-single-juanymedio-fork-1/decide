import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8000"
VOTING = 1


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))



class DefThanks(TaskSet):

    @task
    def index(self):
        self.client.get("/booth/thanks/")


class DefViewRegister(TaskSet):

    @task
    def index(self):
        self.client.get("/booth/register/")

class DefRegister(TaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def register(self):
        username, pwd = self.voter
        self.register = self.client.post("/booth/register/", {
            "username": username,
            "password1": pwd,
            "password2": pwd
        }).json()

    def on_quit(self):
        self.voter = None

class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)


    def on_quit(self):
        self.voter = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)

class Register(HttpUser):
    host = HOST
    tasks = [DefRegister]
    wait_time= between(3,5)

class Thanks(HttpUser):
    host = HOST
    tasks = [DefThanks]
    wait_time= between(3,5)

class ViewRegister(HttpUser):
    host = HOST
    tasks = [DefViewRegister]
    wait_time= between(3,5)