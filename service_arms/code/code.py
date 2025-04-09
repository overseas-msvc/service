import importlib
from db_manage.mysql_connector.database import Database


def write_code_to_db(code_info):
    db = Database("Code")
    code_type = code_info["code_type"]
    del code_info["code_type"]
    code_id = db.add_object(code_type, code_info)
    code_id = db.add_object("Code", {
        "code_type": code_type,
        "code_id": code_id
    })
    return code_id


def get_files(code_id, endpoints):
    code = get_code_obj(code_id)
    files = code.get_files(endpoints)
    return files

def get_test_files(code_id, test_type, endpoints):
    code = get_code_obj(code_id)
    files = code.get_test_files(test_type, endpoints)
    return files

def get_code_obj(code_id):
    db = Database("Code")
    code_info = db.get_object_by_id("Code", code_id)
    code_type = code_info.code_type
    module = importlib.import_module(f"service_arms.code.code_types.{code_type}")
    code = getattr(module, code_type)(code_info.code_id)
    return code