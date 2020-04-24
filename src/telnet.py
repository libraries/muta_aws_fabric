import os
import datetime
import json
import subprocess
import time

import aws_pool
import convention
import misc


def build_binary():
    os.makedirs('./bin/telnet', exist_ok=True)
    with misc.chdir('./telnet'):
        misc.call('go build -o ../bin/telnet/ github.com/libraries/muta_aws_fabric/telnet/cmd/server')
        misc.call('go build -o ../bin/telnet/ github.com/libraries/muta_aws_fabric/telnet/cmd/client')


def deploy_binary():
    aws_pool.make_pool()
    aws_pool.pool.run(f"rm -rf telnet")
    aws_pool.pool.run(f"mkdir -p telnet")
    for e in aws_pool.pool:
        print(f"{e.host} upload telnet binaries")
        e.put("./bin/telnet/server", "telnet/telnet_server")
        e.put("./bin/telnet/client", "telnet/telnet_client")


def remote_kill():
    aws_pool.make_pool()
    aws_pool.pool.run("killall telnet_server | tee")


def remote_run():
    remote_kill()
    aws_pool.pool.run("setsid telnet/telnet_server -l :4101 >/dev/null 2>&1 &")


def monitor():
    for _ in range(1 << 32):
        print("=" * 80)
        for i in range(len(convention.aws_ip_node_list)):
            for j in range(len(convention.aws_ip_node_list)):
                if j == i:
                    continue
                a = convention.aws_ip_node_list[i]
                b = convention.aws_ip_node_list[j]

                try:
                    r = subprocess.getoutput(
                        f'ssh -o "StrictHostKeyChecking no" -i ./bin/develop/id_rsa ubuntu@{a} "./telnet/telnet_client -s {b}:4101"')
                    r = r.split()
                    print(json.dumps({
                        'time': str(datetime.datetime.now()),
                        'from': a,
                        'to': b,
                        'handshake': int(r[0]),
                        'pingpong': int(r[1]),
                        'speed': 1000 / float(r[2]),
                    }))
                except Exception as e:
                    print(json.dumps({
                        'time': str(datetime.datetime.now()),
                        'from': a,
                        'to': b,
                        'error': str(e),
                    }))
        print("=" * 80)
        time.sleep(300)
