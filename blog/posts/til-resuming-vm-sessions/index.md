---
date: "2025-01-01"
layout: post
title: "TIL: How to resume sessions on virtual machines"
categories: [code, cloud, TIL]
---

Today I learned how to resume sessions on virtual machines while using Visual Studio Code remote.

[Visual Studio Code remote](https://code.visualstudio.com/docs/remote/remote-overview) is incredible for SSH-ing into remote virtual machines. But sometimes you start off a long-running process in a shell on the remote machine and your connection is interrupted before it can finish; then, when you resume the connection, you've lost the progress you made through your code.

But today I learned that you can start off *persistent* shell processes using a command line tool called **screen** that comes pre-installed in many Linux distributions (eg Ubuntu).

To use it (assuming it is pre-installed), once you've opened the folder you're working in on the remote via SSH from VS Code, simply type

```bash
screen -S YOUR-SHELL-NAME
```

to initiate a shell with screen name `YOUR-SHELL-NAME` that will persist.

Once you reconnect to the virtual machine run `screen -ls` to see existing running shells and `screen -r YOUR-SHELL-NAME` to reconnect to the running session! Super useful.
