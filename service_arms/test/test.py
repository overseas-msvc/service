
from db_manage.mysql_connector.database import Database
from service_arms.code import code

def write_test_to_db(test):
    test_type = test["test_type"]
    del test["test_type"]
    
    db = Database("Test")
    test_id = db.add_object(test_type, test)
    test_id = db.add_object("Test", {
        "test_type": test_type,
        "test_id": test_id
    })
    return test_id

def get_test_files(test_id, code_id, endpoints):
    db = Database("Test")
    test = db.get_object_by_id("Test", test_id)
    files = code.get_test_files(code_id, test.test_type, endpoints)
    return files



