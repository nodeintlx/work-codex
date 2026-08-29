from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import html
import json
import os
from pathlib import Path
import re
import shutil
from textwrap import dedent
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
import yaml

from .factcheck import BriefVerification, factcheck_campaign, write_factcheck_report
from .store import StoreError


@dataclass(frozen=True)
class BrandSystem:
    name: str
    tagline: str
    social_handle: str
    assets: dict[str, str]
    signature: dict[str, Any]
    colors: dict[str, str]
    fonts: dict[str, str]
    voice: dict[str, Any]
    design: dict[str, Any]


@dataclass(frozen=True)
class ContentBrief:
    slug: str
    title: str
    publish_day: str
    archetype: str
    pillar: str
    target_channel: str
    audience: list[str]
    hero_stat: str
    hook: str
    thesis: str
    proof_points: list[str]
    contrarian_take: str
    call_to_action: str
    discussion_question: str
    quote: str
    quote_highlights: list[str]
    video_hook: str
    video_close: str
    hashtags: list[str]
    fact_ids: list[str]


@dataclass(frozen=True)
class GeneratedCampaign:
    output_dir: Path
    written_paths: list[Path]


def generate_content_campaign(root: Path, campaign_path: Path) -> GeneratedCampaign:
    campaign = _load_yaml(campaign_path)
    if not isinstance(campaign, dict):
        raise StoreError(f"campaign did not load as a mapping: {campaign_path}")

    brand_path = _resolve_path(campaign_path.parent, str(campaign.get("brand", "")))
    brand = _load_brand(brand_path)
    briefs = [_load_brief(item) for item in campaign.get("briefs", [])]
    if not briefs:
        raise StoreError(f"campaign has no briefs: {campaign_path}")

    campaign_slug = str(campaign.get("slug", campaign_path.stem)).strip() or campaign_path.stem
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = root / "nrg-bloom" / "content-engine" / "generated" / f"{stamp}-{campaign_slug}"
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    copied_assets = _copy_brand_assets(brand_path.parent, brand.assets, output_dir)
    written_paths.extend(copied_assets.values())
    brief_verifications: dict[str, BriefVerification] = {}
    verification_standard: str | None = None
    if str(campaign.get("fact_registry", "")).strip():
        factcheck_result = factcheck_campaign(root, campaign_path)
        brief_verifications = {brief.slug: brief for brief in factcheck_result.briefs}
        verification_standard = factcheck_result.verification_standard
        written_paths.extend(write_factcheck_report(output_dir, factcheck_result))

    overview_path = output_dir / "campaign-overview.md"
    overview_path.write_text(
        _campaign_overview_markdown(campaign, brand, briefs, brief_verifications, verification_standard),
        encoding="utf-8",
    )
    written_paths.append(overview_path)

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "campaign": {
            "slug": campaign_slug,
            "title": str(campaign.get("title", campaign_slug)),
        },
        "verification": {
            "enabled": bool(brief_verifications),
            "fact_registry": str(campaign.get("fact_registry", "")).strip() or None,
            "standard": verification_standard if brief_verifications else None,
        },
        "brand": {
            "name": brand.name,
            "tagline": brand.tagline,
            "social_handle": brand.social_handle,
            "assets": {
                **brand.assets,
                **{key: str(path) for key, path in copied_assets.items()},
            },
            "signature": brand.signature,
            "colors": brand.colors,
            "fonts": brand.fonts,
        },
        "briefs": [],
    }
    quote_cards: list[dict[str, str]] = []

    for brief in briefs:
        brief_dir = output_dir / brief.slug
        brief_dir.mkdir(parents=True, exist_ok=True)
        logo_src = _relative_asset_ref(brief_dir, copied_assets.get("logo_white"))
        signature_image_key = str(brand.signature.get("image_asset", "")).strip()
        speaker_src = _relative_asset_ref(brief_dir, copied_assets.get(signature_image_key)) if signature_image_key else None

        paths = {
            "linkedin-founder.md": _linkedin_founder_post(brand, brief),
            "linkedin-company.md": _linkedin_company_post(brand, brief),
            "x-thread.md": _x_thread(brand, brief),
            "carousel.md": _carousel_brief(brand, brief),
            "video-script.md": _video_script(brand, brief),
            "tiktok-caption.md": _tiktok_caption(brand, brief),
            "social-card.html": _social_card_html(brand, brief, logo_src),
            "quote-card-portrait.html": _quote_card_html(brand, brief, logo_src=logo_src, speaker_photo_src=speaker_src),
        }
        for filename, content in paths.items():
            path = brief_dir / filename
            path.write_text(content.rstrip() + "\n", encoding="utf-8")
            written_paths.append(path)

        quote_card_png_path = brief_dir / "quote-card-portrait.png"
        _render_quote_card_png(
            path=quote_card_png_path,
            brand=brand,
            brief=brief,
            logo_path=copied_assets.get("logo_white"),
            speaker_photo_path=copied_assets.get(signature_image_key) if signature_image_key else None,
        )
        written_paths.append(quote_card_png_path)
        quote_cards.append(
            {
                "slug": brief.slug,
                "title": brief.title,
                "html": f"{brief.slug}/quote-card-portrait.html",
                "png": f"{brief.slug}/quote-card-portrait.png",
            }
        )

        video_spec_path = brief_dir / "video-scenes.json"
        video_spec = _video_scene_spec(brand, brief)
        video_spec_path.write_text(json.dumps(video_spec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written_paths.append(video_spec_path)

        verification = brief_verifications.get(brief.slug)
        if verification is not None:
            data_sheet_path = brief_dir / "data-sheet.md"
            data_sheet_path.write_text(_data_sheet_markdown(brief, verification), encoding="utf-8")
            written_paths.append(data_sheet_path)

        brief_manifest = {
            "slug": brief.slug,
            "title": brief.title,
            "publish_day": brief.publish_day,
            "archetype": brief.archetype,
            "pillar": brief.pillar,
            "target_channel": brief.target_channel,
            "output_dir": str(brief_dir),
            "fact_ids": brief.fact_ids,
            "quote_card_html": str(brief_dir / "quote-card-portrait.html"),
            "quote_card_png": str(brief_dir / "quote-card-portrait.png"),
        }
        if verification is not None:
            brief_manifest["verification"] = {
                "verified": True,
                "path": str(brief_dir / "verification.json"),
            }
            brief_manifest["data_sheet"] = str(brief_dir / "data-sheet.md")
        manifest["briefs"].append(brief_manifest)

        brief_manifest_path = brief_dir / "manifest.json"
        brief_manifest_path.write_text(json.dumps(brief_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written_paths.append(brief_manifest_path)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written_paths.append(manifest_path)

    quote_cards_index_path = output_dir / "quote-cards.html"
    quote_cards_index_path.write_text(
        _quote_cards_index_html(
            campaign_title=str(campaign.get("title", campaign_slug)),
            brand=brand,
            cards=quote_cards,
        ),
        encoding="utf-8",
    )
    written_paths.append(quote_cards_index_path)

    latest_dir = root / "nrg-bloom" / "content-engine" / "generated" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    latest_index = latest_dir / "LATEST.txt"
    latest_index.write_text(str(output_dir) + "\n", encoding="utf-8")
    written_paths.append(latest_index)

    return GeneratedCampaign(output_dir=output_dir, written_paths=written_paths)


def _campaign_overview_markdown(
    campaign: dict[str, Any],
    brand: BrandSystem,
    briefs: list[ContentBrief],
    brief_verifications: dict[str, BriefVerification],
    verification_standard: str | None,
) -> str:
    lines = [
        f"# {campaign.get('title', 'NRG Bloom Content Campaign')}",
        "",
        f"Brand: {brand.name}",
        f"Tagline: {brand.tagline}",
        "",
        "## Positioning",
        "",
        str(campaign.get("positioning", "")).strip(),
        "",
        "## Editorial Thesis",
        "",
        str(campaign.get("editorial_thesis", "")).strip(),
        "",
        "## Weekly Sequence",
        "",
    ]
    for brief in briefs:
        lines.extend(
            [
                f"### {brief.publish_day} — {brief.title}",
                f"- Archetype: {brief.archetype}",
                f"- Pillar: {brief.pillar}",
                f"- Target channel: {brief.target_channel}",
                f"- Hero stat: {brief.hero_stat}",
                f"- Hook: {brief.hook}",
                "",
            ]
        )
        verification = brief_verifications.get(brief.slug)
        if verification is not None:
            lines.extend(
                [
                    f"- Verification: {len(verification.facts)} fact(s), each backed by 3+ corroborating sources",
                    f"- Verification standard: {verification_standard or '3 corroborating sources minimum per fact'}",
                    f"- Fact IDs: {', '.join(verification.fact_ids)}",
                    "",
                ]
            )
    return "\n".join(lines)


def _linkedin_founder_post(brand: BrandSystem, brief: ContentBrief) -> str:
    hashtags = " ".join(brief.hashtags[:6])
    opening_frame = _voice_pick(brand, "founder_opening_frames", brief.slug, fallback="Most people are reading this too loosely.")
    interpretation_frame = _voice_pick(brand, "founder_interpretation_frames", brief.slug, fallback="The more useful read is this:")
    conviction_frame = _voice_pick(brand, "founder_conviction_frames", brief.slug, fallback="My read is simple:")
    close_frame = _voice_pick(brand, "founder_close_frames", brief.slug, fallback="That is where NRG Bloom intends to win.")
    return dedent(
        f"""
        # LinkedIn Founder Post
        **Title:** {brief.title}
        **Channel:** Founder POV
        **Pillar:** {brief.pillar}

        {brief.hook}

        {brief.hero_stat}

        {opening_frame}

        {brief.thesis}

        {interpretation_frame}

        {brief.proof_points[0]}

        {brief.proof_points[1]}

        {brief.proof_points[2]}

        {conviction_frame} {brief.contrarian_take}

        {close_frame}

        {brief.call_to_action}

        {brief.discussion_question}

        {hashtags}
        """
    ).strip()


def _linkedin_company_post(brand: BrandSystem, brief: ContentBrief) -> str:
    interpretation_frame = _voice_pick(brand, "founder_interpretation_frames", brief.slug, fallback="Read that in practical terms:")
    return dedent(
        f"""
        # LinkedIn Company Post
        **Title:** {brief.title}
        **Channel:** Company Page

        {brief.hook}

        {brief.hero_stat}

        {brief.thesis}

        {interpretation_frame}

        - {brief.proof_points[0]}
        - {brief.proof_points[1]}
        - {brief.proof_points[2]}

        {brief.contrarian_take}

        {brief.call_to_action}
        """
    ).strip()


def _x_thread(brand: BrandSystem, brief: ContentBrief) -> str:
    opening_frame = _voice_pick(brand, "founder_opening_frames", brief.slug, fallback="Most people are missing the point.")
    tweets = [
        f"1/ {brief.hook}",
        f"2/ {brief.hero_stat}",
        f"3/ {opening_frame} {brief.thesis}",
        f"4/ {brief.proof_points[0]}",
        f"5/ {brief.proof_points[1]}",
        f"6/ {brief.proof_points[2]}",
        f"7/ {brief.contrarian_take}",
        f"8/ {brief.call_to_action}",
        f"9/ {brief.discussion_question}",
    ]
    return "# X Thread\n\n" + "\n\n".join(tweets)


def _carousel_brief(brand: BrandSystem, brief: ContentBrief) -> str:
    slides = [
        ("Slide 1", brief.title, brief.hook),
        ("Slide 2", "The Stat", brief.hero_stat),
        ("Slide 3", "What Most People Miss", brief.thesis),
        ("Slide 4", "Operator Truth #1", brief.proof_points[0]),
        ("Slide 5", "Operator Truth #2", brief.proof_points[1]),
        ("Slide 6", "Operator Truth #3", brief.proof_points[2]),
        ("Slide 7", "The Contrarian Take", brief.contrarian_take),
        ("Slide 8", "Call To Action", brief.call_to_action),
    ]
    lines = [f"# Carousel Brief — {brief.title}", ""]
    for label, heading, body in slides:
        lines.extend([f"## {label}", f"- Heading: {heading}", f"- Body: {body}", ""])
    return "\n".join(lines).strip()


def _video_script(brand: BrandSystem, brief: ContentBrief) -> str:
    interpretation_frame = _voice_pick(brand, "founder_interpretation_frames", brief.slug, fallback="The operating takeaway is straightforward:")
    return dedent(
        f"""
        # Short Video Script
        **Title:** {brief.title}
        **Format:** 45-60 second talking-head or kinetic text

        ## Hook
        {brief.video_hook}

        ## Body
        {brief.hero_stat}

        Most people hear that and think market size.
        {interpretation_frame}

        {brief.thesis}

        First: {brief.proof_points[0]}

        Second: {brief.proof_points[1]}

        Third: {brief.proof_points[2]}

        {brief.contrarian_take}

        ## Close
        {brief.video_close}
        """
    ).strip()


def _tiktok_caption(brand: BrandSystem, brief: ContentBrief) -> str:
    tags = " ".join(brief.hashtags[:5])
    return dedent(
        f"""
        # TikTok Caption

        {brief.hook}

        {brief.hero_stat}

        {brief.thesis}

        {brief.contrarian_take}

        {brief.video_close}

        {tags}
        """
    ).strip()


def _video_scene_spec(brand: BrandSystem, brief: ContentBrief) -> dict[str, Any]:
    return {
        "format": "tiktok_story_arc",
        "brand": {
            "colors": brand.colors,
            "fonts": brand.fonts,
        },
        "title": brief.title,
        "cta": brief.call_to_action,
        "scenes": [
            {"text": brief.video_hook, "highlight": brief.title.split(" ")[0]},
            {"text": brief.hero_stat, "highlight": brief.hero_stat.split(" ")[0]},
            {"text": brief.proof_points[0], "highlight": "operators"},
            {"text": brief.proof_points[1], "highlight": "capital"},
            {"text": brief.proof_points[2], "highlight": "speed"},
            {"text": brief.contrarian_take, "highlight": "contrarian"},
            {"text": brief.video_close, "highlight": brand.name},
        ],
    }


def _data_sheet_markdown(brief: ContentBrief, verification: BriefVerification) -> str:
    lines = [
        f"# Data Sheet — {brief.title}",
        "",
        f"Brief slug: {brief.slug}",
        f"Hero stat: {brief.hero_stat}",
        f"Core thesis: {brief.thesis}",
        "",
        "## Claims Used In The Post",
        "",
        f"- Hook claim: {brief.hook}",
        f"- Proof point 1: {brief.proof_points[0]}",
        f"- Proof point 2: {brief.proof_points[1]}",
        f"- Proof point 3: {brief.proof_points[2]}",
        f"- Contrarian take: {brief.contrarian_take}",
        "",
        "## Verified Facts",
        "",
    ]
    for fact in verification.facts:
        lines.extend(
            [
                f"### {fact.fact_id}",
                fact.claim,
                f"Scope: {fact.scope}",
                "",
                "Sources:",
            ]
        )
        for source in fact.sources:
            line = f"- [{source.source_type}] {source.authority}"
            if source.title:
                line += f" | {source.title}"
            lines.append(line)
            if source.url:
                lines.append(f"  URL: {source.url}")
            lines.append(f"  Excerpt: {source.excerpt}")
            if source.checked_on:
                lines.append(f"  Checked: {source.checked_on}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _voice_pick(brand: BrandSystem, key: str, seed: str, *, fallback: str) -> str:
    values = brand.voice.get(key, [])
    if not isinstance(values, list) or not values:
        return fallback
    options = [str(value).strip() for value in values if str(value).strip()]
    if not options:
        return fallback
    index = sum(ord(char) for char in seed) % len(options)
    return options[index]


def _social_card_html(brand: BrandSystem, brief: ContentBrief, logo_src: str | None = None) -> str:
    colors = brand.colors
    fonts = brand.fonts
    proof_markup = "\n".join(f"<li>{point}</li>" for point in brief.proof_points)
    logo_markup = (
        f'<img class="logo" src="{html.escape(logo_src)}" alt="{html.escape(brand.name)} logo">'
        if logo_src
        else f'<div class="name">{brand.name}</div>'
    )
    return dedent(
        f"""
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{brief.title}</title>
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family={fonts['display'].replace(' ', '+')}:wght@500;700&family={fonts['body'].replace(' ', '+')}:wght@400;500;600&display=swap" rel="stylesheet">
          <style>
            :root {{
              --bg: {colors['bg']};
              --surface: {colors['surface']};
              --border: {colors['border']};
              --accent: {colors['accent']};
              --accent-warm: {colors['accent_warm']};
              --text: {colors['text']};
              --text-muted: {colors['text_muted']};
              --text-dim: {colors['text_dim']};
            }}
            * {{ box-sizing: border-box; }}
            body {{
              margin: 0;
              min-height: 100vh;
              font-family: "{fonts['body']}", sans-serif;
              background:
                radial-gradient(circle at top right, rgba(0, 200, 150, 0.18), transparent 28%),
                radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.14), transparent 24%),
                linear-gradient(180deg, #0a0e1a 0%, #0d1324 100%);
              color: var(--text);
              display: grid;
              place-items: center;
              padding: 32px;
            }}
            .card {{
              width: 1080px;
              min-height: 1080px;
              padding: 72px;
              border-radius: 36px;
              background:
                linear-gradient(180deg, rgba(17, 24, 39, 0.95), rgba(10, 14, 26, 0.98));
              border: 1px solid rgba(31, 41, 55, 0.9);
              position: relative;
              overflow: hidden;
              box-shadow: 0 28px 80px rgba(0, 0, 0, 0.45);
            }}
            .card::before {{
              content: "";
              position: absolute;
              inset: 0;
              background-image:
                linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
              background-size: 52px 52px;
              mask-image: linear-gradient(180deg, rgba(255,255,255,0.35), transparent 70%);
              pointer-events: none;
            }}
            .topline {{
              display: inline-flex;
              align-items: center;
              gap: 12px;
              padding: 10px 16px;
              border: 1px solid rgba(0, 200, 150, 0.3);
              border-radius: 999px;
              color: var(--accent);
              font-size: 20px;
              font-weight: 600;
              letter-spacing: 0.04em;
              text-transform: uppercase;
            }}
            .title {{
              margin: 28px 0 18px;
              font-family: "{fonts['display']}", sans-serif;
              font-size: 74px;
              line-height: 0.95;
              max-width: 760px;
            }}
            .hero-stat {{
              font-family: "{fonts['display']}", sans-serif;
              font-size: 38px;
              line-height: 1.15;
              color: var(--accent-warm);
              max-width: 760px;
              margin-bottom: 24px;
            }}
            .thesis {{
              font-size: 32px;
              line-height: 1.35;
              max-width: 800px;
              color: var(--text);
            }}
            .panel {{
              margin-top: 40px;
              padding: 28px 32px;
              background: rgba(17, 24, 39, 0.82);
              border: 1px solid rgba(0, 200, 150, 0.18);
              border-radius: 26px;
              max-width: 860px;
            }}
            .panel h2 {{
              margin: 0 0 16px;
              font-size: 20px;
              letter-spacing: 0.08em;
              text-transform: uppercase;
              color: var(--text-muted);
            }}
            ul {{
              margin: 0;
              padding-left: 24px;
              display: grid;
              gap: 12px;
              font-size: 26px;
              line-height: 1.35;
            }}
            .footer {{
              position: absolute;
              left: 72px;
              right: 72px;
              bottom: 60px;
              display: flex;
              justify-content: space-between;
              align-items: end;
              gap: 24px;
            }}
            .quote {{
              max-width: 700px;
              font-size: 22px;
              color: var(--text-muted);
              line-height: 1.45;
            }}
            .brand {{
              text-align: right;
              display: flex;
              flex-direction: column;
              align-items: end;
            }}
            .brand .logo {{
              max-width: 220px;
              max-height: 54px;
              object-fit: contain;
              filter: brightness(0) invert(1);
            }}
            .brand .handle {{
              margin-top: 10px;
              font-size: 18px;
              color: var(--text);
              font-weight: 600;
            }}
            .brand .tagline {{
              margin-top: 6px;
              font-size: 16px;
              color: var(--text-dim);
            }}
          </style>
        </head>
        <body>
          <article class="card">
            <div class="topline">{brand.name} / {brief.pillar.replace('-', ' ')}</div>
            <h1 class="title">{brief.title}</h1>
            <div class="hero-stat">{brief.hero_stat}</div>
            <p class="thesis">{brief.thesis}</p>
            <section class="panel">
              <h2>Operator Signals</h2>
              <ul>
                {proof_markup}
              </ul>
            </section>
            <footer class="footer">
              <div class="quote">"{brief.quote}"</div>
              <div class="brand">
                {logo_markup}
                <div class="handle">{brand.social_handle}</div>
                <div class="tagline">{brand.tagline}</div>
              </div>
            </footer>
          </article>
        </body>
        </html>
        """
    ).strip()


def _quote_card_html(
    brand: BrandSystem,
    brief: ContentBrief,
    *,
    logo_src: str | None = None,
    speaker_photo_src: str | None = None,
) -> str:
    accent = str(brand.colors.get("quote_accent", "#6BA3E8"))
    accent_deep = str(brand.colors.get("quote_accent_deep", "#14489B"))
    quote_surface = str(brand.colors.get("quote_surface", "#14233A"))
    card_background = str(brand.colors.get("quote_background", "#1A2D4A"))
    quote_markup = _quote_html_markup(brief.quote, brief.quote_highlights, accent_class="accent")
    logo_markup = (
        f'<img src="{html.escape(logo_src)}" alt="{html.escape(brand.name)}" class="brand-logo">'
        if logo_src
        else f'<div class="brand-fallback">{html.escape(brand.name)}</div>'
    )
    signature_name = html.escape(str(brand.signature.get("name", brand.name)))
    signature_title = html.escape(str(brand.signature.get("title", brand.tagline)))
    website = html.escape(str(brand.signature.get("website", "nrgbloom.com")))
    handle_tagline = html.escape(str(brand.signature.get("handle_tagline", brand.tagline)))
    pillar_text = html.escape(brief.pillar.replace("-", " ").upper())
    stat_number, stat_unit, stat_tail = _hero_stat_parts(brief.hero_stat)
    hero_display_text, support_text = _hero_display_copy(brief, stat_number, stat_tail)
    support_line = _short_card_text(support_text, 140)
    hero_display_text, support_text = _hero_display_copy(brief, stat_number, stat_tail)
    hero_stat_markup = _hero_stat_markup(stat_number, stat_unit, hero_display_text)
    stat_tail_markup = html.escape(support_text)
    support_line = _short_card_text(support_text, 140)
    chip_items = [
        ("Signal", _short_card_text(brief.proof_points[0], 54)),
        ("Edge", _short_card_text(brief.contrarian_take, 54)),
    ]
    speaker_markup = ""
    if speaker_photo_src:
        speaker_markup = dedent(
            f"""
            <div class="speaker-photo-ring">
              <div class="speaker-photo-inner">
                <img src="{html.escape(speaker_photo_src)}" alt="{signature_name}" class="speaker-photo">
              </div>
            </div>
            """
        ).strip()
    return dedent(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=1080">
        <title>{html.escape(brief.title)} Quote Card</title>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@700;800&display=swap');
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}
          body {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
            background: #000;
            margin: 0;
            padding: 0;
          }}
          .card {{
            width: 1080px;
            height: 1350px;
            background: {card_background};
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
          }}
          .orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
          }}
          .orb-1 {{
            width: 760px;
            height: 760px;
            top: -260px;
            left: -180px;
            background: radial-gradient(ellipse, rgba(40,100,180,0.34) 0%, transparent 66%);
            animation: drift1 11s ease-in-out infinite;
          }}
          .orb-2 {{
            width: 620px;
            height: 620px;
            right: -160px;
            bottom: -160px;
            background: radial-gradient(ellipse, rgba(107,163,232,0.28) 0%, transparent 66%);
            animation: drift2 13s ease-in-out infinite;
          }}
          .orb-3 {{
            width: 360px;
            height: 360px;
            top: 44%;
            right: 18%;
            background: radial-gradient(ellipse, rgba(40,100,180,0.18) 0%, transparent 62%);
            animation: drift1 14s ease-in-out infinite reverse;
          }}
          @keyframes drift1 {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(24px, 18px) scale(1.04); }}
          }}
          @keyframes drift2 {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(-18px, -28px) scale(1.06); }}
          }}
          .noise {{
            position: absolute;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
            z-index: 1;
            pointer-events: none;
          }}
          .grid {{
            position: absolute;
            inset: 0;
            background-image:
              linear-gradient(rgba(107, 163, 232, 0.04) 1px, transparent 1px),
              linear-gradient(90deg, rgba(107, 163, 232, 0.04) 1px, transparent 1px);
            background-size: 54px 54px;
            z-index: 1;
            mask-image: radial-gradient(ellipse 72% 72% at 30% 26%, black, transparent);
          }}
          .top-line {{
            height: 3px;
            background: linear-gradient(90deg, transparent, {accent} 30%, {accent_deep} 70%, transparent);
            position: relative;
            z-index: 2;
          }}
          .content {{
            position: relative;
            z-index: 2;
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 72px 80px 56px;
          }}
          .pillar {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 42px;
          }}
          .pillar-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {accent};
            box-shadow: 0 0 12px rgba(107, 163, 232, 0.6);
          }}
          .pillar-text {{
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: {accent};
          }}
          .hero {{
            margin-bottom: 24px;
          }}
          .stat-row {{
            display: flex;
            align-items: baseline;
            gap: 6px;
            margin-bottom: 8px;
          }}
          .stat-number {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 124px;
            font-weight: 800;
            line-height: 0.88;
            background: linear-gradient(180deg, #ffffff 18%, rgba(107, 163, 232, 0.72) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -5px;
          }}
          .stat-unit {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 38px;
            font-weight: 700;
            color: #ffffff;
            line-height: 1;
            margin-bottom: 16px;
          }}
          .hero-headline {{
            font-size: 60px;
            font-weight: 800;
            line-height: 0.98;
            letter-spacing: -2.8px;
            color: #ffffff;
            max-width: 820px;
            margin-bottom: 10px;
          }}
          .stat-label {{
            font-size: 20px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.72);
            line-height: 1.38;
            max-width: 720px;
            margin-bottom: 0;
            letter-spacing: -0.2px;
          }}
          .chip-row {{
            display: flex;
            gap: 14px;
            margin-bottom: 26px;
            flex-wrap: wrap;
          }}
          .chip {{
            min-width: 0;
            max-width: 420px;
            padding: 16px 18px;
            background: rgba(20, 72, 155, 0.2);
            border: 1px solid rgba(107, 163, 232, 0.24);
            border-radius: 16px;
          }}
          .data-kicker {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: {accent};
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
          }}
          .data-desc {{
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            line-height: 1.34;
            letter-spacing: -0.15px;
          }}
          .quote-panel {{
            position: relative;
            background: {quote_surface};
            border-radius: 24px;
            padding: 34px 38px 32px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
            margin-top: auto;
          }}
          .quote-mark,
          .quote-mark-close {{
            font-size: 64px;
            font-weight: 900;
            color: {accent};
            opacity: 0.9;
          }}
          .quote-mark {{
            line-height: 0.6;
            margin-bottom: 14px;
          }}
          .quote-mark-close {{
            line-height: 0.4;
            text-align: right;
            margin-top: 12px;
          }}
          .quote-text {{
            font-size: 30px;
            font-weight: 700;
            color: #fff;
            line-height: 1.3;
            letter-spacing: -0.5px;
          }}
          .quote-text .accent {{
            color: {accent};
          }}
          .speaker-section {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 20px;
            margin-top: 24px;
          }}
          .speaker-info {{
            text-align: right;
          }}
          .speaker-name {{
            font-size: 22px;
            font-weight: 700;
            color: #fff;
            letter-spacing: 0.3px;
          }}
          .speaker-title {{
            font-size: 14px;
            font-weight: 600;
            color: {accent};
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 4px;
          }}
          .speaker-photo-ring {{
            width: 110px;
            height: 110px;
            border-radius: 50%;
            padding: 4px;
            background: linear-gradient(135deg, {accent}, {accent_deep}, {accent});
            flex-shrink: 0;
            box-shadow: 0 4px 24px rgba(107,163,232,0.3);
          }}
          .speaker-photo-inner {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #000;
            position: relative;
          }}
          .speaker-photo {{
            width: 250%;
            height: 250%;
            object-fit: cover;
            object-position: center 20%;
            filter: brightness(0.75) contrast(1.15);
            margin-left: -80%;
            margin-top: -25%;
          }}
          .bottom-line {{
            height: 1px;
            background: rgba(255,255,255,0.08);
            margin-top: 28px;
          }}
          .brand-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
          }}
          .brand-left {{
            display: flex;
            align-items: center;
            gap: 20px;
          }}
          .brand-logo {{
            height: 50px;
            width: auto;
            filter: brightness(0) invert(1);
          }}
          .brand-fallback {{
            color: #fff;
            font-size: 26px;
            font-weight: 700;
            letter-spacing: 0.04em;
          }}
          .brand-divider {{
            width: 1px;
            height: 36px;
            background: rgba(255,255,255,0.06);
          }}
          .brand-url {{
            font-size: 13px;
            font-weight: 600;
            color: rgba(255,255,255,0.35);
            letter-spacing: 1px;
          }}
          .handle-section {{
            text-align: right;
          }}
          .handle {{
            font-size: 16px;
            font-weight: 600;
            color: {accent};
          }}
          .handle-tagline {{
            font-size: 11px;
            font-weight: 600;
            color: rgba(255,255,255,0.35);
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 5px;
          }}
        </style>
        </head>
        <body>
        <div class="card">
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="orb orb-3"></div>
          <div class="noise"></div>
          <div class="grid"></div>
          <div class="top-line"></div>
          <div class="content">
            <div class="pillar">
              <div class="pillar-dot"></div>
              <div class="pillar-text">{pillar_text}</div>
            </div>
            <div class="hero">
              {hero_stat_markup}
              <div class="stat-label">{html.escape(support_line)}</div>
            </div>
            <div class="chip-row">
              {_data_item_markup(*chip_items[0], class_name="chip")}
              {_data_item_markup(*chip_items[1], class_name="chip")}
            </div>
            <div class="quote-panel">
              <div class="quote-mark">&ldquo;</div>
              <div class="quote-text">{quote_markup}</div>
              <div class="quote-mark-close">&rdquo;</div>
            </div>
            <div class="speaker-section">
              <div class="speaker-info">
                <div class="speaker-name">{signature_name}</div>
                <div class="speaker-title">{signature_title}</div>
              </div>
              {speaker_markup}
            </div>
            <div class="bottom-line"></div>
            <div class="brand-row">
              <div class="brand-left">
                {logo_markup}
                <div class="brand-divider"></div>
                <div class="brand-url">{website}</div>
              </div>
              <div class="handle-section">
                <div class="handle">{html.escape(brand.social_handle)}</div>
                <div class="handle-tagline">{handle_tagline}</div>
              </div>
            </div>
          </div>
        </div>
        </body>
        </html>
        """
    ).strip()


def _load_brand(path: Path) -> BrandSystem:
    data = _load_yaml(path)
    if not isinstance(data, dict):
        raise StoreError(f"brand system did not load as a mapping: {path}")
    return BrandSystem(
        name=str(data.get("name", "NRG Bloom")),
        tagline=str(data.get("tagline", "")),
        social_handle=str(data.get("social_handle", "@NRGBloom")),
        assets=dict(data.get("assets", {})),
        signature=dict(data.get("signature", {})),
        colors=dict(data.get("colors", {})),
        fonts=dict(data.get("fonts", {})),
        voice=dict(data.get("voice", {})),
        design=dict(data.get("design", {})),
    )


def _load_brief(data: Any) -> ContentBrief:
    if not isinstance(data, dict):
        raise StoreError("content brief must be an object")
    proof_points = [str(item) for item in data.get("proof_points", [])]
    if len(proof_points) < 3:
        raise StoreError("content brief requires at least 3 proof_points")
    return ContentBrief(
        slug=str(data["slug"]),
        title=str(data["title"]),
        publish_day=str(data["publish_day"]),
        archetype=str(data["archetype"]),
        pillar=str(data["pillar"]),
        target_channel=str(data["target_channel"]),
        audience=[str(item) for item in data.get("audience", [])],
        hero_stat=str(data["hero_stat"]),
        hook=str(data["hook"]),
        thesis=str(data["thesis"]),
        proof_points=proof_points,
        contrarian_take=str(data["contrarian_take"]),
        call_to_action=str(data["call_to_action"]),
        discussion_question=str(data["discussion_question"]),
        quote=str(data["quote"]),
        quote_highlights=[str(item) for item in data.get("quote_highlights", [])],
        video_hook=str(data["video_hook"]),
        video_close=str(data["video_close"]),
        hashtags=[str(item) for item in data.get("hashtags", [])],
        fact_ids=[str(item) for item in data.get("fact_ids", [])],
    )


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _copy_brand_assets(base_dir: Path, assets: dict[str, str], output_dir: Path) -> dict[str, Path]:
    copied: dict[str, Path] = {}
    for key, raw in assets.items():
        asset_raw = str(raw).strip()
        if not asset_raw:
            continue
        source_path = _resolve_path(base_dir, asset_raw)
        if not source_path.exists():
            continue
        suffix = source_path.suffix or ".bin"
        destination = output_dir / f"brand-{key.replace('_', '-')}{suffix}"
        shutil.copyfile(source_path, destination)
        copied[key] = destination
    return copied


def _relative_asset_ref(from_dir: Path, asset_path: Path | None) -> str | None:
    if asset_path is None:
        return None
    return Path(os.path.relpath(asset_path, start=from_dir)).as_posix()


def _quote_html_markup(text: str, highlights: list[str], *, accent_class: str) -> str:
    rendered = html.escape(text)
    for phrase in highlights:
        safe_phrase = html.escape(phrase)
        rendered = rendered.replace(safe_phrase, f'<span class="{accent_class}">{safe_phrase}</span>', 1)
    return rendered


def _quote_cards_index_html(*, campaign_title: str, brand: BrandSystem, cards: list[dict[str, str]]) -> str:
    card_markup = "\n".join(
        f"""
        <a class="card" href="{html.escape(item['html'])}">
          <div class="eyebrow">Quote Card</div>
          <div class="title">{html.escape(item['title'])}</div>
          <div class="meta">{html.escape(item['html'])}</div>
          <div class="meta">{html.escape(item['png'])}</div>
        </a>
        """.strip()
        for item in cards
    )
    return dedent(
        f"""
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{html.escape(campaign_title)} Quote Cards</title>
          <style>
            * {{ box-sizing: border-box; }}
            body {{
              margin: 0;
              padding: 48px;
              font-family: Inter, Arial, sans-serif;
              background: #050814;
              color: #fff;
            }}
            h1 {{
              margin: 0 0 12px;
              font-size: 42px;
            }}
            p {{
              margin: 0 0 30px;
              color: rgba(255,255,255,0.65);
              font-size: 18px;
            }}
            .grid {{
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
              gap: 20px;
            }}
            .card {{
              display: block;
              padding: 24px;
              border-radius: 20px;
              background: #0f172a;
              border: 1px solid rgba(107,163,232,0.18);
              text-decoration: none;
              color: inherit;
            }}
            .eyebrow {{
              color: #6ba3e8;
              text-transform: uppercase;
              letter-spacing: 0.12em;
              font-size: 12px;
              font-weight: 700;
            }}
            .title {{
              margin-top: 14px;
              font-size: 28px;
              font-weight: 800;
              line-height: 1.1;
            }}
            .meta {{
              margin-top: 12px;
              color: rgba(255,255,255,0.5);
              font-size: 14px;
            }}
          </style>
        </head>
        <body>
          <h1>{html.escape(brand.name)} Quote Cards</h1>
          <p>{html.escape(campaign_title)} / portrait quote assets for X and LinkedIn.</p>
          <div class="grid">
            {card_markup}
          </div>
        </body>
        </html>
        """
    ).strip()


def _render_quote_card_png(
    *,
    path: Path,
    brand: BrandSystem,
    brief: ContentBrief,
    logo_path: Path | None,
    speaker_photo_path: Path | None,
) -> None:
    width = 1080
    height = 1350
    background = brand.colors.get("quote_background", "#1A2D4A")
    image = Image.new("RGBA", (width, height), _hex_to_rgba(background))
    draw = ImageDraw.Draw(image)

    accent = brand.colors.get("quote_accent", "#6BA3E8")
    accent_deep = brand.colors.get("quote_accent_deep", "#14489B")
    quote_surface = brand.colors.get("quote_surface", "#14233A")
    white = (255, 255, 255, 255)
    muted = (255, 255, 255, 89)
    stat_number, stat_unit, stat_tail = _hero_stat_parts(brief.hero_stat)
    hero_display_text, support_text = _hero_display_copy(brief, stat_number, stat_tail)
    support_line = _short_card_text(support_text, 140)

    draw.rectangle((0, 0, width, 3), fill=_hex_to_rgba(accent))
    _draw_blur_orb(image, center=(150, 120), radius=340, color=_hex_to_rgba(accent_deep, alpha=54))
    _draw_blur_orb(image, center=(930, 1160), radius=260, color=_hex_to_rgba(accent, alpha=38))
    _draw_blur_orb(image, center=(760, 620), radius=170, color=_hex_to_rgba(accent_deep, alpha=24))
    _draw_grid_overlay(image, color=_hex_to_rgba(accent, alpha=10), step=54)
    _draw_noise_overlay(image, opacity=10)

    pillar_font = _load_font(size=14, bold=True)
    hero_font = _load_font(size=66, bold=True)
    stat_number_font = _load_mono_font(size=132, bold=True)
    stat_unit_font = _load_mono_font(size=42, bold=True)
    body_font = _load_font(size=20, bold=False)
    data_kicker_font = _load_mono_font(size=14, bold=True)
    data_text_font = _load_font(size=16, bold=True)
    quote_mark_font = _load_font(size=64, bold=True)
    quote_font = _load_font(size=30, bold=True)
    speaker_name_font = _load_font(size=22, bold=True)
    speaker_title_font = _load_font(size=14, bold=True)
    handle_font = _load_font(size=16, bold=True)
    small_font = _load_font(size=13, bold=True)

    content_x = 80
    draw.ellipse((content_x, 77, content_x + 8, 85), fill=_hex_to_rgba(accent))
    draw.text((content_x + 20, 66), brief.pillar.replace("-", " ").upper(), font=pillar_font, fill=_hex_to_rgba(accent))

    current_y = 124
    if stat_number:
        draw.text((content_x, current_y), stat_number, font=stat_number_font, fill=white)
        number_box = draw.textbbox((content_x, current_y), stat_number, font=stat_number_font)
        if stat_unit:
            draw.text((number_box[2] + 10, current_y + 68), stat_unit.upper(), font=stat_unit_font, fill=white)
        current_y = number_box[3] + 14
    else:
        wrapped_hero = _wrap_text(draw, hero_display_text, hero_font, max_width=820)
        draw.multiline_text((content_x, current_y), wrapped_hero, font=hero_font, fill=white, spacing=2)
        hero_box = draw.multiline_textbbox((content_x, current_y), wrapped_hero, font=hero_font, spacing=2)
        current_y = hero_box[3] + 16

    wrapped_tail = _wrap_text(draw, support_line, body_font, max_width=720)
    draw.multiline_text((content_x, current_y), wrapped_tail, font=body_font, fill=muted, spacing=8)
    tail_box = draw.multiline_textbbox((content_x, current_y), wrapped_tail, font=body_font, spacing=8)
    current_y = tail_box[3] + 24

    chip_height = 94
    chip_gap = 14
    chip_width = int((width - 160 - chip_gap) / 2)
    chip_items = [("SIGNAL", _short_card_text(brief.proof_points[0], 54)), ("EDGE", _short_card_text(brief.contrarian_take, 54))]
    for index, (label, value) in enumerate(chip_items):
        chip_x = 80 + index * (chip_width + chip_gap)
        chip_box = (chip_x, current_y, chip_x + chip_width, current_y + chip_height)
        draw.rounded_rectangle(chip_box, radius=16, fill=_hex_to_rgba(accent_deep, alpha=42), outline=_hex_to_rgba(accent, alpha=46), width=1)
        draw.text((chip_x + 18, current_y + 14), label, font=data_kicker_font, fill=_hex_to_rgba(accent))
        wrapped_value = _wrap_text(draw, value, data_text_font, max_width=chip_width - 36)
        draw.multiline_text((chip_x + 18, current_y + 38), wrapped_value, font=data_text_font, fill=white, spacing=4)

    quote_top = current_y + chip_height + 28
    quote_box = (80, quote_top, width - 80, quote_top + 290)
    draw.rounded_rectangle(quote_box, radius=24, fill=_hex_to_rgba(quote_surface), outline=(255, 255, 255, 20), width=1)
    draw.text((118, quote_top + 34), "“", font=quote_mark_font, fill=_hex_to_rgba(accent, alpha=230))
    wrapped_quote = _wrap_text(draw, brief.quote, quote_font, max_width=800)
    draw.multiline_text((124, quote_top + 98), wrapped_quote, font=quote_font, fill=white, spacing=10)
    draw.text((width - 150, quote_top + 216), "”", font=quote_mark_font, fill=_hex_to_rgba(accent, alpha=230))

    signature_name = str(brand.signature.get("name", brand.name))
    signature_title = str(brand.signature.get("title", brand.tagline)).upper()
    name_box = draw.textbbox((0, 0), signature_name, font=speaker_name_font)
    name_width = name_box[2] - name_box[0]
    speaker_right = width - 60
    photo_size = 110
    photo_x = speaker_right - photo_size
    photo_y = quote_box[3] + 26
    info_right = photo_x - 20
    draw.text((info_right - name_width, photo_y + 20), signature_name, font=speaker_name_font, fill=white)
    title_box = draw.textbbox((0, 0), signature_title, font=speaker_title_font)
    title_width = title_box[2] - title_box[0]
    draw.text((info_right - title_width, photo_y + 54), signature_title, font=speaker_title_font, fill=_hex_to_rgba(accent))

    if speaker_photo_path and speaker_photo_path.exists():
        _paste_circular_photo(
            image=image,
            photo_path=speaker_photo_path,
            x=photo_x,
            y=photo_y,
            size=photo_size,
            ring_light=accent,
            ring_dark=accent_deep,
        )

    footer_line_y = photo_y + photo_size + 40
    draw.line((80, footer_line_y, width - 80, footer_line_y), fill=(255, 255, 255, 20), width=1)

    brand_y = footer_line_y + 46
    cursor_x = 80
    if logo_path and logo_path.exists():
        cursor_x = _paste_logo(image, logo_path, x=80, y=brand_y - 6, target_height=50) + 20
    else:
        fallback_font = _load_font(size=26, bold=True)
        draw.text((80, brand_y), brand.name, font=fallback_font, fill=white)
        fallback_box = draw.textbbox((80, brand_y), brand.name, font=fallback_font)
        cursor_x = fallback_box[2] + 20
    draw.line((cursor_x, brand_y + 2, cursor_x, brand_y + 38), fill=(255, 255, 255, 15), width=1)
    website = str(brand.signature.get("website", "nrgbloom.com"))
    draw.text((cursor_x + 20, brand_y + 18), website, font=small_font, fill=muted)

    handle = brand.social_handle
    handle_box = draw.textbbox((0, 0), handle, font=handle_font)
    handle_width = handle_box[2] - handle_box[0]
    handle_x = width - 60 - handle_width
    draw.text((handle_x, brand_y + 8), handle, font=handle_font, fill=_hex_to_rgba(accent))
    handle_tagline = str(brand.signature.get("handle_tagline", brand.tagline)).upper()
    tagline_box = draw.textbbox((0, 0), handle_tagline, font=small_font)
    tagline_width = tagline_box[2] - tagline_box[0]
    draw.text((width - 60 - tagline_width, brand_y + 38), handle_tagline, font=small_font, fill=muted)

    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path)


def _hex_to_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        return (255, 255, 255, alpha)
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4)) + (alpha,)


def _hero_stat_parts(hero_stat: str) -> tuple[str | None, str | None, str | None]:
    match = re.match(r"^\s*([0-9][0-9,./]*)(?:\s*([A-Za-z%$]+))?(?:\s+(.*))?$", hero_stat.strip())
    if not match:
        return None, None, hero_stat.strip() or None
    number = match.group(1)
    unit = match.group(2) or None
    tail = match.group(3) or None
    return number, unit, tail


def _hero_display_copy(brief: ContentBrief, stat_number: str | None, stat_tail: str | None) -> tuple[str, str]:
    if stat_number:
        return brief.hero_stat, stat_tail or brief.title
    return brief.title, brief.hero_stat


def _hero_stat_markup(stat_number: str | None, stat_unit: str | None, hero_stat: str) -> str:
    if stat_number:
        unit_markup = f'<div class="stat-unit">{html.escape(stat_unit.upper())}</div>' if stat_unit else ""
        return (
            '<div class="stat-row">'
            f'<div class="stat-number">{html.escape(stat_number)}</div>'
            f"{unit_markup}"
            "</div>"
        )
    return f'<div class="hero-headline">{html.escape(hero_stat)}</div>'


def _data_item_markup(label: str, value: str, *, class_name: str = "data-item") -> str:
    return dedent(
        f"""
        <div class="{html.escape(class_name)}">
          <div class="data-kicker">{html.escape(label)}</div>
          <div class="data-desc">{html.escape(value)}</div>
        </div>
        """
    ).strip()


def _short_card_text(text: str, limit: int) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    trimmed = clean[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    if not trimmed:
        trimmed = clean[: limit - 1].rstrip(" ,;:")
    return trimmed + "..."


def _draw_blur_orb(image: Image.Image, *, center: tuple[int, int], radius: int, color: tuple[int, int, int, int]) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=100))
    image.alpha_composite(overlay)


def _draw_grid_overlay(image: Image.Image, *, color: tuple[int, int, int, int], step: int) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = image.size
    for x in range(0, width, step):
        draw.line((x, 0, x, height), fill=color, width=1)
    for y in range(0, height, step):
        draw.line((0, y, width, y), fill=color, width=1)
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((-220, -140, 980, 940), fill=180)
    overlay.putalpha(mask)
    image.alpha_composite(overlay)


def _draw_noise_overlay(image: Image.Image, *, opacity: int) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = overlay.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            if (x * 17 + y * 29) % 23 == 0:
                pixels[x, y] = (255, 255, 255, opacity)
    image.alpha_composite(overlay)


def _load_font(*, size: int, bold: bool) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        font_path = Path(candidate)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def _load_mono_font(*, size: int, bold: bool) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]
    for candidate in candidates:
        font_path = Path(candidate)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return _load_font(size=size, bold=bold)


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


def _paste_logo(image: Image.Image, logo_path: Path, *, x: int, y: int, target_height: int) -> int:
    logo = Image.open(logo_path).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    ratio = target_height / max(logo.height, 1)
    target_width = max(int(logo.width * ratio), 1)
    logo = logo.resize((target_width, target_height), Image.LANCZOS)
    alpha = logo.getchannel("A")
    white_logo = Image.new("RGBA", logo.size, (255, 255, 255, 255))
    white_logo.putalpha(alpha)
    image.alpha_composite(white_logo, (x, y))
    return x + target_width


def _paste_circular_photo(
    *,
    image: Image.Image,
    photo_path: Path,
    x: int,
    y: int,
    size: int,
    ring_light: str,
    ring_dark: str,
) -> None:
    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse((0, 0, size - 1, size - 1), fill=_hex_to_rgba(ring_light))
    ring_draw.ellipse((4, 4, size - 5, size - 5), fill=(0, 0, 0, 255))
    ring_draw.arc((0, 0, size - 1, size - 1), start=35, end=215, fill=_hex_to_rgba(ring_dark), width=8)

    photo = Image.open(photo_path).convert("RGBA")
    photo = ImageOps.fit(photo, (size - 14, size - 14), Image.LANCZOS, centering=(0.5, 0.22))
    photo = ImageEnhance.Brightness(photo).enhance(0.78)
    photo = ImageEnhance.Contrast(photo).enhance(1.12)
    mask = Image.new("L", photo.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, photo.width - 1, photo.height - 1), fill=255)
    photo.putalpha(mask)
    ring.alpha_composite(photo, (7, 7))
    image.alpha_composite(ring, (x, y))
