import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


async def task1() -> int:
    print("task1开始")
    result = await sub_task()
    print("task1结束")
    return result


async def sub_task() -> int:
    print("sub_task开始")
    # 创建future对象
    event_loop = asyncio.get_running_loop()
    future = event_loop.create_future()
    # 创建线程池对象
    executor = ThreadPoolExecutor()
    # 在其他线程执行任务
    event_loop.run_in_executor(executor, thread_task, future)
    # 挂起当前任务，事件循环调度其他任务执行
    result = await future
    print("sun_task结束")
    return result


def thread_task(future):
    time.sleep(5)
    future.set_result(100)


async def task2() -> int:
    print("task2开始")
    await asyncio.sleep(1)
    print("task2结束")
    return 200


async def main():
    print("main开始")
    result = await asyncio.gather(task1(), task2())
    print(result)
    print("main结束")


if __name__ == "__main__":
    asyncio.run(main())
