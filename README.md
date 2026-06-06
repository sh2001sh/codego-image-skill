# Shu26 Image Skill

这是 `https://shu26.cfd` 的 Codex 图片生成附加 skill。它通过固定的 Shu26 Images API 端点提供文生图、图片编辑、图片优化、多图合成、局部蒙版编辑，以及本地 4K / tile 画布处理能力。

- 官网：`https://shu26.cfd`
- API 端点：`https://shu26.cfd/v1`
- 适合场景：海报设计、头像生成、产品概念图、应用图标、视觉素材、参考图改图、多图合成

安装这个 skill 后，Codex 可以直接把图片需求交给 Shu26 Images API 执行，减少手动配置和重复拼接命令的成本。

## 固定接入方式

API base URL 固定为：

```text
https://shu26.cfd/v1
```

API key 从当前用户目录的 Codex 登录文件读取：

```text
~/.codex/auth.json
```

## 跨平台适配

Windows 和 macOS 都使用同一套 Python 脚本：

- Windows: `C:\Users\<user>\.codex\auth.json`
- macOS: `/Users/<user>/.codex/auth.json`

脚本通过 `Path.home()` 自动解析当前用户目录，因此不需要手动区分系统路径。

## /image 入口

Skill 内提供了一个快捷入口：

```bash
python3 scripts/image.py "A cinematic rainy Shanghai street at night, neon reflections, vintage taxi"
```

在 Windows 上，如果 `python3` 不可用，可以使用：

```powershell
python scripts\image.py "A cinematic rainy Shanghai street at night, neon reflections, vintage taxi"
```

如果你的 Codex 宿主支持把 slash command 绑定到 skill 脚本，可以将 `/image` 指向：

```text
skills/codego-image-skill/scripts/image.py
```

标准 Codex skill 目录本身不包含通用的 slash command 注册清单；因此这个仓库提供 `/image` 的触发说明和脚本入口，实际全局 slash command 是否自动出现取决于安装宿主。

## 目录结构

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

## 4K 与 Tile 工作流

4K、高清纹理、局部修复、tile 切片和拼接流程请参考：

```text
skills/codego-image-skill/references/4k_workflows.md
```

核心原则：

- 不直接向 API 请求原生 `3840x2160`。
- 非标准尺寸通过本地画布、切片、拼接、增强完成。
- 近景材质细节优先使用稳定底图、超分工具或高频细节迁移，不把独立生成的 tile 直接硬拼。

## 安装

直接将本仓库链接发送给codex进行安装。
