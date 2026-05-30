import asyncio


async def sub_task() -> int:
    print("sub_task")
    return 100


async def task01() -> int:
    print("task01")
    # await后面是协程函数的话，事件循环一般不会切换到其他任务去执行
    # 而是继续调度执行后面的协程函数
    # async协程对象是串行，顺序执行，不阻塞
    # 如果是future对象的话，事件循环会切换到其他的任务去执行
    await asyncio.sleep(5)
    result = await sub_task()
    return result


async def task02() -> int:
    print("task02")
    return 200


async def main():
    print("main")
    result = await asyncio.gather(task01(), task02())
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
