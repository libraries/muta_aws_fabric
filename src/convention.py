import argparse
import json
import os

import toml

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="./res/config.toml", help="path of config file")
parser.add_argument("step", nargs="+", help="step name to run")
args = parser.parse_args()

with open(args.config, "r") as f:
    conf = toml.load(f)

a = json.dumps(conf, indent=4)
print(f"config = {a}")

aws_id_rsa = "./res/id_rsa"
aws_ip_node_list = conf["aws_ip_node_list"]
aws_ip_sync_list = conf["aws_ip_sync_list"]
aws_ip_send_list = conf["aws_ip_send_list"]
telegram_token = conf["telegram_token"]
telegram_chat_id = conf["telegram_chat_id"]
dockerhub_username = "mutadev"
muta_path = "/src/muta"
muta_genesis_template_path = os.path.join(muta_path, "devtools", "chain", "genesis.toml")
muta_config_template_path = os.path.join(muta_path, "devtools", "chain", "config.toml")
muta_data_path = "/tmp/muta"
muta_logs_path = os.path.join(muta_data_path, "logs")
muta_api_port = 8000
muta_p2p_port = 1337
