from dataclasses import dataclass, asdict
from pathlib import Path
import json
import os


@dataclass
class Chunk:
    index: int
    text: str
    start: int
    end: int


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def split_text(
    text: str, chunk_size: int = 500, overlap: int = 80, min_chunk_size: int = 160
) -> list[Chunk]:
    if chunk_size < 0:
        raise ValueError("chunk size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size.")
    if min_chunk_size < 0:
        raise ValueError("min_chunk_size must be >= 0.")
    if chunk_size < min_chunk_size:
        raise ValueError("chunk_size must be >= min_chunk_size.")

    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        # 如果是最后一块，且长度小于最小限制
        if end == len(text) and (end - start) < min_chunk_size:
            if chunks:  # 存在前一个块，合并进去
                prev = chunks[-1]
                prev.text += chunk_text
                prev.end = end
            else:  # 没有前一个块，直接保留
                chunks.append(Chunk(index=index, text=chunk_text, start=start, end=end))
            break
        chunks.append(Chunk(index=index, text=chunk_text, start=start, end=end))
        index += 1
        if end == len(text):
            break
        start = end - overlap
    return chunks


def save_chunks_json(chunks: list[Chunk], filePath: Path | str) -> None:
    chunks_dict = [asdict(chunk) for chunk in chunks]
    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(chunks_dict, f, ensure_ascii=False, indent=2)


def main() -> None:
    path = Path("./01_Python后端基础.md")
    text = normalize_text(path.read_text(encoding="utf-8"))
    chunks = split_text(text)

    # 统计输出信息
    total_chars = len(text)
    total_lines = len(text.splitlines())
    chunk_count = len(chunks)
    if chunks:
        max_len = max(len(c.text) for c in chunks)
        min_len = min(len(c.text) for c in chunks)
    else:
        max_len = min_len = 0

    print("=== 文档统计信息 ===")
    print(f"总字符数: {total_chars}")
    print(f"总行数: {total_lines}")
    print(f"chunk 数量: {chunk_count}")
    print(f"最大 chunk 长度: {max_len}")
    print(f"最小 chunk 长度: {min_len}")

    save_chunks_json(chunks, "chunks.json")


if __name__ == "__main__":
    main()
