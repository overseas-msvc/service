from service_arms.repo.repo import create_repo, get_repo, upload_folder_to_github, get_repo_obj, write_repo_to_db, \
                                   upload_files_to_github, add_webhook
from service_arms.deployment.deployment import get_yamls, get_deployment, write_deployment_to_db
from service_arms.pipeline.pipeline import create_pipeline, get_pipeline_obj, write_pipeline_to_db, \
    trigger_pipeline, get_host
from service_arms.image.image import write_image_to_db, create_registry_repository, get_artifact
from service_arms.endpoints.endpoints import write_endpoints_to_db, get_endpoints
from service_arms.code.code import write_code_to_db, get_files
from service_arms.test.test import get_test_files, write_test_to_db
from db_manage.mysql_connector.database import Database

from folder.Folder import Folder

class Service:

    def __init__(self, id):
        db = Database("Service")
        service = db.get_object_by_id("Service", id)
        self.id = id
        self.name = service.name
        self.version = service.version
        self.project_id = service.project_id
        self.ids = db.get_object_by_id(service.service_type, service.service_id)

    def write_to_db(service_info):
        service = {}
        service_type = service_info["service_type"]

        service["repo_type"] = service_info["repo"]["repo_type"]
        service["repo_id"] = write_repo_to_db(service_info["repo"])

        service["image_type"] = service_info["image"]["image_type"]
        service["image_id"] = write_image_to_db(service_info["image"])

        service["deployment_type"] = service_info["deployment"]["deployment_type"]
        service["deployment_id"] = write_deployment_to_db(service_info["deployment"])

        service["code_type"] = service_info["code"]["code_type"]
        service["code_id"] = write_code_to_db(service_info["code"])

        service["test_type"] = service_info["test"]["test_type"]
        service["test_id"] = write_test_to_db(service_info["test"])
        
        service["pipeline_type"] = service_info["pipeline"]["pipeline_type"]
        service["pipeline_id"] = write_pipeline_to_db(service_info["pipeline"])

        
        db = Database("Service")
        service_id = db.add_object(service_type, service)
        service_id = db.add_object("Service", {
            "name": service_info["name"],
            "service_type": service_type,
            "service_id": service_id,
            "project_id": service_info["project_id"],
            "version": service_info["version"]
        })
        write_endpoints_to_db(service_info["endpoints"], service_id)
        return service_id

    def create_service(self, trigger=True):
        # create_repo(self.ids.repo_id)
        # create_registry_repository(self.ids.image_id)
        # self.upload_infrastucture_folder()
        # self.upload_code_files()
        # self.upload_test_files()
        # create_pipeline(self.ids.pipeline_id, {
        #     "name": self.name,
        #     "repo": get_repo(self.ids.repo_id),
        #     "deployment": get_deployment(self.ids.deployment_id),
        #     "artifact": get_artifact(self.ids.image_id)
        # })
        self.add_repo_webhook()
        if trigger:
            trigger_pipeline(self.ids.pipeline_id, self.name)

    def add_repo_webhook(self):
        pipeline_host = get_host(self.ids.pipeline_id)
        add_webhook(self.ids.repo_id, f"{pipeline_host}/github-webhook/")


    def upload_infrastucture_folder(self):
        infrastructure_folder = Folder("infrastructure")
        yamls = get_yamls(self.ids.deployment_id, self.name)
        infrastructure_folder.add_folders(yamls)
        upload_folder_to_github(self.ids.repo_id, infrastructure_folder)

    def upload_code_files(self):
        endpoints = get_endpoints(self.id)
        files = get_files(self.ids.code_id, endpoints)
        upload_files_to_github(self.ids.repo_id, files)

    def upload_test_files(self):
        endpoints = get_endpoints(self.id)
        files = get_test_files(self.ids.test_id, self.ids.code_id, endpoints)
        upload_files_to_github(self.ids.repo_id, files)
