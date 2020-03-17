# Opus!

# 设置 FD

```sh
$ sudo bash -c 'echo -n "fs.file-max = 65535" >> /etc/sysctl.conf'
$ sudo bash -c 'echo -n "* soft  nofile 65535" >> /etc/security/limits.conf'
$ sudo bash -c 'echo -n "* hard nofile 65535" >> /etc/security/limits.conf'

$ sysctl -p
$ cat /proc/sys/fs/file-max
```

# 查询进程占用的 FD

```sh
$ ls -l /proc/pid/fd/
```
