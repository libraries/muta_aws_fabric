import os
import subprocess

import convention
import misc


def huobi_binary():
    with misc.chdir(convention.huobi_path):
        misc.call("cargo build --release")
    with misc.chdir(os.path.join(convention.muta_path, "./devtools/keypair")):
        misc.call("cargo build --release")

    misc.call("rm -rf build")
    misc.call("mkdir -p build")
    a = os.path.join(convention.muta_path, "target/release/muta-keypair")
    misc.call(f"cp {a} ./build")
    a = os.path.join(convention.huobi_path, "target/release/huobi-chain")
    misc.call(f"cp {a} ./build")
