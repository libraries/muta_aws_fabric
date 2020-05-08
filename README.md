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
