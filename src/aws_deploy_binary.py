import aws_pool
import convention
import misc


def deploy_muta_binary():
    aws_pool.make_pool()
    misc.call("python3 -m zipfile -c build.zip build")
    aws_pool.pool.run("killall -9 muta-chain huobi-chain | true")
    aws_pool.pool.run(f"rm -rf build build.zip")
    for e in aws_pool.pool:
        print(f"{e.host} upload build.zip")
        e.put("build.zip", "build.zip")
    aws_pool.pool.run("python3 -m zipfile -e build.zip . && cd build && chmod +x muta-chain")


def deploy_muta_run():
    aws_pool.make_pool()
    aws_pool.pool.run("killall -9 muta-chain huobi-chain | true")
    aws_pool.pool.run(f"rm -rf {convention.muta_data_path}")
    for i, e in enumerate(aws_pool.pool):
        print(f"{e.host} start muta-chain")
        e.run(
            f"cd build && (CONFIG=config_{i+1}.toml GENESIS=genesis.toml nohup ./muta-chain >& log < /dev/null &) && sleep 1")


def deploy_huobi_binary():
    aws_pool.make_pool()
    misc.call("python3 -m zipfile -c build.zip build")
    aws_pool.pool.run("killall -9 muta-chain huobi-chain | true")
    aws_pool.pool.run(f"rm -rf build build.zip")
    for e in aws_pool.pool:
        print(f"{e.host} upload build.zip")
        e.put("build.zip", "build.zip")
    aws_pool.pool.run("python3 -m zipfile -e build.zip . && cd build && chmod +x huobi-chain")


def deploy_huobi_run():
    aws_pool.make_pool()
    aws_pool.pool.run("killall -9 muta-chain huobi-chain | true")
    aws_pool.pool.run(f"rm -rf {convention.muta_data_path}")
    for i, e in enumerate(aws_pool.pool):
        print(f"{e.host} start huobi-chain")
        e.run(
            f"cd build && (nohup ./huobi-chain -c config_{i+1}.toml -g genesis.toml >& log < /dev/null &) && sleep 1")
