from service_arms.pipeline.stages.objects.Stage import Stage
from service_arms.pipeline.stages.objects.credentials.userCredential import UserCredential
from service_comunications.connectors import get_connector


def get_git_clone(repo):
    clone = Stage("Clone Repository")
    repo_connctor = get_connector(repo["connector_id"])
    if repo["repo_type"] == "GithubRepo":
        # clone.credentials.append(GithubAppCredential(service.repo.app_id, service.repo.key_path))
        clone.credentials.append(UserCredential(repo_connctor["username"], repo_connctor["pat"], "github_pat"))
        clone.steps.append(f"git branch: 'main', credentialsId: 'github_app', url: '{repo['url']}'")
    return clone