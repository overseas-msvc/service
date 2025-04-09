import os

from folder.Folder import Folder, File


class KubernetsService:

    folder_path = "service_arms/deployment/deployment_types/kubernetes_utils/yaml_templates/{service_type}"
    
    
    def get_yamls(self, service_name):
        service_type = self.__class__.__name__.lower()
        folder_path = self.folder_path.format(service_type=service_type)
        folder = Folder(f"{service_name}_{service_type}")
        for file in os.listdir(folder_path):
            with open(f"{folder_path}/{file}") as f:
                file = File(file, f.read())
            folder.add_page(file)
        return folder
        

