import asyncio


async def task1() -> int:
    print("task1")
    return 100


async def task2() -> int:
    print("task2")
    return 200


async def task3() -> int:
    print("task3")
    raise ValueError("这是task3的错误")


async def main1():
    print("main1")
    # 此处是异步的，但是是串行的，task2会等到task1执行完成后才会调度执行
    res1 = await task1()
    print(f"res1 = {res1}")
    res2 = await task2()
    print(f"res2 = {res2}")
    res3 = await task3()
    print(f"res3 = {res3}")


async def main2():
    print("main2")
    # 异步且并发的
    # 默认情况下，一个任务抛异常，gather会向外抛出异常
    # 使用 return_exceptions 可以让异常作为结果返回
    res = await asyncio.gather(task1(), task2(), task3(), return_exceptions=True)
    for result in res:
        if isinstance(result, Exception):
            print(f"failed, {result}")
        else:
            print(f"结果是: {result}")


if __name__ == "__main__":
    asyncio.run(main2())
