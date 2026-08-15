#!/usr/bin/env python3
"""Set a Letta Desktop/Letta Code agent profile image.

Writes a square PNG to <agent-memory>/profile.png and optionally commits it.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover - exercised by users without Pillow
    print(
        "Missing dependency: Pillow. Install with `python3 -m pip install Pillow`.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def resolve_memory_dir(args: argparse.Namespace) -> Path:
    if args.memory_dir:
        return Path(args.memory_dir).expanduser().resolve()

    env_memory = os.environ.get("MEMORY_DIR") or os.environ.get("LETTA_MEMORY_DIR")
    if env_memory:
        return Path(env_memory).expanduser().resolve()

    agent_id = (
        args.agent_id or os.environ.get("AGENT_ID") or os.environ.get("LETTA_AGENT_ID")
    )
    if not agent_id:
        raise SystemExit(
            "Could not resolve memory dir. Pass --memory-dir or set AGENT_ID/MEMORY_DIR."
        )

    backend_dir = Path(
        args.local_backend_dir
        or os.environ.get("LETTA_LOCAL_BACKEND_DIR")
        or "~/.letta/lc-local-backend"
    ).expanduser()
    return (backend_dir / "memfs" / agent_id / "memory").resolve()


def crop_square(image: Image.Image, size: int) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGBA")
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    image = image.crop((left, top, left + side, top + side))
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    # Composite onto opaque background so Desktop gets a simple RGB PNG.
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.alpha_composite(image)
    return background.convert("RGB")


def commit_profile(memory_dir: Path, author: str | None) -> str | None:
    if not (memory_dir / ".git").exists():
        print(f"No git repo at {memory_dir}; wrote profile.png without committing.")
        return None

    add = run(["git", "add", "profile.png"], cwd=memory_dir)
    if add.returncode != 0:
        raise SystemExit(add.stderr or add.stdout or "git add failed")

    diff = run(
        ["git", "diff", "--cached", "--quiet", "--", "profile.png"], cwd=memory_dir
    )
    if diff.returncode == 0:
        print("profile.png already matches HEAD; no commit created.")
        head = run(["git", "rev-parse", "--short", "HEAD"], cwd=memory_dir)
        return head.stdout.strip() if head.returncode == 0 else None

    cmd = ["git", "commit", "-m", "Set agent profile image"]
    if author:
        cmd.insert(2, f"--author={author}")
    commit = run(cmd, cwd=memory_dir)
    if commit.returncode != 0:
        raise SystemExit(commit.stderr or commit.stdout or "git commit failed")

    head = run(["git", "rev-parse", "--short", "HEAD"], cwd=memory_dir)
    return head.stdout.strip() if head.returncode == 0 else None


def verify_profile(agent_id: str | None) -> None:
    base_url = os.environ.get("LETTA_BASE_URL")
    api_key = os.environ.get("LETTA_API_KEY")
    agent_id = agent_id or os.environ.get("AGENT_ID") or os.environ.get("LETTA_AGENT_ID")
    if not (base_url and api_key and agent_id):
        print("Skipping API verification; LETTA_BASE_URL, LETTA_API_KEY, or AGENT_ID missing.")
        return

    url = f"{base_url.rstrip('/')}/v1/agents/{agent_id}/profile-picture"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Profile-picture endpoint returned HTTP {exc.code}: {exc.read().decode('utf-8', 'ignore')}")
    except Exception as exc:  # noqa: BLE001 - command-line diagnostic
        raise SystemExit(f"Could not verify profile picture endpoint: {exc}")

    data_url = payload.get("data_url", "")
    if not isinstance(data_url, str) or not data_url.startswith("data:image/png;base64,"):
        raise SystemExit("Profile-picture endpoint did not return a PNG data URL.")
    print(f"Verified profile-picture endpoint ({len(data_url)} chars).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="Source image path (PNG, JPG, WEBP, etc.)")
    parser.add_argument("--memory-dir", help="Target agent memory directory; defaults to MEMORY_DIR")
    parser.add_argument("--agent-id", help="Target agent id; defaults to AGENT_ID")
    parser.add_argument(
        "--local-backend-dir",
        help="Local backend root used with --agent-id (default: ~/.letta/lc-local-backend)",
    )
    parser.add_argument("--size", type=int, default=512, help="Output square size in pixels")
    parser.add_argument("--no-commit", action="store_true", help="Write profile.png without committing")
    parser.add_argument("--verify", action="store_true", help="Verify via /v1/agents/:id/profile-picture")
    args = parser.parse_args()

    source = Path(args.image).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source image not found: {source}")
    if args.size < 64 or args.size > 2048:
        raise SystemExit("--size must be between 64 and 2048")

    memory_dir = resolve_memory_dir(args)
    memory_dir.mkdir(parents=True, exist_ok=True)
    output = memory_dir / "profile.png"

    with Image.open(source) as image:
        crop_square(image, args.size).save(output, format="PNG", optimize=True)

    print(f"Wrote {output}")

    commit_sha = None
    if not args.no_commit:
        agent_id = args.agent_id or os.environ.get("AGENT_ID") or os.environ.get("LETTA_AGENT_ID")
        agent_name = os.environ.get("AGENT_NAME") or "Letta Code"
        author = f"{agent_name} <{agent_id}@letta.com>" if agent_id else None
        commit_sha = commit_profile(memory_dir, author)
        if commit_sha:
            print(f"Memory commit: {commit_sha}")

    if args.verify:
        verify_profile(args.agent_id)

    print("If Desktop still shows the old image, reload or reopen the agent profile.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
