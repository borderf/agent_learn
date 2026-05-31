import asyncio


async def task1() -> int:
    print("task1")
    await asyncio.sleep(0.1)
    return 100


async def task2() -> int:
    print("task2")
    await asyncio.sleep(0.1)
    raise ValueError("我出错了")


async def task3() -> int:
    print("task3")
    await asyncio.sleep(0.1)
    return 300


# 通用的异常处理包装器
async def capture_exceptions(coro):
    try:
        return await coro
    except Exception as e:
        return e


async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(capture_exceptions(task1()))
        t2 = tg.create_task(capture_exceptions(task2()))
        t3 = tg.create_task(capture_exceptions(task3()))
        # 此处所有任务已经在并发执行
    # 退出时，自动等待所有任务完成
    for name, t in [("a", t1), ("b", t2), ("c", t3)]:
        result = t.result()
        if isinstance(result, Exception):
            print(f"{name} 失败: {result}")
        else:
            print(f"{name} 成功: {result}")


if __name__ == "__main__":
    asyncio.run(main())
