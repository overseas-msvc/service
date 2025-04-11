from jinja2 import Template
from service_arms.deployment.deployment_types.kubernetes_utils.KubernetesComponent import KubernetsComponent
from db_manage.mysql_connector.database import Database

class Deployment(KubernetsComponent):
    def __init__(self, deployment_id):
        db = Database("Deployment")
        deployment = db.get_object_by_id("KubernetesDeployment", deployment_id)
        self.id = deployment.id
        self.port = deployment.port
        self.app = deployment.app # should it be a label
        self.include_autoScale = bool(deployment.include_autoScale == "true")
        self.include_service = bool(deployment.include_service == "true")
        self.variables = db.get_list_of_objects("Variable", {"parent_type": "KubernetesDeployment",
                                                                                 "parent_id": self.id})
        if self.include_autoScale:
            self.hpa = db.get_list_of_objects("Hpa", {"KubernetesDeployment_id": self.id})[0]

    def write_to_db(component):
        db = Database("Deployment")
        if component["include_autoScale"] == "true":
            hpa = component["hpa"]
            del component["hpa"]
        component_id = db.add_object("KubernetesDeployment", component)
        if component["include_autoScale"] == "true":
            hpa["KubernetesDeployment_id"] = component_id
            db.add_object("Hpa", hpa)
        return component_id



    ##todo: add autoscalling flag
    def get_yamls(self, service_name, image):
        folder = super().get_yamls(service_name)
        files = []
        for file in folder.files:
            if file.name == "deployment.yaml":
                files.append(file)
            if file.name == "hpa.yaml" and self.include_autoScale:
                files.append(file)
            if file.name == "service.yaml" and self.include_service:
                files.append(file)
        folder.files = files
        for file in folder.files:
            template = Template(file.content)
            paremeters = {
                "app": self.app,
                "name": service_name.lower(),
                "service_name": service_name.lower(),
                "port": self.port,
                "image": f"{image}:1.<version>",
                "deployment_variables": self.get_variables_yaml()
            }
            if self.include_autoScale:
                paremeters.update({
                    "maxReplicas": self.hpa.max_replicas,
                    "minReplicas": self.hpa.min_replicas,
                })
            file.content = template.render(paremeters)
        return folder
    
    def get_variables_yaml(self):
        yaml_str = ""
        for var in self.variables:
            yaml_str += f"\n        - name: {var.name}\n          value: \"{var.value}\""
        return yaml_str