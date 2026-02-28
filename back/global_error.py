from flask import jsonify
from werkzeug.exceptions import HTTPException

def global_error_handler(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "success": False,
            "error": {
                "type": e.name,
                "message": e.description,
                "status_code": e.code,
            }
        }
        
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        response = {
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": str(e),
                "status_code": 500,
            }
        }
        
        return jsonify(response), 500