---
date: "2024-03-08"
layout: post
title: "TIL: how to connect Visual Studio Code to Azure Virtual Machines"
categories: [code, research, cloud, python, rstats]
---

In a previous blog post, I looked at [how to connect desktop-based Visual Studio Code to a Google Cloud Virtual machine](../visual-studio-code-in-the-cloud/index.md); today, it's how to do the same using a virtual machine running on Microsoft's Azure platform.

## Setting Up

There are two pieces to this puzzle: Visual Studio Code and the Azure Cloud Platform.

First, grab Visual Studio Code for your local computer (ie your non-cloud computer) and whatever extensions you fancy, but you'll need [the remote explorer (SSH)](https://code.visualstudio.com/docs/remote/ssh) at a minimum.

You'll also need to sign up for a Microsoft Azure account and get either the free tier of services or activate a pay-as-you-go account. Be warned: if you have multiple Microsoft accounts for home and work, this can be a frustrating and circular process where you are constantly signing in and being taken to different accounts.

With that in place, there are two ways to proceed to create your Azure infrastructure: you can either use the Azure Command Line Interface (CLI), which you can find information [on here](https://learn.microsoft.com/en-us/cli/azure/) or use the [Azure website](https://portal.azure.com/#home) directly.

## Creating a Cloud VM Instance

### Using the website

On the [Azure website](https://portal.azure.com/#home), navigate to the "Virtual Machines" resources page and hit create. There are a couple of options, but if you're just trying this out you might like to use one of the pre-configured machines. I used one of the pre-configured D-Series computers and chose Linux (Ubuntu) as the operating system. You'll need to set your subscription and resource group from the drop-down menu. Give the virtual machine a name, choose the region closest to you, and feel free to use the defaults for most of the other options. There is a box for a username: note that this is what your ID will be on the virtual machine once it's created. Choose SSH as the authentication type and give the file a name. Hit review and create! Make sure to save the private key certificate, the ".pem" file, to somewhere sensible on your local machine. This file is what will let you remotely access the virtual machine from your computer via Visual Studio Code.

There is an important extra step here, at least on MacOS. The certificate file that you've just downloaded will be set so that everyone has read and write permissions. When you later try to connect via SSH, this will raise alarm bells. So you want to set it so that only the Mac's current user, you, can read and write it. To do this, navigate to the file in the command line and then run

```bash
chmod 600 my-certificate-name.pem
```

### Using the command line interface

Let's now see how to do this using the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) instead. Follow the install instructions for your system. In the following, I'll assume you already have a resource group set up. Use `az login` to login to your cloud account.

Then the command to create a virtual machine (running Ubuntu 22.04.4 LTS with 2 cores and 8GB of RAM) is:

```bash
resourcegroup="RESOURCE-GROUP"
vmname="VIRTUAL-MACHINE-NAME"
username="USERNAME"
az vm create --resource-group $resourcegroup --name $vmname --image Ubuntu2204 --admin-username $username --size Standard_D2ds_v4 ----generate-ssh-keys
```

You can see a summary list of available images by running `az vm image list`. To get the full, live list of Ubuntu options it would be `az vm image list -f Ubuntu --all` but note that this could take a long time to run. For more powerful computers, select another size (you can see the available ones using `az vm list-sizes --location REGION --output table` but you'll have to check the website for prices.

If the `create` command is successful, you should see something a bit like the following appear:

```text
{
  "fqdns": "",
  "id": "/subscriptions/YOUR-SUBSCRIPTION-ID/resourceGroups/RESOURCE-GROUP/providers/Microsoft.Compute/virtualMachines/VIRTUAL-MACHINE-NAME",
  "location": REGION,
  "macAddress": AN-ID,
  "powerState": "VM running",
  "privateIpAddress": "X.X.X.X",
  "publicIpAddress": "X.X.X.X",
  "resourceGroup": RESOURCE-GROUP,
  "zones": ""
}
```

Note that you should also get a public SSH key back from this operation, which by default is saved as a .pem file in `~/.ssh` on your local machine.

## Connecting to a running Azure Virtual Machine Instance from Visual Studio Code

Okay, so your Azure VM instance is running and now you're going to connect to it with Visual Studio Code.

First, we need to set up the SSH connection between your computer and your running cloud VM; essentially a way for them to talk to each other. You can find out more about SSH authentication [here](https://www.ssh.com/academy/ssh/protocol). On the Azure website, and looking at your virtual machine, click on the "connect" button. You'll then see two options: use "Native SSH". When you click on Native, you'll see a panel open up on the right-hand side (as long as your virtual machine is already running). You'll see a command a bit like:

```bash
ssh -i ~/.ssh/id_rsa.pem VM-USERNAME@VM-IP-ADDRESS
```

Essentially, what this is saying is that to SSH into your running virtual machine from the command line, you'll need to use the SSH command passing in as arguments both the location of your ".pem" certificate, which should only be read/write by you, and then the username you used for the VM followed by the public IP address of the VM, which you can see in the panel.

You could just run this on the command line and connect that way. But to get all the goodies of Visual Studio Code, it's a slightly different process.

Within Visual Studio Code on your local computer, go to the remote explorer tab, which you can find on the left hand side (you'll need to have installed the remote explorer package for SSH). Choose 'SSH Targets' from the drop-down menu at the top. Click the "+" button next to SSH and then paste in the SSH command. Hit refresh on the remotes panel, and you should now see a new entry for your virtual machine. Right click on it and select "Connect in New Window" to get Visual Studio Code to connect.

Congratulations, you should now be on your VM instance using Code! You can check because the green text in the bottom left-hand corner of Visual Studio Code should read

> SSH: VIRTUAL-MACHINE-NAME

And the command prompt in the new VS Code window should say something like `USERNAME@VIRTUAL-MACHINE-NAME:~$`.

For more instructions, including installing Python and git, check out the [original post on this with Google Cloud](../visual-studio-code-in-the-cloud/index.md).

## Finishing

Remember: best practice is to treat a cloud instance as temporary. Shunt data you want to save in and out when you use it, and use version control for code. And most of all, **don't forget to turn your VM instance off when you've finished using it!**

Hopefully this has been a useful summary of how to use Visual Studio Code in the (Azure!) cloud. Happy coding!
