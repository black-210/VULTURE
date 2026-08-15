"""Digital forensics helpers: file metadata extraction placeholder."""
import os


def file_metadata(path: str) -> dict:
    try:
        st = os.stat(path)
        return {
            "size": st.st_size,
            "mtime": st.st_mtime,
            "ctime": st.st_ctime,
        }
    except Exception:
        return {}
