import os
import subprocess

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from .utilities import loadConfiguration, checkFileStatus, get_relative_path


class LFSBlobClient(BlobServiceClient):
    def __init__(self, configurationFile='/etc/az_lfs_hsm_remove.json', **kwargs) -> None:
        configuration = loadConfiguration(configurationFile)
        self.accountURL = configuration.get('accountURL')
        self.containerName = configuration.get('containerName')
        super().__init__(self.accountURL, credential=DefaultAzureCredential(exclude_workload_identity_credential=True, exclude_environment_credential=True), **kwargs)

    def lfs_hsm_remove(self, filePath):
        absolutePath = os.path.abspath(filePath)
        if checkFileStatus(absolutePath):
            client = self.get_blob_client(container=self.containerName, blob=get_relative_path(absolutePath))
            client.delete_blob()
            subprocess.check_output(["lfs", "hsm_set", "--lost", absolutePath])
            subprocess.check_output(["lfs", "hsm_set", "--dirty", absolutePath])