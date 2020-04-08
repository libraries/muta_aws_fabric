import aws_pool
import convention
import huobi_pipeline
import muta_pipeline
import telnet


def main():
    for i, e in enumerate(convention.args.step):
        print(f"[{i}] step {e}")
        if e == "huobi_build_binary":
            huobi_pipeline.build_binary()
        if e == "huobi_build_config":
            huobi_pipeline.build_config()
        if e == "huobi_deploy_binary":
            huobi_pipeline.deploy_binary()
        if e == "huobi_remote_run":
            huobi_pipeline.remote_run()
        if e == "huobi_remote_kill":
            huobi_pipeline.remote_kill()
        if e == "huobi":
            muta_pipeline.remote_kill()
            huobi_pipeline.remote_kill()
            huobi_pipeline.build_binary()
            huobi_pipeline.build_config()
            huobi_pipeline.deploy_binary()
            huobi_pipeline.remote_run()

        if e == "muta_build_binary":
            muta_pipeline.build_binary()
        if e == "muta_build_config":
            muta_pipeline.build_config()
        if e == "muta_deploy_binary":
            muta_pipeline.deploy_binary()
        if e == "muta_remote_run":
            muta_pipeline.remote_run()
        if e == "muta_remote_kill":
            muta_pipeline.remote_kill()
        if e == "muta":
            huobi_pipeline.remote_kill()
            muta_pipeline.remote_kill()
            muta_pipeline.build_binary()
            muta_pipeline.build_config()
            muta_pipeline.deploy_binary()
            muta_pipeline.remote_run()

        if e == "telnet_deploy":
            telnet.deploy_binary()
        if e == "telnet_server_kill":
            telnet.remote_kill()
        if e == "telnet_server_run":
            telnet.remote_run()

        if e == "aws_bash":
            aws_pool.bash()


if __name__ == "__main__":
    main()
