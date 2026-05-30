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


if __name__ == "__main__":
    # main()
    asyncio.run(main_fetch())
