import aws_pool
import misc

def deploy_binary():
    aws_pool.make_pool()
    aws_pool.pool.run(f"mkdir -p telnet")
    for e in aws_pool.pool:
        e.put("telnet/bin/server", "telnet/server")
        e.put("telnet/bin/client", "telnet/client")
    aws_pool.pool.run("telnet/server")
