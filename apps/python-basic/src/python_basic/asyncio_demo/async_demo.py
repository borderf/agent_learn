import asyncio


async def task():
    print("task")


def demo():
    coro = task()
    # 协程函数的返回值不是直接结果，而是协程对象
    # 协程对象是一个未执行的任务，要执行这个任务，需要事件循环来调度
    print(type(coro))
    # 创建事件循环，并将coro协程对象也就是任务注册到事件循环中，由事件循环调度执行
    asyncio.run(coro)


if __name__ == "__main__":
    demo()
