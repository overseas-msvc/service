import importlib


# import service_arms.repo.repo_types as repo_types
from db_manage.mysql_connector.database import Database


def get_repo(repo_id):
    db = Database("Repo")
    repo = db.get_object_by_id("Repo", repo_id)
    repo_instance = db.get_object_by_id(repo.repo_type, repo.repo_id, inJson=True)
    repo_instance["repo_type"] = repo.repo_type
    return repo_instance

def write_repo_to_db(repo_info):
    db = Database("Repo")
    repo_type = repo_info["repo_type"]
    del repo_info["repo_type"]
    # createting GithubRepo
    repo_instance_id = db.add_object(repo_type, repo_info)
    # creating Repo
    repo_id = db.add_object("Repo", {"repo_type": repo_type, "repo_id": repo_instance_id})
    return repo_id

def create_repo(repo_id):
    db = Database("Repo")
    # getting GithubRepo object (the actual tasks enabler)
    repo = get_repo_obj(repo_id)
    repo_url = repo.create_repo()
    # update url
    db = Database("Repo")
    repo = db.get_object_by_id("Repo", repo_id)
    db.update_object(repo.repo_type, repo.repo_id, {"url": repo_url})


def add_exisiting_repo(repo_info):
    db = Database("Repo")
    db.add_object(repo_info)

def upload_files_to_github(repo_id, files):
    repo = get_repo_obj(repo_id)
    repo.upload_files_to_github(files)

def upload_file_to_github(repo_id, file):
    repo = get_repo_obj(repo_id)
    repo.upload_file_to_github(file)

def upload_folder_to_github(repo_id, folder):
    repo = get_repo_obj(repo_id)
    repo.upload_folder_to_github(folder)

def add_webhook(repo_id, host, ssl_disable=False):
    repo = get_repo_obj(repo_id)
    repo.add_webhook(host, ssl_disable)

##############################
def get_repo_obj(repo_id):
    db = Database("Repo")
    repo_info = db.get_object_by_id("Repo", repo_id)
    repo_type = repo_info.repo_type
    module = importlib.import_module(f"service_arms.repo.repo_types.{repo_type}")
    repo = getattr(module, repo_type)(repo_info.repo_id)
    return repo

