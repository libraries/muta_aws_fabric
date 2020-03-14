import convention
import aws_bash
import aws_deploy_binary
import muta_binary_build
import muta_config_build


def main():
    for i, e in enumerate(convention.args.step):
        print(f"[{i}] step {e}")
        if e == "muta_build_docker":
            muta_binary_build.muta_docker()
        if e == "muta_build_binary":
            muta_binary_build.muta_binary()
        if e == "muta_build_config":
            muta_config_build.muta_config()
        if e == "aws_deploy_binary":
            aws_deploy_binary.deploy_binary()
        if e == "aws_deploy_run":
            aws_deploy_binary.deploy_run()
        if e == "aws_bash":
            aws_bash.bash()


if __name__ == "__main__":
    main()
