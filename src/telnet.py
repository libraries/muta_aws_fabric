import aws_pool
import misc


def deploy_binary():
    aws_pool.make_pool()
    aws_pool.pool.run(f"rm -rf telnet")
    aws_pool.pool.run(f"mkdir -p telnet")
    for e in aws_pool.pool:
        print(f"{e.host} upload telnet binaries")
        e.put("telnet/bin/server", "telnet/telnet_server")
        e.put("telnet/bin/client", "telnet/telnet_client")


def remote_kill():
    aws_pool.make_pool()
    aws_pool.pool.run("killall telnet_server | tee")


def remote_run():
    remote_kill()
    aws_pool.pool.run("setsid telnet/telnet_server -l :4101 >/dev/null 2>&1 &")
