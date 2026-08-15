---
name: setting-profile-images
description: Sets Letta Desktop and Letta Code agent profile images by writing profile.png into an agent MemFS repository. Use when the user asks to add, change, generate, or fix an agent avatar, profile picture, profile image, or Desktop agent photo.
---

# Setting Profile Images

## Key fact

Letta Desktop displays an agent profile image from the agent memory repository at:

```text
$MEMORY_DIR/profile.png
```

The Desktop/local backend API reads the same file via:

```text
GET /v1/agents/:agent_id/profile-picture
```

For local Desktop agents, do **not** PATCH arbitrary agent metadata for the avatar. Write `profile.png` into MemFS and commit it.

## Workflow

1. Obtain an image:
   - Use a user-provided image path, or
   - Generate/create an avatar image with another image/art skill, then save it locally.
2. Convert/crop it to a square PNG using `scripts/set_profile_image.py`.
3. Commit the resulting `profile.png` to the target agent's memory repo.
4. Verify via the profile-picture endpoint when `LETTA_BASE_URL` and `LETTA_API_KEY` are available.
5. Tell the user to reload/reopen the agent profile in Desktop if the old image is cached.

## Current agent quick start

Locate this skill's script if needed:

```bash
SCRIPT=$(find ~/letta/skills ~/.letta/skills -path '*/setting-profile-images/scripts/set_profile_image.py' -print -quit)
```

Set the current agent's profile image:

```bash
python3 "$SCRIPT" /path/to/avatar.png
```

The script uses, in order:

- `--memory-dir`, if passed
- `$MEMORY_DIR`
- `$LETTA_MEMORY_DIR`
- `~/.letta/lc-local-backend/memfs/$AGENT_ID/memory`

## Other local agent

```bash
python3 "$SCRIPT" /path/to/avatar.png \
  --agent-id agent-local-... \
  --local-backend-dir ~/.letta/lc-local-backend
```

## Useful options

```bash
python3 "$SCRIPT" /path/to/avatar.jpg --size 512
python3 "$SCRIPT" /path/to/avatar.jpg --no-commit
python3 "$SCRIPT" /path/to/avatar.jpg --verify
```

- `--size` controls the square output size in pixels. Use `512` unless there is a reason not to.
- `--no-commit` writes the file but leaves the memory repo uncommitted.
- `--verify` calls `/v1/agents/:agent_id/profile-picture` after writing, when API env vars are present.

## Manual fallback

If the script is unavailable:

```bash
cp /path/to/avatar.png "$MEMORY_DIR/profile.png"
git -C "$MEMORY_DIR" add profile.png
git -C "$MEMORY_DIR" commit --author="$AGENT_NAME <$AGENT_ID@letta.com>" -m 'Add agent profile image'
```

Make sure the image is a reasonably sized square PNG before copying.
