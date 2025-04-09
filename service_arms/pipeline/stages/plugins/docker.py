from service_arms.pipeline.stages.objects.Stage import Stage
from service_arms.pipeline.stages.objects.Script import Script
from service_comunications.connectors import get_connector

from service_arms.pipeline.stages.objects.credentials.userCredential import UserCredential


def get_docker_build(artifact):
    build = Stage("Build")
    registry_connctor = get_connector(artifact["registry"]["connector_id"])
    tag = f"{registry_connctor['username']}/{artifact['image']['image'].lower()}:1.$BUILD_NUMBER"
    build.credentials.append(UserCredential(registry_connctor["username"], registry_connctor["token"], "acr_login"))
    # service.pipeline.install_jenkins_plugin("Docker Pipeline")
    docker_script = Script()
    docker_script.commands.append(f"docker.withRegistry('', 'acr_login') {{\n\t\t\t\t\t\tdef dockerImage = docker.build(\"{tag}\")\n\t\t\t\t\t\tdockerImage.push()\n\t\t\t\t\t}}")
    build.steps.append(docker_script)
    return build