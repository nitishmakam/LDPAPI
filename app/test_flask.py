import os
import pytest
from app import app
import random
import json

gen_user = lambda: "user%s" % str(random.randint(0, 10000000))

def register(client, username, email, password):
    return client.post(
            "/api/users/register",
            content_type="application/json",
            data=json.dumps(
                dict(
                    username=username,
                    email=email,
                    password=password)))

def login(client, username, password):
    return client.post(
            "/api/users/login",
            content_type="application/json",
            data=json.dumps(
                dict(
                    username=username,
                    password=password)))

def test_username_exists():
    c = app.test_client()
    username = gen_user()
    rv = c.get("/api/users/usernameExists/%s" % username)
    assert rv.status_code == 200
    rv = register(c, username, "%s@abc.com" % username,
                  "abc123")
    assert rv.status_code == 200
    rv = c.get("/api/users/usernameExists/%s" % username)
    assert rv.status_code == 409

def test_login():
    c = app.test_client()
    username = gen_user()
    rv = register(c, username, "%s@abc.com" % username,
                  "abc123")
    assert rv.status_code == 200
    rv = login(c, username, "abc321")
    assert rv.status_code == 403
    rv = login(c, username, "abc123")
    assert rv.status_code == 200

def test_prediction_db():
    c = app.test_client()
    username = gen_user()
    rv = register(c, username, "%s@abc.com" % username,
                  "abc123")
    assert rv.status_code == 200
    rv = login(c, username, "abc123")
    assert rv.status_code == 200
    token = rv.get_json()["token"]
    randomdata = json.dumps({
                    "key1": "val1",
                    "key2": "val2"})
    rv = c.post("/api/prediction/save",
                content_type="application/json",
                data=randomdata,
                headers={"token": token})
    assert rv.status_code == 200
    rv = c.post("/api/prediction/save",
                content_type="application/json",
                data=randomdata,
                headers={"token": token})
    assert rv.status_code == 200
    rv = c.get("/api/prediction/",
               headers={"token": token})
    assert len(rv.get_json()) == 2
    pid = rv.get_json()[0]["id"]
    rv = c.delete("/api/prediction/%s" % pid,
                  headers={"token": token})
    rv = c.get("/api/prediction/",
               headers={"token": token})
    assert len(rv.get_json()) == 1
