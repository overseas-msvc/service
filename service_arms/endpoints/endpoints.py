import importlib
from db_manage.mysql_connector.database import Database


def write_endpoints_to_db(endpoints, service_id):
    db = Database("Endpoint")
    for endpoint in endpoints:
        endpoint_type = endpoint["endpoint_type"]
        del endpoint["endpoint_type"]
        variables = endpoint["variables"]
        del endpoint["variables"]
        endpoint_id = db.add_object(endpoint_type, endpoint)
        endpoint_id = db.add_object("Endpoint", {"endpoint_type": endpoint_type,
                                   "endpoint_id": endpoint_id,
                                   "service_id": service_id})
        write_variables_to_db(db, variables, endpoint_id)



def write_variables_to_db(db, variables, endpoint_id):
    for variable in variables:
        variable["endpoint_id"] = endpoint_id
        db.add_object("Variable", variable)

def get_endpoints(service_id):
    db = Database("Endpoint")
    endpoints = db.get_list_of_objects("Endpoint", {"service_id": service_id})
    endpoints_instaces = []
    for endpoint in endpoints:
        endpoints_instace = db.get_object_by_id(endpoint.endpoint_type, endpoint.endpoint_id, inJson=True)
        endpoints_instace["variables"] = db.get_list_of_objects("Variable", {"endpoint_id": endpoints_instace["id"]}, inJson=True)
        endpoints_instaces.append(endpoints_instace)
    return endpoints_instaces


# def get_endpoints_objs(service_id):
#     db = Database("Endpoint")
#     endpoints = db.get_list_of_objects("Endpoint", {"service_id": service_id})
#     endpoints_objs = []
#     for endpoint in endpoints:
#         endpoint_type = endpoint.endpoint_type
#         module = importlib.import_module(f"service_arms.endpoints.endpoint_types.{endpoint_type}")
#         endpoints_objs.append(getattr(module, endpoint_type)(endpoint.endpoint_id))
#     return endpoints_objs
