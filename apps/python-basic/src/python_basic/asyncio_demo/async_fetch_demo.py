import asyncio
from dataclasses import dataclass
import time
import httpx


@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int
    elapsed_ms: float


async def fetch(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
) -> FetchResult:
    # 在这里获取信号量
    async with semaphore:
        print(f"[开始] {url}")
        start = time.perf_counter()
        try:
            response = await client.get(url, timeout=5)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[完成] {url}  {elapsed:.0f}ms")
            return FetchResult(
                url,
                status_code=response.status_code,
                elapsed_ms=elapsed,
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[失败] {url}  {elapsed:.0f}ms  {e}")
            raise


async def fetch_all(
    urls: list[str],
    concurrency: int = 3,
) -> list[FetchResult | BaseException]:
    timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    semaphore = asyncio.Semaphore(concurrency)
    # 注意是在真正执行的地方去获取信号量
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = [fetch(client, url, semaphore) for url in urls]
        return await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )


async def main() -> None:
    urls = [
        "https://www.python.org",
        "https://docs.python.org/3/",
        "https://fastapi.tiangolo.com/",
        "https://www.baidu.com/",
    ]
    start = time.perf_counter()
    results = await fetch_all(urls, 4)
    for result in results:
        print(result)
    print(f"请求总耗时: {time.perf_counter() - start}s")


if __name__ == "__main__":
    asyncio.run(main())
