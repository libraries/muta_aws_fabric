# Muta aws fabric

# Usage

First, initial the environment:

```sh
$ mkdir -p ./bin/develop
$ cp ./res/config.toml ./bin/develop
$ cp xxx/id_rsa ./bin/develop
$ cp xxx/id_rsa.pub ./bin/develop
```

```sh
# clone the muta repo, switch to your branch or commit at /src
$ git clone https://github.com/nervosnetwork/muta.git
$ vim ./bin/develop/config.toml # replace the muta path in config file

$ export CONFIG=./bin/develop/config.toml
# deploy muta in one line. If execute this command twice, the previous chain will be free.
$ py src/main.py muta
# stop the chain
$ py src/main.py muta_remote_kill
```

command `muta` is an aggregated command, it will execute a subcommand (you can execute it separately):

- `muta_build_binary`
- `muta_build_config`
- `muta_deploy_binary`
- `muta_remote_run`

You can also use the `muta_remote_kill` command to kill all muta processes.

For easy machine management, there is a powerful command `aws_bash`, it will execute every command you input to every machine:

```sh
$ py src/main.py aws_bash
# install curl on all boxes
> apt install -y curl
```

# Telnet: network infomation between nodes

```sh
$ py src/main.py telnet_build_binary
$ py src/main.py telnet_deploy
$ py src/main.py telnet_server_run
$ py src/main.py telnet_monitor
```

The script will print the speed and delay between any two nodes.

# FD

Tips for how to set file descriptions.

```sh
$ sudo bash -c 'echo -n "fs.file-max = 65535" >> /etc/sysctl.conf'
$ sudo bash -c 'echo -n "* soft  nofile 65535" >> /etc/security/limits.conf'
$ sudo bash -c 'echo -n "* hard nofile 65535" >> /etc/security/limits.conf'

$ sysctl -p
$ cat /proc/sys/fs/file-max
```

```sh
$ ls -l /proc/pid/fd/
```
