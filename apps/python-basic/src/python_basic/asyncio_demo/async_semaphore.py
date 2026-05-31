import asyncio


async def embed(text: str) -> list[float]:
    await asyncio.sleep(0.2)
    return [0.1, 0.2, 0.3]


async def embed_many(texts: list[str], concurrency: int = 3) -> list[list[float]]:
    semaphore = asyncio.Semaphore(concurrency)

    async def limited_embed(text: str) -> list[float]:
        async with semaphore:
            return await embed(text)

    return await asyncio.gather(*(limited_embed(text) for text in texts))


if __name__ == "__main__":
    texts = ["1", "2", "3", "4", "5", "6"]
    res = asyncio.run(embed_many(texts))
    print(res)
