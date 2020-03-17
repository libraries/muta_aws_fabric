import copy
import json
import subprocess
import toml

import convention
import misc


def huobi_config():
    interval = misc.recv_int_from_stdin("interval", 3000)
    poolsize = misc.recv_int_from_stdin("poolsize", 200000)
    timeout_gap = misc.recv_int_from_stdin("timeout_gap", 999999)
    cycles_limit = misc.recv_int_from_stdin("cycles_limit", 630000000)
    tx_num_limit = misc.recv_int_from_stdin("tx_num_limit", 30000)

    node_num = len(convention.aws_ip_node_list) + len(convention.aws_ip_sync_list)
    r = subprocess.getoutput(f"./build/muta-keypair -n {node_num}")
    with open("./build/keypairs.json", "w") as f:
        f.write(r)
    keypair_list = json.loads(r)

    assert "common_ref" in keypair_list
    for e in keypair_list["keypairs"]:
        assert "private_key" in e
        assert "public_key" in e
        assert "address" in e
        assert "bls_public_key" in e

    genesis = toml.load(convention.huobi_genesis_template_path)
    assert genesis["services"][1]["name"] == "metadata"
    payload = json.loads(genesis["services"][1]["payload"])
    payload["common_ref"] = keypair_list["common_ref"]
    payload["timeout_gap"] = timeout_gap
    payload["cycles_limit"] = cycles_limit
    payload["tx_num_limit"] = tx_num_limit
    payload["interval"] = interval
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
    with open("./build/genesis.toml", "w") as f:
        toml.dump(genesis, f)

    config_template = toml.load(convention.huobi_config_template_path)
    for i, e in enumerate(convention.aws_ip_node_list + convention.aws_ip_sync_list):
        node_config = copy.deepcopy(config_template)
        keypair = keypair_list["keypairs"][i]
        node_config["privkey"] = keypair["private_key"]
        node_config["data_path"] = convention.muta_data_path
        node_config["graphql"]["listening_address"] = "0.0.0.0:" + str(convention.muta_api_port)
        node_config["network"]["listening_address"] = "0.0.0.0:" + str(convention.muta_p2p_port)
        node_config["logger"]["log_path"] = convention.muta_logs_path
        node_config["mempool"]["pool_size"] = poolsize
        node_config["network"]["bootstraps"] = [{
            "pubkey": keypair_list["keypairs"][0]["public_key"],
            "address": convention.aws_ip_node_list[0] + ":" + str(convention.muta_p2p_port),
        }]

        with open(f"./build/config_{i+1}.toml", "w") as f:
            toml.dump(node_config, f)
