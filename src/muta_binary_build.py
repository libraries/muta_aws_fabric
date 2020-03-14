import os
import subprocess

import convention
import misc


def muta_docker():
    with misc.chdir(convention.muta_path):
        commit_id = subprocess.getoutput("git log -1 --pretty=\"%h\"")
        dockerhub_username = convention.dockerhub_username
        image_tag = f'{dockerhub_username}/muta:{commit_id}'
        misc.call(f"docker build -t {image_tag} .")
        misc.call(f"docker push {image_tag}")
    return {
        "image_tag": image_tag
    }


def muta_binary():
    with misc.chdir(convention.muta_path):
        misc.call("cargo build --release --example muta-chain")
        with misc.chdir("./devtools/keypair"):
            misc.call("cargo build --release")

    misc.call("rm -rf build")
    misc.call("mkdir -p build")
    a = os.path.join(convention.muta_path, "target/release/examples/muta-chain")
    misc.call(f"cp {a} ./build")
    a = os.path.join(convention.muta_path, "target/release/muta-keypair")
    misc.call(f"cp {a} ./build")
