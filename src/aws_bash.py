import aws_pool

import fabric


def bash():
    aws_pool.make_pool()
    for _ in range(1 << 32):
        s = input("> ")
        try:
            aws_pool.pool.run(s)
        except fabric.exceptions.GroupException as e:
            print(e)
