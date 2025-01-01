---
date: "2024-04-23"
layout: post
title: "TIL: how to create and work with remote blob storage on Azure"
categories: [code, cloud]
image: None
---

In this TIL, I find out how to create a new blob storage account on Microsoft Azure. This is a place to store unstructured data of any kind (as opposed to, say, a SQL database).

Note that the instructions below assume you are using a bash-like terminal, for example [zsh](https://ohmyz.sh/), rather than [Powershell](https://learn.microsoft.com/en-us/powershell/).

## Prerequisites

You'll need to sign up for a Microsoft Azure account for this, and create a "resource group". You'll also need the Azure Command Line Interface (CLI), which you can find information [on here](https://learn.microsoft.com/en-us/cli/azure/). (Alternatively, you can do this through the [Azure Portal](https://portal.azure.com/#home), but it's often useful to have the reproducible commands.)

It's also helpful to understand the lingo Azure uses for storage.

- storage accounts are the high level service
- "storage containers" are specific data-holding entities that contain blob storage, that is data of any shape and size

## Instructions

### Creating a storage account with the command line interface

First set and load your configs. Note that the storage account name must be between 3 and 24 characters in length and use numbers and lower-case letters only.

```bash
storagename=<>
resourcegroup=<>
location=<> # eg "uksouth"
sku="Standard_LRS" # Standard Locally Redundant Storage
```

Then to create the blob, it's

```bash
az storage account create --name $storagename --resource-group $resourcegroup --location $location --sku $sku --encryption-services blob
```

If this has worked, you'll get a JSON structure back that looks something like this:

```text
{
  "accessTier": "Hot",
  "accountMigrationInProgress": null,
  "allowBlobPublicAccess": false,
  "allowCrossTenantReplication": false,
  "allowSharedKeyAccess": null,
  "allowedCopyScope": null,
  "azureFilesIdentityBasedAuthentication": null,
  "blobRestoreStatus": null,
  "creationTime": "<>",
  "customDomain": null,
  "defaultToOAuthAuthentication": null,
  "dnsEndpointType": null,
  "enableHttpsTrafficOnly": true,
  "enableNfsV3": null,
  "extendedLocation": null,
  "failoverInProgress": null,
  "geoReplicationStats": null,
  "id": "/subscriptions/<>/resourceGroups/<>/providers/Microsoft.Storage/storageAccounts/<>",
  "identity": null,
  "immutableStorageWithVersioning": null,
  "isHnsEnabled": null,
  "isLocalUserEnabled": null,
  "isSftpEnabled": null,
  "isSkuConversionBlocked": null,
  "keyPolicy": null,
  "kind": "StorageV2",
  "largeFileSharesState": null,
  "lastGeoFailoverTime": null,
  "location": "uksouth",
  "minimumTlsVersion": "TLS1_0",
  "name": "<>",
  "networkRuleSet": {
    "bypass": "AzureServices",
    "defaultAction": "Allow",
    "ipRules": [],
    "ipv6Rules": [],
    "resourceAccessRules": null,
    "virtualNetworkRules": []
  },
  "primaryEndpoints": {
    "blob": "https://<>.blob.core.windows.net/",
    "dfs": "https://<>.dfs.core.windows.net/",
    "file": "https://<>.file.core.windows.net/",
    "internetEndpoints": null,
    "microsoftEndpoints": null,
    "queue": "https://<>.queue.core.windows.net/",
    "table": "https://<>.table.core.windows.net/",
    "web": "https://<>.z33.web.core.windows.net/"
  },
  "primaryLocation": <>,
  "privateEndpointConnections": [],
  "provisioningState": "Succeeded",
  "publicNetworkAccess": null,
  "resourceGroup": "inv-day-test",
  "routingPreference": null,
  "sasPolicy": null,
  "secondaryEndpoints": null,
  "secondaryLocation": null,
  "sku": {
    "name": "Standard_LRS",
    "tier": "Standard"
  },
  "statusOfPrimary": "available",
  "statusOfSecondary": null,
  "storageAccountSkuConversionStatus": null,
  "tags": {},
  "type": "Microsoft.Storage/storageAccounts"
}
```

### Assign permission to use the storage account

Right now, you've created a storage account, but you don't have permission to use it! Let's change that by adding the current user to have the role assignment "Storage Blob Data Contributor".

```bash
subscriptionid=<>  # long combination of numbers and letters with dashes

az ad signed-in-user show --query id -o tsv | az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee @- \
    --scope "/subscriptions/$subscriptionid/resourceGroups/$resourcegroup/providers/Microsoft.Storage/storageAccounts/$storagename"
```

Note that we already saved the other variables. Running this should result in another JSON file full of info.

### Creating a storage container using the CLI

Next up, we want to create a storage container. 

```bash
containername=<>  # eg "mydemocontainer"

az storage container create \
    --account-name $storagename \
    --name $containername \
    --auth-mode login
```

Once this runs you should get a little JSON saying

```text
{
  "created": true
}
```

### How to upload a file to blob storage

Now we need a text file to try out "mydemocontainer" or whatever you called it in `containername`. To create one, use

```bash
echo "hello world" >> test.txt
```

this creates the file `test.txt` locally. To then upload it to your storage container as `test_on_blob.txt`, use the below:

```bash
az storage blob upload --account-name $storagename --container-name $containername --name test_on_blob.txt --file test.txt --auth-mode login
```

### Checking it worked

Of course, you can check this in the Azure Portal. But to check it on the command line, it's

```bash
az storage blob list --account-name $storagename --container-name $containername --output table --auth-mode login
```

which should result in a table showing a single file, `test_on_blob.txt`.

### Download data back from the blob

For this, we'll use the `az storage blob download` command.

```bash
az storage blob download --account-name $storagename --container-name $containername --name test_on_blob.txt --file back_from_blob.txt --auth-mode login
```

That's it! The general setup is the same. For transferring lots of files, you may want to check out the [azcopy](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) utility too. There are also [Python libraries](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) for interacting with blob storage.
