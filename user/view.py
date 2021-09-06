from flask import Blueprint, make_response, request, jsonify
from flask_restful import Api, Resource
from user.controller import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

usr = Blueprint("user", __name__)
api = Api(usr)


class UserInfo(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                users_cursor = get_all_users()
                users = [x for x in users_cursor]
                return users
            else:
                return make_response(jsonify({"MSG": "ADMIN rights required"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class AddUser(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                user_info = request.get_json()
                role_id = get_role_id(user_info["role"])
                if role_id:
                    add_user(user_info, role_id)
                    return make_response(jsonify({"MSG": "User added"}), 200)
                else:
                    return make_response(jsonify({"MSG": "Role assigned doesnt exist"}), 400)
            else:
                return make_response(jsonify({"MSG": "ADMIN rights required"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class UpdatePassword(Resource):
    @jwt_required
    def put(self):
        try:
            email = request.json.get("email")
            password = request.json.get("password")
            auth_cursor = get_auth(email, password)
            if auth_cursor:
                new_password = request.json.get("new_password")
                update_password(email, new_password)
                return make_response(jsonify({"MSG": "Password updated"}), 200)
            else:
                return make_response(jsonify({"MSG": "Credentials invalid or missing"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class RemoveUser(Resource):
    @jwt_required
    def delete(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                email = request.json.get("email")
                remove_user(email)
                return make_response(jsonify({"MSG": "User Removed"}), 200)
            else:
                return make_response(jsonify({"MSG": "ADMIN rights required"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


# class Login(Resource):
#     def post(self):
#         try:
#             email = request.json.get("email")
#             password = request.json.get("password")
#             user_cursor = get_auth(email, password)
#             role = user_cursor["role"]
#             if user_cursor:
#                 access_token = create_access_token(identity={"email": email, "role": role}, expires_delta=False)
#                 create_session(email, access_token)
#                 return make_response(jsonify({"Logged in Successful": access_token}), 200)
#             else:
#                 return make_response(jsonify({"Invalid": "Credentials"}), 201)
#         except Exception as e:
#             return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


# class Logout(Resource):
#     @jwt_required
#     def post(self):
#         try:
#             current_user = get_jwt_identity()
#             remove_session(current_user["email"])
#             return make_response(jsonify({"Logged": "out"}), 200)
#         except Exception as e:
#             return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


api.add_resource(UserInfo, '/userinfo')
api.add_resource(AddUser, '/adduser')
api.add_resource(UpdatePassword, '/updatepassword')
api.add_resource(RemoveUser, '/removeuser')
# api.add_resource(Login, '/login')
# api.add_resource(Logout, '/logout')
