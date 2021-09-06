from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource
from role.controller import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

ro = Blueprint("role", __name__)
api = Api(ro)


class AllRoles(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                role_cursor = get_all_roles()
                roles = [x for x in role_cursor]
                return make_response(roles, 200)
            else:
                return make_response(jsonify({"MSG": "ADMIN REQUIRED"}), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class AddRole(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                role = request.json.get("role")
                add_role(role)
                return make_response(jsonify({"MSG": "Role  added"}), 200)
            else:
                return make_response(jsonify({"MSG": "ADMIN REQUIRED"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class RemoveRole(Resource):
    @jwt_required
    def delete(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                role = request.json.get("role")
                remove_role(role)
                return make_response(jsonify({"MSG": "Role Removed"}), 200)
            else:
                return make_response(jsonify({"MSG": "ADMIN REQUIRED"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class UpdateRole(Resource):
    @jwt_required
    def put(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                role = request.json.get("role")
                new_role = request.json.get("new_role")
                update_role(role, new_role)
                return make_response(jsonify({"MSG": "Role updated"}), 200)
            else:
                return make_response(jsonify({"MSG": "ADMIN REQUIRED"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


api.add_resource(AllRoles, '/allroles')
api.add_resource(AddRole, '/addrole')
api.add_resource(RemoveRole, '/removerole')
api.add_resource(UpdateRole, '/updaterole')
