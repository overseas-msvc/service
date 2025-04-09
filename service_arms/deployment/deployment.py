from db_manage.mysql_connector.database import Database
import importlib


def write_deployment_to_db(deployment_info):
    db = Database("Deployment")
    deployment_type = deployment_info["deployment_type"]
    del deployment_info["deployment_type"]
    deployment_components = deployment_info["components"]
    del deployment_info["components"]
    deployment_id = db.add_object(deployment_type, deployment_info)
    for component in deployment_components:
        component_type = component["component_type"]
        del component["component_type"]
        component_variables = component["variables"]
        del component["variables"]
        component_id = db.add_object(component_type, component)
        # the word kubernetes shouldnt be here
        db.add_object("KubernetesComponent", {"component_type": component_type,
                                              "component_id": component_id,
                                              "kubernetes_id": deployment_id})
        for variable in component_variables:
            variable["parent_type"] = component_type
            variable["parent_id"] = component_id
            db.add_object("Variable", variable)
    deployment_id = db.add_object("Deployment", {
        "deployment_type": deployment_type,
        "deployment_id": deployment_id
    })
    return deployment_id

def get_yamls(deployment_id, service_name):
    deployment = get_deployment_obj(deployment_id)
    folder = deployment.get_yamls(service_name)
    return folder
    # fetch the deployment from db and then get yamls and return folder

def get_deployment(deployment_id):
    db = Database("Deployment")
    deployment = db.get_object_by_id("Deployment", deployment_id)
    deployment_instance = db.get_object_by_id(deployment.deployment_type, deployment.deployment_id, inJson=True)
    deployment_instance["deployment_type"] = deployment.deployment_type
    return deployment_instance

def get_deployment_obj(deployment_id):
    db = Database("Deployment")
    deployment = db.get_object_by_id("Deployment", deployment_id)
    deployment_type = deployment.deployment_type
    deployment = db.get_object_by_id(deployment_type, deployment.deployment_id)
    module = importlib.import_module(f"service_arms.deployment.deployment_types.{deployment_type}")
    deployment = getattr(module, deployment_type)(deployment)
    return deployment