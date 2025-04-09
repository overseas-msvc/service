
from service_arms.pipeline.stages.objects.Stage import Stage
from service_arms.pipeline.stages.objects.credentials.SecretFile import SecretFile
from service_comunications.connectors import get_file_from_connector
from folder.Folder import File

def get_kubernetes_deploy(deployment):
    # service.pipeline.install_jenkins_plugin("Kubernetes Continuous Deploy Plugin")
    deploy = Stage("Deploy")
    ###testing mode
    kubeconfig = get_file_from_connector(deployment["connector_id"], "kubeconfig")
    ###end
    deploy.credentials.append(SecretFile(File("kubeconfig", kubeconfig["file_content"].encode('utf-8')), "kubeconfig"))
    step = f"""withKubeConfig([credentialsId: 'kubeconfig']) {{
					powershell '''
						kubectl create namespace {deployment['namespace']}
                        $yamlFiles = Get-ChildItem -Path 'infrastructure/' -Filter "*.yaml" -Recurse
                        foreach ($yamlFile in $yamlFiles) {{
                            (Get-Content $yamlFile.FullName) -replace '&lt;version&gt;', $env:BUILD_NUMBER | Set-Content $yamlFile.FullName
                            Write-Host "Applying: $yamlFile"
                            kubectl apply -f $yamlFile.FullName --namespace {deployment['namespace']}
                        }}
					'''
				    }}"""
    deploy.steps.append(step)
    return deploy