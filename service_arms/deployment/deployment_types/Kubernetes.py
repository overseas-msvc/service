
from service_arms.deployment.deployment_types.kubernetes_utils.Deployment import Deployment
from db_manage.mysql_connector.database import Database


class Kubernetes():
    
    def __init__(self, data):
        db = Database("Deployment")
        components = db.get_list_of_objects("KubernetesComponent", {"kubernetes_id": data.id})
        self.components = []
        for component in components:
            self.components.append(self.get_component(component))

    @classmethod
    def write_to_db(cls, deployment_info):
        db = Database("Deployment")
        deployment_components = deployment_info["components"]
        del deployment_info["components"]
        deployment_id = db.add_object("Kubernetes", deployment_info)
        for component in deployment_components:
            component_type = component["component_type"]
            del component["component_type"]
            component_variables = component["variables"]
            del component["variables"]
            # component_id = db.add_object(component_type, component)
            # the word kubernetes shouldnt be here
            component_class = cls.get_component_class(component_type)
            component_id = component_class.write_to_db(component)
            db.add_object("KubernetesComponent", {"component_type": component_type,
                                                  "component_id": component_id,
                                                  "kubernetes_id": deployment_id})
            for variable in component_variables:
                variable["parent_type"] = component_type
                variable["parent_id"] = component_id
                db.add_object("Variable", variable)
        return deployment_id

    def get_component_class(component_type):
        match component_type:
            case "KubernetesDeployment":
                return Deployment

    def get_component(self, component):
        match component.component_type:
            case "KubernetesDeployment":
                return Deployment(component.component_id)
            
    def get_yamls(self, service_name, image):
        folders = []
        for component in self.components:
            folders.append(component.get_yamls(service_name, image))
        return folders
    
        
#TODO: if somone wants a config ma or secret as part of the service it should automaticly be paired to the deployment/job. also what about a job