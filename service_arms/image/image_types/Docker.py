from db_manage.mysql_connector.database import Database


class Docker:
    def __init__(self, docker_image_id):
        db = Database("Image")
        docker_image = db.get_object_by_id("Docker", docker_image_id)
        self.image = docker_image.image