import time
import asyncio


def download(name: str) -> str:
    print(f"start {name}")
    time.sleep(2)
    print(f"done {name}")
    return name


async def download_async(name: str) -> str:
    print(f"start {name}")
    await asyncio.sleep(2)
    print(f"done {name}")
    return name


async def main_async() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        download_async("a"),
        download_async("b"),
        download_async("c"),
    )
    print(results)
    print(f"cost: {time.perf_counter() - start:.2f}s")


def main() -> None:
    start = time.perf_counter()
    download("a")
    download("b")
    download("c")
    print(f"cost: {time.perf_counter() - start:.2f}s")


async def fetch_user() -> dict:
    await asyncio.sleep(1)
    return {"id": "u1"}


async def main_fetch() -> None:
    task = asyncio.create_task(fetch_user())
    print("task created")
    user = await task
    print(user)


async def task1() -> int:
    print("task1开始执行")
    await asyncio.sleep(5)
    print("task1执行结束")
    return 10


async def task2() -> int:
    print("task2开始执行")
    await asyncio.sleep(3)
    print("task2执行结束")
    return 20


async def main_task():
    print("main task开始执行")
    # 获取事件循环
    # event_loop = asyncio.get_running_loop()
    # 手动注册任务
    # t1 = event_loop.create_task(task1())
    # t2 = event_loop.create_task(task2())

    # 等待 t1 任务执行结束，并且获取 t1 任务的执行结果
    # res1 = await t1
    # print(f"res1 = {res1}")
    # 等待 t2 任务执行结束，并且获取 t2 任务的执行结果
    # res2 = await t2
    # print(f"res2 = {res2}")
    # print("main task执行结束")

    # 等同于上述的操作，代码更简洁，返回结果为列表，分别为task1和task2的结果
    result = await asyncio.gather(task1(), task2())
    print(result)


if __name__ == "__main__":
    # main()
    # asyncio.run(main_fetch())
    start = time.time()
    # asyncio.run 会自动创建并管理事件循环
    asyncio.run(main_task())
    # 总耗时
    print(f"总耗时: {time.time() - start}")
