---
name: shu26-image
description: Image generation and image editing skill for shu26.cfd. Use this skill when the user asks for /image, image generation, creating pictures, drawing illustrations, making posters, designing wallpapers, producing avatars, editing photos, optimizing images, restoring images, upscaling images, combining images, merging reference images, or calling the fixed shu26.cfd Images API. Also trigger on Chinese requests such as /image, 生成图片, 生图, 画图, 生成海报, 做宣传图, 生成头像, 图片编辑, 改图, 修图, 优化图片, 图片增强, 图片合成, 多图融合, 参考图生图, and 调用 shu26.cfd 生图.
---

# Shu26 Image Skill

Use this skill as the Codex image-generation add-on for `https://shu26.cfd`.
The API base URL is fixed to `https://shu26.cfd/v1`.

Do not read the API URL or API key from environment variables, command-line
flags, or local config files. The key must come from the current user's Codex
auth file:

```text
~/.codex/auth.json
```

The primary key field is `OPENAI_API_KEY`. Compatibility field names are
`api_key`, `apiKey`, `token`, and `access_token`. Never print the key value.

## Platform Rules

The scripts are cross-platform Python:

- Windows resolves auth to `C:\Users\<user>\.codex\auth.json`.
- macOS resolves auth to `/Users/<user>/.codex/auth.json`.
- Linux resolves auth to `/home/<user>/.codex/auth.json`.

All paths are resolved with `Path.home()`, so do not ask the user to set OS
specific auth paths unless their Codex auth file is genuinely somewhere else.

## /image Workflow

For simple image generation, use the shortcut script:

```bash
python3 scripts/image.py "A cinematic rainy Shanghai street at night, neon reflections, vintage taxi"
```

On Windows, `python scripts\image.py "..."` is also acceptable when `python3` is
not available.

If the host supports binding slash commands to skill scripts, `/image` should
point to:

```text
skills/codego-image-skill/scripts/image.py
```

A standard Codex skill folder does not provide a universal slash-command
registration manifest, so automatic global slash-command availability depends on
the host. Still treat `/image ...` user requests as a trigger for this skill.

## Script Map

Use `scripts/image.py` for normal `/image` style requests. It forwards to
`scripts/generate_image.py` using the fixed Shu26 endpoint and Codex auth key.

Use `scripts/generate_image.py` directly only when advanced options are needed:
image edits, masks, multiple inputs, streaming, resize output, output format, or
retry control.

Use `scripts/check_environment.py` to verify Python support, fixed endpoint
availability in settings, and whether `~/.codex/auth.json` contains a usable
key. It must not offer environment variable or config-file fallbacks.

Use `scripts/tile_canvas.py` for local PNG canvas work: resizing, splitting,
stitching, detail transfer, scoring, sharpening, and 4K/tile experiments.

For 4K, zoomable texture, tiled generation, seam repair, or upscaling workflows,
read `references/4k_workflows.md` before generating or editing tiles.

## Quick Examples

Generate one image:

```bash
python3 scripts/image.py "A premium poster for shu26.cfd, elegant product lighting, clean composition"
```

Generate with an output path:

```bash
python3 scripts/image.py "A minimal app icon for an image generation service" --output ./icon.png
```

Edit one image:

```bash
python3 scripts/image.py "Improve clarity, restore detail, keep the original composition natural" \
  --image ./source.png \
  --output ./optimized-image.png
```

Compose multiple images:

```bash
python3 scripts/image.py "Place the person naturally into the background, matching lighting and perspective" \
  --image ./person.png \
  --image ./background.png \
  --output ./composited-image.png
```

## Compatibility Gate

Treat the official Images API guide/reference as the source of truth for request
fields. Do not infer support from a third-party compatible provider, old
examples, or a model alias.

Before every request:

- Send only fields documented for the chosen request shape.
- For `gpt-image-2`, use only `1024x1024`, `1536x1024`, `1024x1536`, or `auto`.
- Do not request native `3840x2160` from `gpt-image-2`; do 4K assembly locally.
- Omit `--input-fidelity` for `gpt-image-2`.
- Reject `--background transparent` for `gpt-image-2`.
- Keep `--count` at `10` or below.
- Use `--resize-output` for final dimensions outside the official API size set.
- Use `--stream` only intentionally; non-streaming is the default.

## Generation Workflow

1. Convert the user's request into a polished English image prompt unless they
   explicitly ask to pass it as-is with `--raw-prompt`.
2. Preserve important style, subject, composition, aspect ratio, text, color,
   mood, and reference constraints.
3. Run the compatibility gate before every API call.
4. Choose a stable output path in the current workspace or requested folder.
5. For text-to-image, use `image.py` or `generate_image.py --prompt ...`.
6. For editing, optimization, restoration, or enhancement, pass the source with
   `--image`.
7. For multi-image composition, repeat `--image` once per source.
8. For localized edits, pass `--mask`; the mask applies to the first `--image`.
9. Return output paths. If the host can render local files, display the image.

## Safety

All remote image, mask, generated-image, redirect, and API base URLs must use
HTTPS. The scripts reject URLs that use HTTP, include credentials, omit a
hostname, point to localhost, use `.local` hostnames, or use private/link-local,
loopback, reserved, or non-global IP address literals.

When a generation fails because the request is ambiguous or likely interpreted
as unsafe, improve the prompt by adding accurate context and safer framing while
preserving the creative goal.

Default to no fictionalization watermark for ordinary original images. Add a
small unobtrusive `Fictional dramatization` caption only when it materially
reduces confusion or misuse risk.
