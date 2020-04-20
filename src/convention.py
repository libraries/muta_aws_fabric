import json
import os

import toml

with open("./bin/develop/config.toml", "r") as f:
    conf = toml.load(f)

a = json.dumps(conf, indent=4)
print(f"config = {a}")

aws_id_rsa = "./bin/develop/id_rsa"
aws_ip_node_list = conf["aws_ip_node_list"]
aws_ip_sync_list = conf["aws_ip_sync_list"]
aws_ip_send_list = conf["aws_ip_send_list"]

telegram_token = conf["telegram_token"]
telegram_chat_id = conf["telegram_chat_id"]

chain_param_interval = conf["chain_param_interval"]
chain_param_poolsize = conf["chain_param_poolsize"]
chain_param_timeout_gap = conf["chain_param_timeout_gap"]
chain_param_cycles_limit = conf["chain_param_cycles_limit"]
chain_param_tx_num_limit = conf["chain_param_tx_num_limit"]
chain_param_api_port = 8000
chain_param_p2p_port = 1337
chain_param_data_path = "/home/ubuntu/muta/data"
chain_param_logs_path = os.path.join(chain_param_data_path, "logs")


dockerhub_username = "mutadev"

muta_path = "/src/muta"
muta_genesis_template_path = os.path.join(muta_path, "devtools", "chain", "genesis.toml")
muta_config_template_path = os.path.join(muta_path, "devtools", "chain", "config.toml")

huobi_path = "/src/huobi-chain"
huobi_genesis_template_path = os.path.join(huobi_path, "config", "genesis.toml")
huobi_config_template_path = os.path.join(huobi_path, "config", "chain.toml")
