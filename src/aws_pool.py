import fabric

import convention

pool: fabric.ThreadingGroup = None


def make_pool():
    global pool
    if pool:
        return
    ip_list = convention.aws_ip_node_list + convention.aws_ip_sync_list
    pool = fabric.ThreadingGroup(*ip_list, user="ubuntu", connect_kwargs={
        "key_filename": convention.aws_id_rsa,
    })
    pool.run("echo Welcome!")


def bash():
    make_pool()
    for _ in range(1 << 32):
        s = input("> ")
        try:
            pool.run(s)
        except fabric.exceptions.GroupException as e:
            print(e)
