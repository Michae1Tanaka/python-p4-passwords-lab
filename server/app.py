#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User


class ClearSession(Resource):
    def delete(self):
        session["page_views"] = None
        session["user_id"] = None

        return {}, 204


class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(username=json["username"])
        user._password_hash = json["password"]
        db.session.add(user)
        db.session.commit()
        user_query = User.query.filter(User.username == user.username).first()
        session["user_id"] = user_query.id
        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user_id = session["user_id"]
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 201
        return {}, 204


class Login(Resource):
    def post(self):
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        user = User.query.filter(User.username == username).first()
        if password == user._password_hash:
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {}, 401


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {}, 204


api.add_resource(ClearSession, "/clear", endpoint="clear")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
