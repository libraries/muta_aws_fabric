import json
import sys
import subprocess

import requests

import convention
import misc


def aws_bench():
    url = misc.recv_str_from_stdin("url", "http://127.0.0.1:8000/graphql")
    while True:
        output = subprocess.getoutput(f"muta-bench -g 999999 -d 600 --cpu 8 --json {url}")
        last = output.splitlines()[-1]
        data = json.loads(last)
        blocks = data["blocks"]
        msgs = {
            "avg_round": sum([e[2] for e in blocks]) / len(blocks),
            "tx/block": data["tx_block"],
            "sec/block": data["sec_block"],
            "tx/sec": data["tx_sec"],
        }
        requests.post(f"https://api.telegram.org/bot{convention.telegram_token}/sendMessage", data={
            "chat_id": convention.telegram_chat_id,
            "text": json.dumps(msgs, indent=4),
        })
