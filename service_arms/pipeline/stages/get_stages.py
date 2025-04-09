from service_arms.pipeline.stages.plugins.docker import get_docker_build
from service_arms.pipeline.stages.plugins.kubernetes import get_kubernetes_deploy
from service_arms.pipeline.stages.plugins.git import get_git_clone

from service_arms.pipeline.stages.objects.Stage import Stage


def get_clone(repo):
    clone = get_git_clone(repo)
    return clone; 

def get_build(build_type, artifact):
    match build_type:
        case "docker":
            build = get_docker_build(artifact)
    return build

def get_test(test_type):
    match test_type:
        case "pytest":
            test = Stage("test")
            test.steps.append("bat 'pytest --junitxml=report.xml'")
            test.steps.append("bat 'pytest --junitxml=report.xml'")
    return test; 


def get_deploy(deploy_type, deploy):
    # deploy = {"name": "Deploy", "steps":[]}
    match deploy_type:
        case "k8s":
            deploy = get_kubernetes_deploy(deploy)
            # deploy["steps"].append("echo 'connecting to kubernetes'") # connect to kubernetes cluster. 
            # deploy["steps"].append("echo 'kubectl apply -f deployment.yaml'")
    return deploy




