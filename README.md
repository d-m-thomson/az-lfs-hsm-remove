# Azure LFS HSM Remove
This repository contains an implementation to allow hsm-remove on Azure Managed Lustre.

# Prerequisites

This utilities rely on a Managed Identity with propoer permissions on the Azure Blob Storage acting as Lustre HSM backend.

More specifically it requires:
* A managed identity with Storage Blob Data Contributor role on the relevant container for Lustre HSM
* A configuration file in `/etc/az_lfs_hsm_remove.json` containing account URL and container name, with the following format:

```json
{
    "accountURL": "https://<STORAGE_ACCOUNT_NAME>.blob.core.windows.net/",
    "containerName": "<LUSTRE_HSM_CONTAINER_NAME>"
}
```

## Installation

Ideally, this package is meant to run on Python 3. It is suggested to create a virtual environment, for example:

```bash
python3 -m venv $HOME/az_lfs
source $HOME/az_lfs/bin/activate
```

To install the package, download the wheel from the Releases and just perform:

```bash
source $HOME/az_lfs/bin/activate
pip install <WHEEL_FILE>
```

In case you get error in `cryptography` installation, just perform an upgrade of `pip`:

```bash
source $HOME/az_lfs/bin/activate
pip install --upgrade pip
pip install <WHEEL_FILE>
```

## Usage

In order to remove a file from the Lustre backend, the file should be released on the Lustre file system. If that is not the case, the command will print an error and it won't perform any operation

```bash
az_lfs_hsm_remove <file_path>
```

In some cases, it may also be necessary to remove a file from the backend after the original file on the Lustre file system has been removed. This can be done with the -c or --cleanup option. To avoid accidental deletion of backend data, the command will print an error and won't perform any operation if the specified file still exists on the Lustre file system

```bash
az_lfs_hsm_remove --cleanup <original_file_path>
```
## Deleted HSM files

The files that are delated from HSM will be marked with `lfs hsm_state` as lost and dirty. This means that deleting from Lustre FileSystem will cause total lost of date.

If another copy requires archival, it can be restored with `lfs hsm_archive`. After the command is triggered, the `lfs hsm_state` should return a clean state.


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.