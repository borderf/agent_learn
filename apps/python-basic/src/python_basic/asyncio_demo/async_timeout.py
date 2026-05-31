import asyncio


async def call_slow_api() -> str:
    await asyncio.sleep(10)
    return "ok"


async def main():
    try:
        async with asyncio.timeout(3):
            res = await call_slow_api()
            print(res)
    except TimeoutError:
        print("timeout")


if __name__ == "__main__":
    asyncio.run(main())
