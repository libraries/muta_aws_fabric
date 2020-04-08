import datetime
import json
import subprocess
import time

import convention

for _ in range(1 << 32):
    for i in range(len(convention.aws_ip_node_list)):
        for j in range(len(convention.aws_ip_node_list)):
            if j == i:
                continue
            a = convention.aws_ip_node_list[i]
            b = convention.aws_ip_node_list[j]

            try:
                r = subprocess.getoutput(
                    f'ssh -o "StrictHostKeyChecking no" -i ./res/id_rsa ubuntu@{a} "./telnet/telnet_client -s {b}:4101"')
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
    time.sleep(10)
