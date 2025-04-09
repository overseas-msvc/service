
from service_arms.deployment.deployment_types.kubernetes_utils.Deployment import Deployment
from db_manage.mysql_connector.database import Database


class Kubernetes():
    
    def __init__(self, data):
        db = Database("Deployment")
        components = db.get_list_of_objects("KubernetesComponent", {"kubernetes_id": data.id})
        self.components = []
        for component in components:
            self.components.append(self.get_component(component))

    def get_component(self, component):
        match component.component_type:
            case "KubernetesDeployment":
                return Deployment(component.component_id)
            
    def get_yamls(self, service_name):
        folders = []
        for component in self.components:
            folders.append(component.get_yamls(service_name))
        return folders
    
        
#TODO: if somone wants a config ma or secret as part of the service it should automaticly be paired to the deployment/job. also what about a job