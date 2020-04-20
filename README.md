# Muta aws fabric

# Usage

```sh
$ mkdir -p ./bin/develop
$ cp ./res/config.toml ./bin/develop
$ cp xxx/id_rsa ./bin/develop
$ cp xxx/id_rsa.pub ./bin/develop
```

```sh
# deploy muta in one line
$ py src/main.py muta

# deploy huobi-chain in one line
$ py src/main.py huobi

# deploy telnet in one line
$ py src/main.py telnet_deploy telnet_server_run
```

# FD

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
