import copy
import os
import subprocess

import json
import toml

import aws_pool
import convention
import misc


def build_binary():
    with misc.chdir(convention.huobi_path):
        misc.call("unset ROCKSDB_LIB_DIR && cargo build --release")
        with misc.chdir("./devtools/keypair"):
            misc.call("cargo build --release")

    misc.call("rm -rf ./bin/huobi")
    misc.call("mkdir -p ./bin/huobi")

    a = os.path.join(convention.huobi_path, "target/release/muta-keypair")
    misc.call(f"cp {a} ./bin/huobi")
    a = os.path.join(convention.huobi_path, "target/release/huobi-chain")
    misc.call(f"cp {a} ./bin/huobi")


def build_config():
    node_num = len(convention.aws_ip_node_list) + len(convention.aws_ip_sync_list)
    r = subprocess.getoutput(f"./bin/huobi/muta-keypair -n {node_num}")
    with open("./bin/huobi/keypairs.json", "w") as f:
        f.write(r)
    keypair_list = json.loads(r)

    genesis = toml.load(convention.huobi_genesis_template_path)
    assert genesis["services"][1]["name"] == "metadata"
    payload = json.loads(genesis["services"][1]["payload"])
    payload["common_ref"] = keypair_list["common_ref"]
    payload["timeout_gap"] = convention.chain_param_timeout_gap
    payload["cycles_limit"] = convention.chain_param_cycles_limit
    payload["tx_num_limit"] = convention.chain_param_tx_num_limit
    payload["interval"] = convention.chain_param_interval
    payload["verifier_list"] = []

    for i in range(len(convention.aws_ip_node_list)):
        e = keypair_list["keypairs"][i]
        a = {
            "bls_pub_key":  e["bls_public_key"],
            "address": e["address"],
            "propose_weight": 1,
            "vote_weight": 1,
        }
        payload["verifier_list"].append(a)
    genesis["services"][1]["payload"] = json.dumps(payload)
    with open("./bin/huobi/genesis.toml", "w") as f:
        toml.dump(genesis, f)

    config_template = toml.load(convention.huobi_config_template_path)
    for i, e in enumerate(convention.aws_ip_node_list + convention.aws_ip_sync_list):
        node_config = copy.deepcopy(config_template)
        keypair = keypair_list["keypairs"][i]
        node_config["privkey"] = keypair["private_key"]
        node_config["data_path"] = convention.chain_param_data_path
        node_config["graphql"]["listening_address"] = "0.0.0.0:" + str(convention.chain_param_api_port)
        node_config["network"]["listening_address"] = "0.0.0.0:" + str(convention.chain_param_p2p_port)
        node_config["logger"]["log_path"] = convention.chain_param_logs_path
        node_config["mempool"]["pool_size"] = convention.chain_param_poolsize
        node_config["rocksdb"]["max_open_files"] = convention.chain_param_rocksdb_max_openfile
        node_config["network"]["bootstraps"] = [{
            "pubkey": keypair_list["keypairs"][0]["public_key"],
            "address": convention.aws_ip_node_list[0] + ":" + str(convention.chain_param_p2p_port),
        }]
        node_config["apm"] = {}
        node_config["apm"]["service_name"] = f'huobi_{i+1}'
        node_config["apm"]["tracing_address"] = convention.chain_param_apm_tracing_address
        node_config["apm"]["tracing_batch_size"] = convention.chain_param_apm_tracing_batch_size

        with open(f"./bin/huobi/config_{i+1}.toml", "w") as f:
            toml.dump(node_config, f)


def deploy_binary():
    aws_pool.make_pool()
    with misc.chdir("./bin"):
        misc.call("python3 -m zipfile -c huobi.zip huobi")
        aws_pool.pool.run(f"rm -rf {convention.remote_path}/huobi")
        aws_pool.pool.run("rm -rf /tmp/huobi.zip")
        for e in aws_pool.pool:
            print(f"{e.host} upload huobi.zip")
            e.put("huobi.zip", "/tmp/huobi.zip")
    aws_pool.pool.run(f"python3 -m zipfile -e /tmp/huobi.zip {convention.remote_path}")
    aws_pool.pool.run(f"cd {convention.remote_path}/huobi && chmod +x huobi-chain && chmod +x muta-keypair")


def remote_kill():
    aws_pool.make_pool()
    aws_pool.pool.run(f"cd {convention.remote_path}/huobi && kill -2 `cat huobi.pid` || true")


def remote_run():
    aws_pool.make_pool()
    aws_pool.pool.run(f"rm -rf {convention.chain_param_data_path}")
    for i, e in enumerate(aws_pool.pool):
        print(f"{e.host} start huobi-chain")
        e.run(f"cd {convention.remote_path}/huobi && (nohup ./huobi-chain -c config_{i+1}.toml -g genesis.toml >& log < /dev/null & echo $! > huobi.pid) && sleep 1")
