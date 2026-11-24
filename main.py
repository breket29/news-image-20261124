#!/usr/bin/env python3
"""Entry for make.fun news-image-20261124: "The World in One Day — 24 November 2026".

Copies the poster (poster.png, committed in this same directory) to
/output/entry.png and verifies the copy against the poster's known SHA-256.
Standard library only. Deterministic: the same bytes on every run.
"""
import hashlib
import os
import shutil

POSTER_SHA256 = "dbfb2637421f115e2e7979aa00bec346a6ffe1eab9a1725285ad9f6f7c29ef00"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "poster.png")
    os.makedirs("/output", exist_ok=True)
    dst = "/output/entry.png"
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    size = os.path.getsize(dst)
    print(f"wrote {dst} ({size} bytes, sha256 {digest})")
    assert digest == POSTER_SHA256, "SHA-256 mismatch — poster copy is corrupt"
    print("sha256 OK")


if __name__ == "__main__":
    main()
