#!/usr/bin/env python3
"""Fix images 5 and 6."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1080
output_dir = os.path.expanduser('~/.openclaw/workspace/agents/nano-banana/output')

FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'

def font(size):
    return ImageFont.truetype(FONT_PATH, size)

def text_center_x(draw, text, y, fnt, fill, img_w=W):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (img_w - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)

def rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# =========================================================
# Image 5: Audience Recommendations (fix emoji → use text labels)
# =========================================================
def gen_audience():
    img = Image.new('RGB', (W, H), '#fafafe')
    draw = ImageDraw.Draw(img)
    
    # Title
    title_font = font(48)
    text_center_x(draw, "你是哪类开发者？", 60, title_font, '#1e293b')
    
    # Four recommendation cards in 2x2 grid (no emoji, use text icons)
    recs = [
        {'audience': '独立开发者', 'icon': '< / >', 'rec': 'OpenCode', 'reason': '灵活 · 开源 · 省钱', 'color': '#22c55e', 'bg': '#f0fdf4', 'icon_color': '#22c55e'},
        {'audience': '团队协作', 'icon': 'TEAM', 'rec': 'Claude Code', 'reason': '稳定 · 质量 · 规范', 'color': '#3b82f6', 'bg': '#eff6ff', 'icon_color': '#3b82f6'},
        {'audience': 'OpenAI 用户', 'icon': 'GPT', 'rec': 'Codex', 'reason': '无缝 · 整合 · 熟悉', 'color': '#f97316', 'bg': '#fff7ed', 'icon_color': '#f97316'},
        {'audience': '编程新手', 'icon': 'NEW', 'rec': 'OpenCode', 'reason': '社区 · 教程 · 免费', 'color': '#22c55e', 'bg': '#f0fdf4', 'icon_color': '#22c55e'},
    ]
    
    card_w = 440
    card_h = 330
    gap_x = 50
    gap_y = 50
    grid_w = card_w * 2 + gap_x
    grid_h = card_h * 2 + gap_y
    base_x = (W - grid_w) // 2
    base_y = (H - grid_h) // 2 + 40
    
    for i, r in enumerate(recs):
        col = i % 2
        row = i // 2
        x = base_x + col * (card_w + gap_x)
        y = base_y + row * (card_h + gap_y)
        
        # Card
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, r['bg'], outline=r['color'], width=3)
        
        # Icon badge (small rounded rect instead of emoji)
        icon_font = font(20)
        badge_w = 60
        badge_h = 30
        badge_x = x + (card_w - badge_w) // 2
        badge_y = y + 25
        rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 8, r['color'])
        bbox = draw.textbbox((0, 0), r['icon'], font=icon_font)
        iw = bbox[2] - bbox[0]
        draw.text((badge_x + (badge_w - iw) // 2, badge_y + 3), r['icon'], font=icon_font, fill='#ffffff')
        
        # Audience label
        aud_font = font(32)
        bbox = draw.textbbox((0, 0), r['audience'], font=aud_font)
        aw = bbox[2] - bbox[0]
        draw.text((x + (card_w - aw) // 2, y + 75), r['audience'], font=aud_font, fill='#333333')
        
        # Arrow down
        arrow_font = font(28)
        bbox = draw.textbbox((0, 0), "|", font=arrow_font)
        aw2 = bbox[2] - bbox[0]
        # Draw a simple down arrow with lines
        mid_x = x + card_w // 2
        draw.line([(mid_x, y + 125), (mid_x, y + 155)], fill='#bbbbbb', width=2)
        draw.polygon([(mid_x - 8, y + 150), (mid_x + 8, y + 150), (mid_x, y + 165)], fill='#bbbbbb')
        
        # Recommendation
        rec_font = font(42)
        bbox = draw.textbbox((0, 0), r['rec'], font=rec_font)
        rw = bbox[2] - bbox[0]
        draw.text((x + (card_w - rw) // 2, y + 175), r['rec'], font=rec_font, fill=r['color'])
        
        # Reason
        reason_font = font(24)
        bbox = draw.textbbox((0, 0), r['reason'], font=reason_font)
        rew = bbox[2] - bbox[0]
        draw.text((x + (card_w - rew) // 2, y + 250), r['reason'], font=reason_font, fill='#777777')
    
    img.save(os.path.join(output_dir, '05_audience.png'))
    print("✅ 05_audience.png fixed")

# =========================================================
# Image 6: Conclusion Quote (fix quote marks rendering as code)
# =========================================================
def gen_conclusion():
    img = Image.new('RGB', (W, H), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Subtle grid lines for tech feel
    for i in range(0, W, 80):
        draw.line([(i, 0), (i, H)], fill='#1a2744', width=1)
    for i in range(0, H, 80):
        draw.line([(0, i), (W, i)], fill='#1a2744', width=1)
    
    # Decorative quote marks - use simple ASCII-safe drawing instead of font
    # Left quote mark - draw two circles with tails
    for offset in [0, 50]:
        cx, cy = 160 + offset, 310
        draw.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill='#3a7bfd')
        draw.polygon([(cx - 15, cy), (cx - 25, cy + 35), (cx + 5, cy + 10)], fill='#3a7bfd')
    
    # Right quote mark
    for offset in [0, 50]:
        cx, cy = 840 + offset, 620
        draw.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill='#3a7bfd')
        draw.polygon([(cx + 15, cy), (cx + 25, cy - 35), (cx - 5, cy - 10)], fill='#3a7bfd')
    
    # Main quote
    main_font = font(56)
    text_center_x(draw, "没有最好的工具", 400, main_font, '#ffffff')
    text_center_x(draw, "只有最适合你的", 480, main_font, '#ffffff')

    # Decorative line
    line_w = 200
    lx = (W - line_w) // 2
    draw.line([(lx, 580), (lx + line_w, 580)], fill='#3a7bfd', width=3)
    
    # Subtitle
    sub_font = font(28)
    text_center_x(draw, "选对工具，事半功倍", 620, sub_font, '#64748b')
    
    # Bottom branding
    brand_font = font(22)
    text_center_x(draw, "OpenCode | Claude Code | Codex  -  选型指南", 920, brand_font, '#475569')
    
    # Corner accents
    draw.line([(40, 40), (120, 40)], fill='#3a7bfd', width=3)
    draw.line([(40, 40), (40, 120)], fill='#3a7bfd', width=3)
    draw.line([(W-120, H-40), (W-40, H-40)], fill='#3a7bfd', width=3)
    draw.line([(W-40, H-120), (W-40, H-40)], fill='#3a7bfd', width=3)
    
    img.save(os.path.join(output_dir, '06_conclusion.png'))
    print("✅ 06_conclusion.png fixed")

gen_audience()
gen_conclusion()
print("\n🎉 Fixed images regenerated!")
