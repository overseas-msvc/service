from jinja2 import Template
from service_arms.deployment.deployment_types.kubernetes_utils.KubernetesService import KubernetsService
from db_manage.mysql_connector.database import Database

class Deployment(KubernetsService):
    def __init__(self, deployment_id):
        db = Database("Deployment")
        deployment = db.get_object_by_id("KubernetesDeployment", deployment_id)
        self.id = deployment.id
        self.port = deployment.port
        self.image = deployment.image
        self.app = deployment.app # should it be a label
        self.min_replicas = deployment.minReplicas
        self.max_replicas = deployment.maxReplicas
        self.autoScale = deployment.autoScale
        self.variables = db.get_list_of_objects("Variable", {"parent_type": "KubernetesDeployment",
                                                                                 "parent_id": self.id})


    ##todo: add autoscalling flag
    def get_yamls(self, service_name):
        folder = super().get_yamls(service_name)
        for file in folder.files:
            template = Template(file.content)
            file.content = template.render({
                "app": self.app,
                "name": service_name.lower(),
                "service_name": service_name.lower(),
                "port": self.port,
                "image": f"{self.image}:1.<version>",
                "maxReplicas": self.max_replicas,
                "minReplicas": self.min_replicas,
                "deployment_variables": self.get_variables_yaml()
            })
        return folder
    
    def get_variables_yaml(self):
        yaml_str = ""
        for var in self.variables:
            yaml_str += f"\n        - name: {var.name}\n          value: \"{var.value}\""
        return yaml_str