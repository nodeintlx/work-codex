#!/usr/bin/env python3
"""
Professional Markdown-to-PDF converter.

Renders markdown documents as clean, human-quality PDFs using pymupdf.
No HTML rendering engine — direct text placement for pixel-perfect control.

Usage:
    python3 md_to_pdf.py input.md output.pdf [--title "Document Title"]
"""

import fitz
import re
import sys
import textwrap

# ─── Page Configuration ───────────────────────────────────────────────────────
PAGE_WIDTH = 612       # Letter width in points
PAGE_HEIGHT = 792      # Letter height in points
MARGIN_LEFT = 60
MARGIN_RIGHT = 60
MARGIN_TOP = 65
MARGIN_BOTTOM = 55
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# ─── Typography ───────────────────────────────────────────────────────────────
FONT_BODY = "helv"
FONT_BOLD = "hebo"
FONT_ITALIC = "heit"
FONT_MONO = "cour"

SIZE_H1 = 16
SIZE_H2 = 13
SIZE_H3 = 11
SIZE_H4 = 10
SIZE_BODY = 9.5
SIZE_TABLE = 8.5
SIZE_SMALL = 7.5
SIZE_FOOTER = 7.5

COLOR_BLACK = (0.1, 0.1, 0.1)
COLOR_DARK = (0.2, 0.2, 0.2)
COLOR_GRAY = (0.4, 0.4, 0.4)
COLOR_LIGHT_GRAY = (0.55, 0.55, 0.55)
COLOR_RULE = (0.75, 0.75, 0.75)
COLOR_TABLE_HEADER_BG = (0.22, 0.27, 0.34)
COLOR_TABLE_HEADER_TEXT = (1, 1, 1)
COLOR_TABLE_ALT_BG = (0.95, 0.96, 0.97)
COLOR_TABLE_BORDER = (0.8, 0.82, 0.84)


class PDFWriter:
    """Writes a professional PDF document from parsed markdown content."""

    def __init__(self, output_path, header_text="", footer_prefix="Page"):
        self.output_path = output_path
        self.header_text = header_text
        self.footer_prefix = footer_prefix
        self.doc = fitz.open()
        self.page = None
        self.y = MARGIN_TOP
        self.page_num = 0
        self._new_page()

    def _new_page(self):
        """Create a new page."""
        self.page = self.doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        self.page_num += 1
        self.y = MARGIN_TOP

    def _need_space(self, height):
        """Check if we need a new page, and create one if so."""
        if self.y + height > PAGE_HEIGHT - MARGIN_BOTTOM:
            self._new_page()
            return True
        return False

    def _text_width(self, text, fontname, fontsize):
        """Calculate the width of a text string."""
        font = fitz.Font(fontname)
        return font.text_length(text, fontsize=fontsize)

    def _write_text_line(self, text, fontname, fontsize, color, x=None, max_width=None):
        """Write a single line of text. Returns the y position after writing."""
        if x is None:
            x = MARGIN_LEFT
        if max_width is None:
            max_width = CONTENT_WIDTH
        self.page.insert_text(
            fitz.Point(x, self.y),
            text,
            fontname=fontname,
            fontsize=fontsize,
            color=color,
        )

    def _wrap_and_write(self, text, fontname, fontsize, color, x=None,
                        max_width=None, line_spacing=1.45, indent=0):
        """Word-wrap text and write it. Returns total height used."""
        if x is None:
            x = MARGIN_LEFT + indent
        if max_width is None:
            max_width = CONTENT_WIDTH - indent

        line_height = fontsize * line_spacing
        font = fitz.Font(fontname)

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test = (current_line + " " + word).strip()
            w = font.text_length(test, fontsize=fontsize)
            if w > max_width and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test
        if current_line:
            lines.append(current_line)

        if not lines:
            return 0

        # Write line-by-line with per-line page break handling
        total_height = 0
        for line in lines:
            if self.y + line_height > PAGE_HEIGHT - MARGIN_BOTTOM:
                self._new_page()
            self.page.insert_text(
                fitz.Point(x, self.y),
                line,
                fontname=fontname,
                fontsize=fontsize,
                color=color,
            )
            self.y += line_height
            total_height += line_height

        return total_height

    def _write_rich_text(self, segments, fontsize, x=None, max_width=None,
                         line_spacing=1.45, indent=0):
        """
        Write text with mixed bold/regular formatting.
        segments: list of (text, fontname, color) tuples.
        Writes line-by-line with per-line page break handling so long
        content flows naturally across pages.
        """
        if x is None:
            x = MARGIN_LEFT + indent
        if max_width is None:
            max_width = CONTENT_WIDTH - indent

        line_height = fontsize * line_spacing

        # Flatten all segments into words with their formatting
        styled_words = []
        for text, fontname, color in segments:
            words = text.split()
            for w in words:
                styled_words.append((w, fontname, color))

        if not styled_words:
            return

        # Build lines
        lines = []  # Each line is a list of (word, fontname, color)
        current_line = []
        current_width = 0

        for word, fn, col in styled_words:
            font = fitz.Font(fn)
            word_w = font.text_length(word + " ", fontsize=fontsize)
            if current_width + word_w > max_width and current_line:
                lines.append(current_line)
                current_line = [(word, fn, col)]
                current_width = word_w
            else:
                current_line.append((word, fn, col))
                current_width += word_w
        if current_line:
            lines.append(current_line)

        # Write line-by-line, checking page breaks per line
        for line in lines:
            if self.y + line_height > PAGE_HEIGHT - MARGIN_BOTTOM:
                self._new_page()
            cx = x
            for word, fn, col in line:
                self.page.insert_text(
                    fitz.Point(cx, self.y),
                    word + " ",
                    fontname=fn,
                    fontsize=fontsize,
                    color=col,
                )
                font = fitz.Font(fn)
                cx += font.text_length(word + " ", fontsize=fontsize)
            self.y += line_height

    def _parse_inline(self, text):
        """Parse inline markdown (bold, italic, code) into segments."""
        segments = []
        # Pattern: **bold**, *italic*, `code`, or plain text
        pattern = re.compile(r'(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|([^*`]+))')
        for m in pattern.finditer(text):
            if m.group(2):  # bold
                segments.append((m.group(2), FONT_BOLD, COLOR_BLACK))
            elif m.group(3):  # italic
                segments.append((m.group(3), FONT_ITALIC, COLOR_DARK))
            elif m.group(4):  # code
                segments.append((m.group(4), FONT_MONO, COLOR_DARK))
            elif m.group(5):  # plain
                segments.append((m.group(5), FONT_BODY, COLOR_BLACK))
        return segments if segments else [(text, FONT_BODY, COLOR_BLACK)]

    def write_h1(self, text):
        """Write a level-1 heading."""
        text = text.strip()
        self._need_space(SIZE_H1 * 3)
        self.y += 10
        self._wrap_and_write(text, FONT_BOLD, SIZE_H1, COLOR_BLACK, line_spacing=1.3)
        # Draw rule under heading
        rule_y = self.y + 2
        self.page.draw_line(
            fitz.Point(MARGIN_LEFT, rule_y),
            fitz.Point(PAGE_WIDTH - MARGIN_RIGHT, rule_y),
            color=COLOR_BLACK, width=1.5
        )
        self.y = rule_y + 14  # Generous gap between rule and content below

    def write_h2(self, text):
        """Write a level-2 heading."""
        text = text.strip()
        self._need_space(SIZE_H2 * 3)
        self.y += 8
        self._wrap_and_write(text, FONT_BOLD, SIZE_H2, COLOR_DARK, line_spacing=1.3)
        rule_y = self.y + 1
        self.page.draw_line(
            fitz.Point(MARGIN_LEFT, rule_y),
            fitz.Point(PAGE_WIDTH - MARGIN_RIGHT, rule_y),
            color=COLOR_RULE, width=0.5
        )
        self.y = rule_y + 12  # Clear gap between rule and content below

    def write_h3(self, text):
        """Write a level-3 heading."""
        text = text.strip()
        self._need_space(SIZE_H3 * 2.5)
        self.y += 6
        self._wrap_and_write(text, FONT_BOLD, SIZE_H3, COLOR_DARK, line_spacing=1.3)
        self.y += 2

    def write_h4(self, text):
        """Write a level-4 heading."""
        text = text.strip()
        self._need_space(SIZE_H4 * 2)
        self.y += 4
        self._wrap_and_write(text, FONT_BOLD, SIZE_H4, COLOR_DARK, line_spacing=1.3)
        self.y += 1

    def write_paragraph(self, text):
        """Write a paragraph with inline formatting support."""
        text = text.strip()
        if not text:
            return
        segments = self._parse_inline(text)
        self._need_space(SIZE_BODY * 2)
        self._write_rich_text(segments, SIZE_BODY)
        self.y += 3

    def write_bullet(self, text, level=0):
        """Write a bullet list item."""
        text = text.strip()
        indent = 12 + (level * 14)
        bullet_x = MARGIN_LEFT + indent
        text_indent = indent + 10

        # Pre-check: ensure bullet and at least first line stay together
        self._need_space(SIZE_BODY * 1.45 * 2)

        # Draw bullet
        bullet_char = "\u2022" if level == 0 else "-"
        self.page.insert_text(
            fitz.Point(bullet_x, self.y),
            bullet_char,
            fontname=FONT_BODY,
            fontsize=SIZE_BODY,
            color=COLOR_GRAY,
        )

        # Write text with inline formatting (flows across pages for long items)
        segments = self._parse_inline(text)
        self._write_rich_text(segments, SIZE_BODY, indent=text_indent)
        self.y += 1

    def write_numbered_item(self, number, text, level=0):
        """Write a numbered list item."""
        text = text.strip()
        indent = 12 + (level * 14)
        num_x = MARGIN_LEFT + indent
        text_indent = indent + 16

        # Pre-check: ensure number and at least first line stay together
        self._need_space(SIZE_BODY * 1.45 * 2)

        self.page.insert_text(
            fitz.Point(num_x, self.y),
            f"{number}.",
            fontname=FONT_BOLD,
            fontsize=SIZE_BODY,
            color=COLOR_DARK,
        )

        # Write text with inline formatting (flows across pages for long items)
        segments = self._parse_inline(text)
        self._write_rich_text(segments, SIZE_BODY, indent=text_indent)
        self.y += 1

    def write_hr(self):
        """Write a horizontal rule."""
        self.y += 8
        self.page.draw_line(
            fitz.Point(MARGIN_LEFT, self.y),
            fitz.Point(PAGE_WIDTH - MARGIN_RIGHT, self.y),
            color=COLOR_RULE, width=0.5
        )
        self.y += 12  # Clear gap between rule and content below

    def write_table(self, headers, rows):
        """Write a formatted table."""
        if not headers:
            return

        num_cols = len(headers)
        # Calculate column widths proportional to content
        col_widths = self._calc_col_widths(headers, rows, num_cols)

        row_height = SIZE_TABLE * 1.8
        header_height = SIZE_TABLE * 2.0
        padding = 5

        # Estimate total table height
        total_height = header_height
        for row in rows:
            # Estimate row height based on longest cell content
            max_lines = 1
            for i, cell in enumerate(row):
                cell_text = self._strip_markdown(cell)
                font = fitz.Font(FONT_BODY)
                text_w = font.text_length(cell_text, fontsize=SIZE_TABLE)
                cell_w = col_widths[i] - (padding * 2)
                if cell_w > 0:
                    lines = max(1, int(text_w / cell_w) + 1)
                    max_lines = max(max_lines, lines)
            total_height += row_height * max_lines

        self._need_space(min(total_height, 200))  # At least try to keep table start on same page
        self.y += 4

        x_start = MARGIN_LEFT

        # ─── Draw header row ─────────────────────────────────────────────
        # Header uses same geometry: top → padding → baseline → bottom
        HDR_PAD_TOP = 6
        HDR_PAD_BOTTOM = 6
        header_top = self.y
        header_baseline = header_top + HDR_PAD_TOP + SIZE_TABLE
        header_bottom = header_baseline + 2 + HDR_PAD_BOTTOM

        # Header background
        self.page.draw_rect(
            fitz.Rect(x_start, header_top, x_start + sum(col_widths), header_bottom),
            color=None, fill=COLOR_TABLE_HEADER_BG
        )

        x = x_start
        for i, header in enumerate(headers):
            header_text = self._strip_markdown(header)
            self.page.insert_text(
                fitz.Point(x + padding, header_baseline),
                header_text,
                fontname=FONT_BOLD,
                fontsize=SIZE_TABLE,
                color=COLOR_TABLE_HEADER_TEXT,
            )
            x += col_widths[i]

        self.y = header_bottom + 4  # Gap between header bar and first data row

        # ─── Draw data rows ──────────────────────────────────────────────
        # Geometry: self.y is the TOP of the row area (not the text baseline).
        # Text baseline = row_top + ROW_PAD_TOP + SIZE_TABLE (ascent).
        # Row bottom = row_top + row_height.
        # Border line drawn at row_bottom. Next row starts at row_bottom.
        ROW_PAD_TOP = 5      # space from row-top edge to top of text ascenders
        ROW_PAD_BOTTOM = 5   # space from bottom of text descenders to row-bottom edge
        LINE_GAP = SIZE_TABLE * 1.5  # vertical distance between baselines for wrapped lines

        for row_idx, row in enumerate(rows):
            # Calculate wrapped lines per cell
            max_lines = 1
            cell_lines = []
            for i, cell in enumerate(row):
                cell_text = self._strip_markdown(cell)
                cell_w = col_widths[i] - (padding * 2) if i < len(col_widths) else 100
                wrapped = self._wrap_text(cell_text, FONT_BODY, SIZE_TABLE, cell_w)
                cell_lines.append(wrapped)
                max_lines = max(max_lines, len(wrapped))

            # Row height = padding + ascent + (extra lines * gap) + descender space + padding
            row_height = ROW_PAD_TOP + SIZE_TABLE + (max_lines - 1) * LINE_GAP + 2 + ROW_PAD_BOTTOM

            # Check if we need a new page
            if self.y + row_height > PAGE_HEIGHT - MARGIN_BOTTOM:
                self._new_page()
                self.y += 4
                # Redraw header on new page
                hdr_baseline = self.y + ROW_PAD_TOP + SIZE_TABLE
                hdr_top = self.y
                hdr_bottom = hdr_baseline + 5
                self.page.draw_rect(
                    fitz.Rect(x_start, hdr_top, x_start + sum(col_widths), hdr_bottom),
                    color=None, fill=COLOR_TABLE_HEADER_BG
                )
                x = x_start
                for i, header in enumerate(headers):
                    header_text = self._strip_markdown(header)
                    self.page.insert_text(
                        fitz.Point(x + padding, hdr_baseline),
                        header_text,
                        fontname=FONT_BOLD,
                        fontsize=SIZE_TABLE,
                        color=COLOR_TABLE_HEADER_TEXT,
                    )
                    x += col_widths[i]
                self.y = hdr_bottom + 6  # Gap after header before first data row

            row_top = self.y
            row_bottom = self.y + row_height
            first_baseline = row_top + ROW_PAD_TOP + SIZE_TABLE

            # Alternating row background
            if row_idx % 2 == 1:
                self.page.draw_rect(
                    fitz.Rect(x_start, row_top, x_start + sum(col_widths), row_bottom),
                    color=None, fill=COLOR_TABLE_ALT_BG
                )

            # Draw cell content
            x = x_start
            for i in range(num_cols):
                if i < len(cell_lines):
                    for j, line in enumerate(cell_lines[i]):
                        line_y = first_baseline + j * LINE_GAP

                        # Determine font — check if cell content is bold
                        cell_raw = row[i] if i < len(row) else ""
                        is_bold = cell_raw.strip().startswith("**") and cell_raw.strip().endswith("**")
                        fn = FONT_BOLD if is_bold else FONT_BODY

                        self.page.insert_text(
                            fitz.Point(x + padding, line_y),
                            line,
                            fontname=fn,
                            fontsize=SIZE_TABLE,
                            color=COLOR_BLACK,
                        )
                x += col_widths[i] if i < len(col_widths) else 0

            # Draw row border at the bottom edge of the row
            self.page.draw_line(
                fitz.Point(x_start, row_bottom),
                fitz.Point(x_start + sum(col_widths), row_bottom),
                color=COLOR_TABLE_BORDER, width=0.3
            )

            # Next row starts immediately at row_bottom (geometry is self-contained)
            self.y = row_bottom

        # Draw outer table border
        table_left = x_start
        table_right = x_start + sum(col_widths)

        # Vertical column dividers
        x = x_start
        for i in range(num_cols - 1):
            x += col_widths[i]
            # Only draw light vertical lines inside the header
            # Keep the rest clean

        self.y += 6

    def _calc_col_widths(self, headers, rows, num_cols):
        """Calculate proportional column widths based on content."""
        max_widths = []
        font = fitz.Font(FONT_BODY)

        for i in range(num_cols):
            header_w = font.text_length(self._strip_markdown(headers[i]), fontsize=SIZE_TABLE)
            max_w = header_w

            for row in rows[:10]:  # Sample first 10 rows
                if i < len(row):
                    cell_text = self._strip_markdown(row[i])
                    w = font.text_length(cell_text[:60], fontsize=SIZE_TABLE)
                    max_w = max(max_w, w)

            max_widths.append(max_w + 14)  # Add padding

        # Scale to fit content width
        total = sum(max_widths)
        if total > CONTENT_WIDTH:
            scale = CONTENT_WIDTH / total
            max_widths = [w * scale for w in max_widths]
        elif total < CONTENT_WIDTH * 0.7:
            # Expand smaller tables to at least 70% width
            scale = (CONTENT_WIDTH * 0.85) / total
            max_widths = [w * scale for w in max_widths]

        return max_widths

    def _wrap_text(self, text, fontname, fontsize, max_width):
        """Wrap text to fit within a given width. Returns list of lines."""
        font = fitz.Font(fontname)
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = (current + " " + word).strip()
            if font.text_length(test, fontsize=fontsize) > max_width and current:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)
        return lines if lines else [""]

    def _strip_markdown(self, text):
        """Remove markdown formatting characters from text."""
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        text = text.replace('---', '--').strip()
        return text

    def add_headers_footers(self):
        """Add headers and footers to all pages."""
        total = len(self.doc)
        for i, page in enumerate(self.doc):
            # Header - right aligned
            if self.header_text:
                page.insert_text(
                    fitz.Point(PAGE_WIDTH - MARGIN_RIGHT - 200, 30),
                    self.header_text,
                    fontname=FONT_BODY,
                    fontsize=SIZE_SMALL,
                    color=COLOR_LIGHT_GRAY,
                )
                # Right-align by measuring text width
                font = fitz.Font(FONT_BODY)
                tw = font.text_length(self.header_text, fontsize=SIZE_SMALL)
                # Overwrite with right-aligned version
                rect = fitz.Rect(MARGIN_LEFT, 22, PAGE_WIDTH - MARGIN_RIGHT, 38)
                page.draw_rect(rect, color=None, fill=(1, 1, 1))  # white out
                page.insert_text(
                    fitz.Point(PAGE_WIDTH - MARGIN_RIGHT - tw, 32),
                    self.header_text,
                    fontname=FONT_BODY,
                    fontsize=SIZE_SMALL,
                    color=COLOR_LIGHT_GRAY,
                )

            # Footer - centered
            footer_text = f"{self.footer_prefix} {i + 1} of {total}"
            font = fitz.Font(FONT_BODY)
            fw = font.text_length(footer_text, fontsize=SIZE_FOOTER)
            page.insert_text(
                fitz.Point((PAGE_WIDTH - fw) / 2, PAGE_HEIGHT - 30),
                footer_text,
                fontname=FONT_BODY,
                fontsize=SIZE_FOOTER,
                color=COLOR_LIGHT_GRAY,
            )

    def save(self):
        """Add headers/footers and save the document."""
        self.add_headers_footers()
        self.doc.save(self.output_path)
        self.doc.close()


def parse_markdown(md_text):
    """
    Parse markdown text into a list of content blocks.
    Each block is a dict with 'type' and content fields.
    """
    blocks = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_headers = []
    table_rows = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            if in_table:
                blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
                in_table = False
                table_headers = []
                table_rows = []
            i += 1
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___') or re.match(r'^-{3,}$', stripped):
            if in_table:
                blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
                in_table = False
                table_headers = []
                table_rows = []
            blocks.append({'type': 'hr'})
            i += 1
            continue

        # Headings
        h_match = re.match(r'^(#{1,4})\s+(.+)$', stripped)
        if h_match:
            if in_table:
                blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
                in_table = False
                table_headers = []
                table_rows = []
            level = len(h_match.group(1))
            text = h_match.group(2).strip()
            blocks.append({'type': f'h{level}', 'text': text})
            i += 1
            continue

        # Table row
        if '|' in stripped and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]  # Remove first/last empty

            # Check if this is a separator row (e.g., |---|---|)
            if all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue

            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            i += 1
            continue

        # Bullet list
        bullet_match = re.match(r'^(\s*)([-*+])\s+(.+)$', stripped)
        if bullet_match:
            if in_table:
                blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
                in_table = False
                table_headers = []
                table_rows = []
            indent = len(line) - len(line.lstrip())
            level = min(indent // 2, 2)
            text = bullet_match.group(3)
            blocks.append({'type': 'bullet', 'text': text, 'level': level})
            i += 1
            continue

        # Numbered list
        num_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', stripped)
        if num_match:
            if in_table:
                blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
                in_table = False
                table_headers = []
                table_rows = []
            number = num_match.group(2)
            text = num_match.group(3)
            blocks.append({'type': 'numbered', 'number': number, 'text': text})
            i += 1
            continue

        # Checkbox items
        check_match = re.match(r'^-\s*\[[ x]\]\s+(.+)$', stripped)
        if check_match:
            text = check_match.group(1)
            checked = '[x]' in stripped.lower()
            prefix = "[Done]" if checked else "[    ]"
            blocks.append({'type': 'bullet', 'text': f"{prefix}  {text}", 'level': 0})
            i += 1
            continue

        # Regular paragraph — collect continuation lines
        if in_table:
            blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})
            in_table = False
            table_headers = []
            table_rows = []

        para = stripped
        i += 1
        # Don't merge lines that look like separate items
        blocks.append({'type': 'paragraph', 'text': para})
        continue

    # Close any remaining table
    if in_table:
        blocks.append({'type': 'table', 'headers': table_headers, 'rows': table_rows})

    return blocks


def render_pdf(md_text, output_path, header_text=""):
    """Render markdown text to a professional PDF."""
    blocks = parse_markdown(md_text)
    pdf = PDFWriter(output_path, header_text=header_text)

    for block in blocks:
        btype = block['type']

        if btype == 'h1':
            pdf.write_h1(block['text'])
        elif btype == 'h2':
            pdf.write_h2(block['text'])
        elif btype == 'h3':
            pdf.write_h3(block['text'])
        elif btype == 'h4':
            pdf.write_h4(block['text'])
        elif btype == 'paragraph':
            pdf.write_paragraph(block['text'])
        elif btype == 'bullet':
            pdf.write_bullet(block['text'], level=block.get('level', 0))
        elif btype == 'numbered':
            pdf.write_numbered_item(block['number'], block['text'])
        elif btype == 'hr':
            pdf.write_hr()
        elif btype == 'table':
            pdf.write_table(block['headers'], block['rows'])

    pdf.save()

    import os
    size = os.path.getsize(output_path)
    pages = fitz.open(output_path).page_count
    print(f"PDF created: {output_path}")
    print(f"Pages: {pages}")
    print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 md_to_pdf.py input.md output.pdf [--header 'Header Text']")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    header = ""

    if "--header" in sys.argv:
        idx = sys.argv.index("--header")
        if idx + 1 < len(sys.argv):
            header = sys.argv[idx + 1]

    with open(input_path, 'r') as f:
        md = f.read()

    render_pdf(md, output_path, header_text=header)
