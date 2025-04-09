import requests
from db_manage.mysql_connector.database import Database
from service_comunications.connectors import get_connector


class DockerHub:
    def __init__(self, rgistry_id):
        db = Database("Image")
        registry = db.get_object_by_id("DockerHub", rgistry_id)
        self.connector = get_connector(registry.connector_id)
        self.address = self.connector["username"]
        self.token = self.connector["token"]

    def create_repository(self, image):
        image = image.lower()
        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        # Data for repository creation
        data = {
            "name": image,
            "is_private": False,  # Set to True for a private repo
            "namespace": self.address,
            "description": "My new Docker repository",
        }

        # Send POST request to create repository
        response = requests.post("https://hub.docker.com/v2/repositories/", json=data, headers=headers)

        # Check response
        if response.status_code == 201:
            print(f"Repository '{image}' created successfully!")
        else:
            print(f"Failed to create repository: {response.text}")

    
    def get_login_step(self):
        return f"echo $acr_pass | docker login --username $acr_user --password-stdin"