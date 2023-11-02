from flask import redirect, render_template, url_for, jsonify
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"success": False, "error" : "404"}), 200


##
@main.app_errorhandler(500)
def api_server_err(e):
    return jsonify({"success": False, "error" : "internal error"}), 200

# Ошибка авторизации
@main.app_errorhandler(401)
def unauthorized_err(e):
    print("401")
    return jsonify({"success": False, "error" : "401"}), 200
