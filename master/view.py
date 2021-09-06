
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from role.view import ro
from user.view import usr
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from controller import *


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = KEY
jwt = JWTManager(app)

api = Api(app)


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            password = request.json.get("password")
            user_cursor = get_auth(email, password)
            role = user_cursor["role"]
            if user_cursor:
                access_token = create_access_token(identity={"email": email, "role": role}, expires_delta=False)
                create_session(email, access_token)
                return make_response(jsonify({"Logged in Successful": access_token}), 200)
            else:
                return make_response(jsonify({"Invalid": "Credentials"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class Logout(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            remove_session(current_user["email"])
            return make_response(jsonify({"Logged": "out"}), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


app.register_blueprint(usr)
app.register_blueprint(ro)

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(debug=True)
