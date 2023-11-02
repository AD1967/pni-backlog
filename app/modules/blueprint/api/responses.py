from flask import jsonify
# стандартный ответ через json
# success = True - result будет в поле result
# success = False - result будет в поле error
def default_json_response(success, result):
    return jsonify({"success": success, ("result" if success else "error"): result})