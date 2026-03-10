from locust import HttpUser, task, between
import random

class LoginUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)

    @task
    def login(self):
        # Pick a random user from our database
        user_id = random.randint(1, 1000000)
        self.client.post("/login", json={
            "username": f"user{user_id}",
            "password": f"pass{user_id}"
        })



