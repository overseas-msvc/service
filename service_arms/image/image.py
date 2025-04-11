from db_manage.mysql_connector.database import Database
from service_comunications.connectors import get_connector
import importlib


def write_image_to_db(image_info):
    db = Database("Image")
    image_type = image_info["image_type"]
    del image_info["image_type"]
    registry = image_info["registry"]
    del image_info["registry"]
    registry_type = registry["registry_type"]
    del registry["registry_type"]
    registry_id = db.add_object(registry_type, registry)
    image_id = db.add_object(image_type, image_info)
    image_id = db.add_object("Image", 
                                {"image_type": image_type,
                                 "image_id": image_id,
                                 "registry_type": registry_type,
                                 "registry_id": registry_id})
    return image_id

def create_registry_repository(image_id):
    image = get_image_obj(image_id)
    registry = get_registry_obj(image_id)
    registry.create_repository(image.image)

def get_artifact(image_id):
    return {
        "image": get_image(image_id),
        "registry": get_registry(image_id)
    }

def get_address(image_id):
    return f"{get_registry_obj(image_id).address}/{get_image_obj(image_id).image}"

def get_image(image_id):
    db = Database("Image")
    image = db.get_object_by_id("Image", image_id)
    image_instance = db.get_object_by_id(image.image_type, image.image_id, inJson=True)
    image_instance["image_type"] = image.image_type
    return image_instance

def get_registry(image_id):
    db = Database("Image")
    registry = db.get_object_by_id("Image", image_id)
    registry_instance = db.get_object_by_id(registry.registry_type, registry.registry_id, inJson=True)
    registry_instance["image_type"] = registry.registry_type
    return registry_instance

def get_image_obj(image_id):
    db = Database("Image")
    image = db.get_object_by_id("Image", image_id)
    image_type = image.image_type
    module = importlib.import_module(f"service_arms.image.image_types.{image_type}")
    image = getattr(module, image_type)(image.image_id)
    return image

def get_registry_obj(image_id):
    db = Database("Image")
    image = db.get_object_by_id("Image", image_id)
    registry_type = image.registry_type
    module = importlib.import_module(f"service_arms.image.registry_types.{registry_type}")
    registry = getattr(module, registry_type)(image.registry_id)
    return registry