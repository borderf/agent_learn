from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    index: int
    text: str
    start: int
    end: int


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def split_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[Chunk]:
    if chunk_size < 0:
        raise ValueError("chunk size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size.")

    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        chunks.append(Chunk(index=index, text=chunk_text, start=start, end=end))
        index += 1
        if end == len(text):
            break
        start = end - overlap
    return chunks


def main() -> None:
    path = Path("sample.md")
    text = normalize_text(path.read_text(encoding="utf-8"))
    chunks = split_text(text)
    for chunk in chunks:
        print(f"Chunk: {chunk.index}: {chunk.start}-{chunk.end}, len={len(chunk.text)}")


if __name__ == "__main__":
    main()
