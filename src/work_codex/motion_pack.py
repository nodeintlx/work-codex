from __future__ import annotations

from dataclasses import dataclass
import html
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFont

from .store import StoreError


@dataclass(frozen=True)
class MotionBuild:
    source_dir: Path
    output_dir: Path
    written_paths: list[Path]


def build_motion_pack(root: Path, source: Path | None = None) -> MotionBuild:
    source_dir = _resolve_source_dir(root, source)
    manifest_path = source_dir / "manifest.json"
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise StoreError(f"motion source manifest did not load as an object: {manifest_path}")

    brand = manifest.get("brand", {})
    briefs = manifest.get("briefs", [])
    if not isinstance(briefs, list) or not briefs:
        raise StoreError(f"motion source has no briefs: {manifest_path}")

    output_dir = source_dir / "motion-pack"
    output_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    cards: list[dict[str, str]] = []

    for brief in briefs:
        if not isinstance(brief, dict):
            continue
        slug = str(brief.get("slug", "")).strip()
        title = str(brief.get("title", slug)).strip()
        brief_dir = Path(str(brief.get("output_dir", "")))
        scene_spec = _load_json(brief_dir / "video-scenes.json")
        if not isinstance(scene_spec, dict):
            raise StoreError(f"scene spec did not load as an object: {brief_dir / 'video-scenes.json'}")
        verification = _load_optional_json(brief_dir / "verification.json")

        variants = {
            "vertical": {"width": 1080, "height": 1920, "font_scale": 1.0},
            "square": {"width": 1080, "height": 1080, "font_scale": 0.84},
        }
        for variant_name, dims in variants.items():
            filename = f"{slug}-{variant_name}.html"
            path = output_dir / filename
            path.write_text(
                _motion_html(
                    title=title,
                    brand=brand,
                    scene_spec=scene_spec,
                    width=dims["width"],
                    height=dims["height"],
                    font_scale=float(dims["font_scale"]),
                    variant_name=variant_name,
                ),
                encoding="utf-8",
            )
            written_paths.append(path)
            cards.append(
                {
                    "title": f"{title} ({variant_name})",
                    "filename": filename,
                }
            )

            png_name = f"{slug}-{variant_name}.png"
            png_path = output_dir / png_name
            _render_scene_poster(
                path=png_path,
                title=title,
                brand=brand,
                scene_spec=scene_spec,
                width=dims["width"],
                height=dims["height"],
                variant_name=variant_name,
            )
            written_paths.append(png_path)
            cards.append(
                {
                    "title": f"{title} ({variant_name} poster)",
                    "filename": png_name,
                }
            )

            if variant_name == "vertical":
                gif_name = f"{slug}-{variant_name}.gif"
                gif_path = output_dir / gif_name
                _render_scene_gif(
                    path=gif_path,
                    title=title,
                    brand=brand,
                    scene_spec=scene_spec,
                    width=dims["width"],
                    height=dims["height"],
                )
                written_paths.append(gif_path)
                cards.append(
                    {
                        "title": f"{title} ({variant_name} animated proof)",
                        "filename": gif_name,
                    }
                )

        if isinstance(verification, dict) and verification.get("facts"):
            proof_name = f"{slug}-proof.png"
            proof_path = output_dir / proof_name
            _render_proof_sheet(
                path=proof_path,
                title=title,
                brand=brand,
                verification=verification,
            )
            written_paths.append(proof_path)
            cards.append(
                {
                    "title": f"{title} (source of truth)",
                    "filename": proof_name,
                }
            )

    index_path = output_dir / "index.html"
    index_path.write_text(_preview_index(source_dir, brand, cards), encoding="utf-8")
    written_paths.append(index_path)

    pack_manifest = {
        "source_dir": str(source_dir),
        "brand": brand,
        "assets": cards,
    }
    pack_manifest_path = output_dir / "manifest.json"
    pack_manifest_path.write_text(json.dumps(pack_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written_paths.append(pack_manifest_path)

    return MotionBuild(source_dir=source_dir, output_dir=output_dir, written_paths=written_paths)


def _resolve_source_dir(root: Path, source: Path | None) -> Path:
    if source is not None:
        candidate = source if source.is_absolute() else (root / source)
        if candidate.is_dir():
            return candidate.resolve()
    latest_path = root / "nrg-bloom" / "content-engine" / "generated" / "latest" / "LATEST.txt"
    if not latest_path.exists():
        raise StoreError(f"latest content campaign pointer not found: {latest_path}")
    target = latest_path.read_text(encoding="utf-8").strip()
    if not target:
        raise StoreError(f"latest content campaign pointer is empty: {latest_path}")
    return Path(target).resolve()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_optional_json(path: Path) -> Any:
    if not path.exists():
        return None
    return _load_json(path)


def _motion_html(
    *,
    title: str,
    brand: dict[str, Any],
    scene_spec: dict[str, Any],
    width: int,
    height: int,
    font_scale: float,
    variant_name: str,
) -> str:
    colors = brand.get("colors", {})
    fonts = brand.get("fonts", {})
    scenes = scene_spec.get("scenes", [])
    if not isinstance(scenes, list) or not scenes:
        raise StoreError("scene spec must contain a non-empty scenes list")

    scene_blocks = []
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            continue
        text = html.escape(str(scene.get("text", "")))
        highlight = str(scene.get("highlight", "")).strip()
        if highlight:
            safe_highlight = html.escape(highlight)
            text = text.replace(safe_highlight, f'<span class="highlight">{safe_highlight}</span>', 1)
        scene_blocks.append(
            f'<section class="scene{" is-active" if index == 0 else ""}" data-index="{index}"><div class="scene-text">{text}</div></section>'
        )

    scene_markup = "\n".join(scene_blocks)
    scenes_json = json.dumps(scenes)
    duration_ms = len(scenes) * 3200
    brand_name = html.escape(str(brand.get("name", "NRG Bloom")))
    tagline = html.escape(str(brand.get("tagline", "")))
    social_handle = html.escape(str(brand.get("social_handle", "@NRGBloom")))
    title_safe = html.escape(title)
    display_font = html.escape(str(fonts.get("display", "Space Grotesk")))
    body_font = html.escape(str(fonts.get("body", "Inter")))
    bg = colors.get("bg", "#0A0E1A")
    surface = colors.get("surface", "#111827")
    border = colors.get("border", "#1F2937")
    accent = colors.get("accent", "#00C896")
    accent_warm = colors.get("accent_warm", "#F59E0B")
    text = colors.get("text", "#F9FAFB")
    text_muted = colors.get("text_muted", "#9CA3AF")
    text_dim = colors.get("text_dim", "#6B7280")
    assets = brand.get("assets", {})
    logo_white = str(assets.get("logo_white", "")).strip() if isinstance(assets, dict) else ""
    logo_src = html.escape("../" + Path(logo_white).name) if logo_white else ""

    base_title_size = int(30 * font_scale)
    base_scene_size = int((82 if height > width else 66) * font_scale)
    base_footer_size = int(24 * font_scale)
    base_badge_size = int(18 * font_scale)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_safe} / {variant_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={display_font.replace(' ', '+')}:wght@500;700&family={body_font.replace(' ', '+')}:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {bg};
      --surface: {surface};
      --border: {border};
      --accent: {accent};
      --accent-warm: {accent_warm};
      --text: {text};
      --text-muted: {text_muted};
      --text-dim: {text_dim};
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      background: #050814;
      font-family: "{body_font}", sans-serif;
      color: var(--text);
      min-height: 100%;
    }}
    body {{
      display: grid;
      place-items: center;
      padding: 20px;
    }}
    .frame {{
      width: {width}px;
      height: {height}px;
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(circle at top right, rgba(0, 200, 150, 0.18), transparent 24%),
        radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.12), transparent 22%),
        linear-gradient(180deg, rgba(17,24,39,0.98), rgba(10,14,26,1));
      border: 1px solid rgba(31, 41, 55, 0.95);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.45);
    }}
    .frame::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
      background-size: 52px 52px;
      mask-image: linear-gradient(180deg, rgba(255,255,255,0.48), transparent 75%);
      pointer-events: none;
    }}
    .frame::after {{
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(110deg, transparent 0%, rgba(0,200,150,0.08) 48%, transparent 56%);
      transform: translateX(-100%);
      animation: sweep {duration_ms}ms linear infinite;
      pointer-events: none;
    }}
    .topbar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      padding: 34px 42px 0;
      z-index: 3;
    }}
    .progress-track {{
      display: grid;
      grid-template-columns: repeat({len(scenes)}, 1fr);
      gap: 8px;
    }}
    .progress-segment {{
      height: 4px;
      border-radius: 999px;
      background: rgba(255,255,255,0.12);
      overflow: hidden;
      position: relative;
    }}
    .progress-segment::after {{
      content: "";
      position: absolute;
      inset: 0;
      transform: scaleX(0);
      transform-origin: left center;
      background: linear-gradient(90deg, var(--accent), var(--accent-warm));
    }}
    .progress-segment.is-running::after {{
      animation: fill 3200ms linear forwards;
    }}
    .meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 22px;
      gap: 16px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      border: 1px solid rgba(0, 200, 150, 0.28);
      border-radius: 999px;
      padding: 10px 16px;
      font-size: {base_badge_size}px;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
      backdrop-filter: blur(4px);
    }}
    .title {{
      max-width: 58%;
      text-align: right;
      font-family: "{display_font}", sans-serif;
      font-size: {base_title_size}px;
      line-height: 1.05;
      color: var(--text-muted);
    }}
    .scene-stage {{
      position: absolute;
      inset: 145px 52px 136px;
      z-index: 2;
    }}
    .scene {{
      position: absolute;
      inset: 0;
      display: grid;
      align-items: center;
      opacity: 0;
      transform: translateY(34px) scale(0.98);
      transition: opacity 420ms ease, transform 420ms ease;
    }}
    .scene.is-active {{
      opacity: 1;
      transform: translateY(0) scale(1);
    }}
    .scene-text {{
      font-family: "{display_font}", sans-serif;
      font-size: {base_scene_size}px;
      line-height: 0.98;
      font-weight: 700;
      letter-spacing: -0.03em;
      max-width: 88%;
      text-wrap: balance;
    }}
    .highlight {{
      color: var(--accent);
      text-shadow: 0 0 24px rgba(0, 200, 150, 0.25);
    }}
    .rail {{
      position: absolute;
      right: 42px;
      top: 220px;
      bottom: 140px;
      width: 2px;
      background: linear-gradient(180deg, rgba(0,200,150,0), rgba(0,200,150,0.7), rgba(245,158,11,0.45), rgba(0,200,150,0));
      opacity: 0.7;
    }}
    .footer {{
      position: absolute;
      left: 42px;
      right: 42px;
      bottom: 42px;
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 18px;
      z-index: 3;
    }}
    .footer-copy {{
      max-width: 56%;
      font-size: {base_footer_size}px;
      line-height: 1.35;
      color: var(--text-muted);
    }}
    .brand {{
      text-align: right;
    }}
    .brand-logo {{
      max-width: 210px;
      max-height: 56px;
      width: auto;
      object-fit: contain;
      filter: brightness(0) invert(1);
    }}
    .brand-name {{
      font-family: "{display_font}", sans-serif;
      font-size: {int(base_footer_size * 1.35)}px;
      line-height: 1;
    }}
    .brand-handle {{
      margin-top: 8px;
      font-size: {int(base_footer_size * 0.86)}px;
      color: var(--text);
      font-weight: 600;
    }}
    .brand-tagline {{
      margin-top: 8px;
      font-size: {int(base_footer_size * 0.78)}px;
      color: var(--text-dim);
      max-width: 320px;
    }}
    @keyframes fill {{
      from {{ transform: scaleX(0); }}
      to {{ transform: scaleX(1); }}
    }}
    @keyframes sweep {{
      from {{ transform: translateX(-100%); }}
      to {{ transform: translateX(110%); }}
    }}
  </style>
</head>
<body>
  <main class="frame">
    <header class="topbar">
      <div class="progress-track" id="progress-track">
        {''.join('<div class="progress-segment"></div>' for _ in scenes)}
      </div>
      <div class="meta">
        <div class="badge">{brand_name}</div>
        <div class="title">{title_safe}</div>
      </div>
    </header>

    <div class="scene-stage" id="scene-stage">
      {scene_markup}
    </div>
    <div class="rail"></div>

    <footer class="footer">
      <div class="footer-copy">{tagline}</div>
      <div class="brand">
        {f'<img class="brand-logo" src="{logo_src}" alt="{brand_name} logo">' if logo_src else f'<div class="brand-name">{brand_name}</div>'}
        <div class="brand-handle">{social_handle}</div>
        <div class="brand-tagline">{html.escape(variant_name)} / animated motion preview</div>
      </div>
    </footer>
  </main>

  <script>
    const scenes = {scenes_json};
    const sceneEls = Array.from(document.querySelectorAll(".scene"));
    const progressEls = Array.from(document.querySelectorAll(".progress-segment"));
    let activeIndex = 0;

    const activate = (index) => {{
      activeIndex = index;
      sceneEls.forEach((el, i) => el.classList.toggle("is-active", i === index));
      progressEls.forEach((el, i) => {{
        el.classList.remove("is-running");
        if (i < index) {{
          el.style.background = "linear-gradient(90deg, var(--accent), var(--accent-warm))";
        }} else {{
          el.style.background = "rgba(255,255,255,0.12)";
        }}
      }});
      const current = progressEls[index];
      if (current) {{
        current.style.background = "rgba(255,255,255,0.12)";
        void current.offsetWidth;
        current.classList.add("is-running");
      }}
    }};

    activate(0);
    setInterval(() => {{
      activate((activeIndex + 1) % scenes.length);
    }}, 3200);
  </script>
</body>
</html>
"""


def _preview_index(source_dir: Path, brand: dict[str, Any], cards: list[dict[str, str]]) -> str:
    brand_name = html.escape(str(brand.get("name", "NRG Bloom")))
    tagline = html.escape(str(brand.get("tagline", "")))
    accent = str(brand.get("colors", {}).get("accent", "#00C896"))
    bg = str(brand.get("colors", {}).get("bg", "#0A0E1A"))
    surface = str(brand.get("colors", {}).get("surface", "#111827"))
    text = str(brand.get("colors", {}).get("text", "#F9FAFB"))
    muted = str(brand.get("colors", {}).get("text_muted", "#9CA3AF"))
    items = "\n".join(
        f'<a class="card" href="{html.escape(item["filename"])}"><div class="title">{html.escape(item["title"])}</div><div class="meta">{html.escape(item["filename"])}</div></a>'
        for item in cards
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{brand_name} Motion Pack</title>
  <style>
    body {{
      margin: 0;
      font-family: Inter, sans-serif;
      background: {bg};
      color: {text};
      padding: 40px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 40px;
    }}
    p {{
      margin: 0 0 28px;
      color: {muted};
      font-size: 18px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      color: inherit;
      padding: 22px;
      border-radius: 18px;
      background: {surface};
      border: 1px solid rgba(255,255,255,0.08);
    }}
    .card:hover {{
      border-color: {accent};
      transform: translateY(-2px);
    }}
    .title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .meta {{
      font-size: 14px;
      color: {muted};
    }}
    .source {{
      margin-top: 20px;
      font-size: 13px;
      color: {muted};
    }}
  </style>
</head>
<body>
  <h1>{brand_name} Motion Pack</h1>
  <p>{tagline}</p>
  <div class="grid">
    {items}
  </div>
  <div class="source">Source campaign: {html.escape(str(source_dir))}</div>
</body>
</html>
"""


def _render_scene_poster(
    *,
    path: Path,
    title: str,
    brand: dict[str, Any],
    scene_spec: dict[str, Any],
    width: int,
    height: int,
    variant_name: str,
) -> None:
    image, draw = _base_canvas(width=width, height=height, brand=brand)
    scenes = scene_spec.get("scenes", [])
    if not isinstance(scenes, list) or not scenes:
        raise StoreError("scene spec must contain a non-empty scenes list")
    hero_scene = scenes[1] if len(scenes) > 1 else scenes[0]
    hero_text = str(hero_scene.get("text", "")).strip()
    highlight = str(hero_scene.get("highlight", "")).strip()
    brand_name = str(brand.get("name", "NRG Bloom"))
    tagline = str(brand.get("tagline", ""))
    colors = brand.get("colors", {})
    accent = colors.get("accent", "#00C896")
    text = colors.get("text", "#F9FAFB")
    muted = colors.get("text_muted", "#9CA3AF")
    body_x = 84
    max_width = width - 168

    _draw_badge(draw, x=body_x, y=76, label=f"{brand_name} / {variant_name} proof", color=accent)
    draw.multiline_text(
        (body_x, 166),
        _wrap_text(draw, title, _load_font("display", 76 if height > width else 58), max_width),
        font=_load_font("display", 76 if height > width else 58),
        fill=text,
        spacing=10,
    )
    if highlight:
        _draw_badge(draw, x=body_x, y=390 if height > width else 330, label=highlight, color=accent)
    draw.multiline_text(
        (body_x, 490 if height > width else 430),
        _wrap_text(draw, hero_text, _load_font("display", 68 if height > width else 52), max_width),
        font=_load_font("display", 68 if height > width else 52),
        fill=ImageColor.getrgb(text),
        spacing=14,
    )
    footer_y = height - 190 if height > width else height - 150
    draw.multiline_text(
        (body_x, footer_y),
        _wrap_text(draw, tagline, _load_font("body", 30 if height > width else 24), max_width // 2),
        font=_load_font("body", 30 if height > width else 24),
        fill=ImageColor.getrgb(muted),
        spacing=8,
    )
    draw.text(
        (width - 84, footer_y + 10),
        brand_name,
        font=_load_font("display", 32 if height > width else 28),
        fill=ImageColor.getrgb(text),
        anchor="ra",
    )
    image.save(path)


def _render_scene_gif(
    *,
    path: Path,
    title: str,
    brand: dict[str, Any],
    scene_spec: dict[str, Any],
    width: int,
    height: int,
) -> None:
    scenes = scene_spec.get("scenes", [])
    if not isinstance(scenes, list) or not scenes:
        raise StoreError("scene spec must contain a non-empty scenes list")
    frames: list[Image.Image] = []
    for scene in scenes:
        frame, draw = _base_canvas(width=width, height=height, brand=brand)
        text = str(scene.get("text", "")).strip()
        highlight = str(scene.get("highlight", "")).strip()
        colors = brand.get("colors", {})
        accent = colors.get("accent", "#00C896")
        text_color = colors.get("text", "#F9FAFB")
        muted = colors.get("text_muted", "#9CA3AF")
        brand_name = str(brand.get("name", "NRG Bloom"))
        _draw_badge(draw, x=84, y=76, label=brand_name, color=accent)
        draw.multiline_text(
            (84, 178),
            _wrap_text(draw, title, _load_font("display", 58), width - 168),
            font=_load_font("display", 58),
            fill=ImageColor.getrgb(muted),
            spacing=10,
        )
        if highlight:
            _draw_badge(draw, x=84, y=420, label=highlight, color=accent)
        draw.multiline_text(
            (84, 520),
            _wrap_text(draw, text, _load_font("display", 74), width - 168),
            font=_load_font("display", 74),
            fill=ImageColor.getrgb(text_color),
            spacing=16,
        )
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))

    first, *rest = frames
    first.save(path, save_all=True, append_images=rest, duration=900, loop=0)


def _render_proof_sheet(
    *,
    path: Path,
    title: str,
    brand: dict[str, Any],
    verification: dict[str, Any],
) -> None:
    width = 1080
    height = 1920
    image, draw = _base_canvas(width=width, height=height, brand=brand)
    colors = brand.get("colors", {})
    accent = colors.get("accent", "#00C896")
    text = colors.get("text", "#F9FAFB")
    muted = colors.get("text_muted", "#9CA3AF")
    panel = ImageColor.getrgb(colors.get("surface", "#111827"))
    border = ImageColor.getrgb(colors.get("border", "#1F2937"))
    _draw_badge(draw, x=72, y=60, label="source of truth", color=accent)
    draw.multiline_text(
        (72, 146),
        _wrap_text(draw, title, _load_font("display", 62), width - 144),
        font=_load_font("display", 62),
        fill=ImageColor.getrgb(text),
        spacing=10,
    )
    draw.text(
        (72, 284),
        str(verification.get("verification_standard", "")),
        font=_load_font("body", 28),
        fill=ImageColor.getrgb(muted),
    )

    y = 342
    for fact in verification.get("facts", []):
        if not isinstance(fact, dict):
            continue
        box_height = 360
        draw.rounded_rectangle((60, y, width - 60, y + box_height), radius=28, fill=panel, outline=border, width=2)
        draw.text((88, y + 28), str(fact.get("id", "")).upper(), font=_load_font("body", 24), fill=ImageColor.getrgb(accent))
        claim = _wrap_text(draw, str(fact.get("claim", "")), _load_font("display", 34), width - 176)
        draw.multiline_text((88, y + 72), claim, font=_load_font("display", 34), fill=ImageColor.getrgb(text), spacing=8)
        source_y = y + 168
        for source in fact.get("sources", [])[:3]:
            if not isinstance(source, dict):
                continue
            source_line = _truncate(str(source.get("path", "")), 72)
            excerpt = _truncate(str(source.get("excerpt", "")), 118)
            draw.text((88, source_y), source_line, font=_load_font("body", 20), fill=ImageColor.getrgb(accent))
            draw.multiline_text(
                (88, source_y + 28),
                _wrap_text(draw, excerpt, _load_font("body", 22), width - 176),
                font=_load_font("body", 22),
                fill=ImageColor.getrgb(muted),
                spacing=6,
            )
            source_y += 86
        y += box_height + 28
        if y > height - 220:
            break

    image.save(path)


def _base_canvas(*, width: int, height: int, brand: dict[str, Any]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    colors = brand.get("colors", {})
    bg = ImageColor.getrgb(colors.get("bg", "#0A0E1A"))
    accent = ImageColor.getrgb(colors.get("accent", "#00C896"))
    accent_warm = ImageColor.getrgb(colors.get("accent_warm", "#F59E0B"))
    surface = ImageColor.getrgb(colors.get("surface", "#111827"))
    image = Image.new("RGBA", (width, height), bg)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse((-160, -120, width // 2, height // 3), fill=(*accent, 54))
    overlay_draw.ellipse((width // 2, height // 2, width + 180, height + 180), fill=(*accent_warm, 40))
    overlay_draw.rounded_rectangle((28, 28, width - 28, height - 28), radius=32, outline=(*surface, 255), width=2)
    for step in range(80, width, 64):
        overlay_draw.line((step, 0, step, height), fill=(255, 255, 255, 14), width=1)
    for step in range(80, height, 64):
        overlay_draw.line((0, step, width, step), fill=(255, 255, 255, 10), width=1)
    image = Image.alpha_composite(image, overlay)
    return image, ImageDraw.Draw(image)


def _draw_badge(draw: ImageDraw.ImageDraw, *, x: int, y: int, label: str, color: str) -> None:
    font = _load_font("body", 24)
    text_box = draw.textbbox((0, 0), label.upper(), font=font)
    width = text_box[2] - text_box[0] + 34
    height = text_box[3] - text_box[1] + 18
    rgb = ImageColor.getrgb(color)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=999, outline=rgb, width=2, fill=(*rgb, 24))
    draw.text((x + 17, y + 8), label.upper(), font=font, fill=rgb)


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont, max_width: int) -> str:
    words = text.split()
    if not words:
        return ""
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return "\n".join(lines)


def _load_font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = {
        "display": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ],
        "body": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ],
    }
    for candidate in candidates.get(kind, []):
        font_path = Path(candidate)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
