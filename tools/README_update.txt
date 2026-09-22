#!/usr/bin/env python3
"""VULTURE local updater without Git.

This module performs a safe, offline-friendly update flow:
- fetch a version manifest
- verify archive SHA256
- back up the current tree
- replace files only after validation
- never run untrusted code automatically
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = REPO_ROOT / ".vulture_backup"
MANIFEST_URL = os.environ.get("VULTURE_MANIFEST_URL", "https://example.invalid/manifest.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url, timeout=30) as response:
        with dest.open("wb") as fh:
            shutil.copyfileobj(response, fh)


def ensure_backup() -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = int(__import__("time").time())
    backup_dir = BACKUP_DIR / f"backup-{ts}"
    backup_dir.mkdir(exist_ok=True)
    return backup_dir


def install_archive(archive_path: Path, stage_dir: Path) -> None:
    if archive_path.suffix.lower() == ".zip":
        import zipfile
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(stage_dir)
    elif archive_path.suffix.lower() in {".tar", ".gz", ".tgz", ".tar.gz"}:
        import tarfile
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(stage_dir)
    else:
        raise ValueError(f"Unsupported archive type: {archive_path.suffix}")


def verify_manifest(manifest: dict, archive_path: Path) -> None:
    for key in ("version", "files", "sha256", "url"):
        if key not in manifest:
            raise ValueError(f"Manifest missing required key: {key}")
    actual = sha256_file(archive_path)
    if actual.lower() != manifest["sha256"].lower():
        raise ValueError("Archive SHA256 mismatch; update aborted")


def apply_update(archive_path: Path) -> None:
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive does not exist: {archive_path}")

    manifest = json.loads(urllib.request.urlopen(MANIFEST_URL, timeout=30).read().decode("utf-8"))
    verify_manifest(manifest, archive_path)

    backup_dir = ensure_backup()
    current_backup = backup_dir / "current"
    if current_backup.exists():
        shutil.rmtree(current_backup)
    shutil.copytree(REPO_ROOT, current_backup, dirs_exist_ok=True)

    stage_dir = REPO_ROOT / ".vulture_update_stage"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(exist_ok=True)

    install_archive(archive_path, stage_dir)

    for src in stage_dir.rglob("*"):
        if src.is_file():
            rel = src.relative_to(stage_dir)
            target = REPO_ROOT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)

    print(f"Update applied from manifest version {manifest['version']}")


def main() -> int:
    try:
        tmpdir = Path(tempfile.mkdtemp(prefix="vulture-update-"))
        archive_path = tmpdir / "vulture_update.zip"
        manifest = json.loads(urllib.request.urlopen(MANIFEST_URL, timeout=30).read().decode("utf-8"))
        download_file(manifest["url"], archive_path)
        apply_update(archive_path)
        return 0
    except Exception as exc:
        print(f"Update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
