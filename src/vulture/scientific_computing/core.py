"""Scientific computing helpers: chunked processing & GPU hooks."""
from typing import Iterable, Callable


def chunked_iter(iterable, chunk_size: int):
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk
