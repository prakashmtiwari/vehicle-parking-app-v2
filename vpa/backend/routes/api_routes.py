import importlib
from flask_restful import Api

def load_class(class_path):
    """Dynamically import a class from a string path."""
    module_name, class_name = class_path.rsplit(".", 1)  # Split module and class name
    module = importlib.import_module(module_name)  # Import module dynamically
    return getattr(module, class_name)  # Get class from module

def register_api_routes(api: Api):
    """Manually register API routes"""
    
    # Pass class path as a string inside api.add_resource()
    api.add_resource(load_class("vpa.resources.spot_resource.spotListResource"), "/spots")
    api.add_resource(load_class("vpa.resources.spot_resource.spotResource"), "/spots/<int:spot_id>")
    api.add_resource(load_class("vpa.resources.lot_resource.lotResource"), "/lots", "/lots/<int:id>")
