# CodeGo Image Skill

This is a Codex image-generation add-on skill for `https://shu26.cfd`. It uses
the fixed CodeGo Images API endpoint to support text-to-image generation, image
editing, image optimization, multi-image composition, masked local edits, and
local 4K / tile canvas workflows.

- Website: `https://shu26.cfd`
- API endpoint: `https://shu26.cfd/v1`
- Best suited for: poster design, avatar generation, product concept images,
  app icons, visual assets, reference-image edits, and multi-image composition

After installing this skill, Codex can send image requests directly to the
CodeGo Images API, reducing manual setup and repeated command assembly.

## Fixed Connection

The API base URL is fixed to:

```text
https://shu26.cfd/v1
```

The API key is read from the current user's Codex auth file:

```text
~/.codex/auth.json
```

## Platform Support

Windows and macOS use the same Python scripts:

- Windows: `C:\Users\<user>\.codex\auth.json`
- macOS: `/Users/<user>/.codex/auth.json`

The scripts use `Path.home()` to resolve the current user's home directory, so
you do not need to configure OS-specific paths manually.

## /image Entry

The skill provides a shortcut entrypoint:

```bash
python3 scripts/image.py "A cinematic rainy Shanghai street at night, neon reflections, vintage taxi"
```

On Windows, if `python3` is unavailable, use:

```powershell
python scripts\image.py "A cinematic rainy Shanghai street at night, neon reflections, vintage taxi"
```

If your Codex host supports binding slash commands to skill scripts, point
`/image` to:

```text
skills/codego-image-skill/scripts/image.py
```

A standard Codex skill directory does not include a universal slash-command
registration manifest. This repository provides the `/image` trigger guidance
and script entrypoint; whether a global slash command appears automatically
depends on the host that installs the skill.

## Structure

```text
skills/
  codego-image-skill/
    SKILL.md
    agents/
    references/
    scripts/
      image.py
      generate_image.py
      check_environment.py
      tile_canvas.py
```

## 4K And Tile Workflows

For 4K output, high-resolution texture, local repair, tile splitting, and
stitching workflows, see:

```text
skills/codego-image-skill/references/4k_workflows.md
```

Core rules:

- Do not request native `3840x2160` directly from the API.
- Build non-standard dimensions locally through canvas preparation, tile
  splitting, stitching, and enhancement.
- For close-up material details, prefer a stable base image, super-resolution
  tooling, or high-frequency detail transfer instead of hard-pasting
  independently generated tiles.

## Installation

Send this repository link directly to Codex for installation.
