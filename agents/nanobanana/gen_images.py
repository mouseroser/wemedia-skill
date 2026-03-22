#!/usr/bin/env python3
"""Generate 6 Xiaohongshu images for Coding Agent comparison post."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1080
output_dir = os.path.expanduser('~/.openclaw/workspace/agents/nano-banana/output')
os.makedirs(output_dir, exist_ok=True)

FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'

def font(size):
    return ImageFont.truetype(FONT_PATH, size)

def text_center_x(draw, text, y, fnt, fill, img_w=W):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (img_w - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)

def rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# =========================================================
# Image 1: Cover - 封面图
# =========================================================
def gen_cover():
    img = Image.new('RGB', (W, H), '#0a0e27')
    draw = ImageDraw.Draw(img)
    
    # Subtle grid lines for tech feel
    for i in range(0, W, 60):
        draw.line([(i, 0), (i, H)], fill='#151b3a', width=1)
    for i in range(0, H, 60):
        draw.line([(0, i), (W, i)], fill='#151b3a', width=1)
    
    # Glowing circle accent
    for r in range(200, 0, -2):
        alpha = max(0, 15 - r // 15)
        color = (30, 80, 200, alpha)
        # Approximate glow with circles
    
    # Accent lines
    draw.line([(100, 380), (980, 380)], fill='#1e50c8', width=2)
    draw.line([(100, 700)], fill='#1e50c8', width=2) if False else None
    
    # Main title
    main_font = font(82)
    text_center_x(draw, "Coding Agent", 360, main_font, '#ffffff')
    text_center_x(draw, "怎么选？", 460, main_font, '#ffffff')
    
    # Decorative line
    line_w = 300
    lx = (W - line_w) // 2
    draw.line([(lx, 580), (lx + line_w, 580)], fill='#3a7bfd', width=3)
    
    # Subtitle
    sub_font = font(36)
    text_center_x(draw, "OpenCode · Claude Code · Codex", 620, sub_font, '#8899cc')
    
    # Bottom tag
    tag_font = font(28)
    text_center_x(draw, "2025 实用选型指南", 760, tag_font, '#556699')
    
    # Corner accents
    draw.line([(40, 40), (120, 40)], fill='#3a7bfd', width=3)
    draw.line([(40, 40), (40, 120)], fill='#3a7bfd', width=3)
    draw.line([(W-120, H-40), (W-40, H-40)], fill='#3a7bfd', width=3)
    draw.line([(W-40, H-120), (W-40, H-40)], fill='#3a7bfd', width=3)
    
    img.save(os.path.join(output_dir, '01_cover.png'))
    print("✅ 01_cover.png")

# =========================================================
# Image 2: Three Product Cards - 三产品定位图
# =========================================================
def gen_products():
    img = Image.new('RGB', (W, H), '#f5f5f5')
    draw = ImageDraw.Draw(img)
    
    # Title
    title_font = font(48)
    text_center_x(draw, "三大 Coding Agent 定位", 60, title_font, '#333333')
    
    # Three cards
    cards = [
        {'color': '#22c55e', 'bg': '#f0fdf4', 'name': 'OpenCode', 'tag': '开源自由派', 'icon': '🟢', 'desc': '模型自由切换\n社区驱动\n零授权费'},
        {'color': '#3b82f6', 'bg': '#eff6ff', 'name': 'Claude Code', 'tag': '商业稳定派', 'icon': '🔵', 'desc': '企业级质量\n深度集成\n稳定可靠'},
        {'color': '#f97316', 'bg': '#fff7ed', 'name': 'Codex', 'tag': '平台整合派', 'icon': '🟠', 'desc': 'OpenAI生态\nGPT深度整合\n云端优先'},
    ]
    
    card_w = 290
    card_h = 700
    gap = 35
    start_x = (W - (card_w * 3 + gap * 2)) // 2
    start_y = 180
    
    for i, c in enumerate(cards):
        x = start_x + i * (card_w + gap)
        y = start_y
        
        # Card background
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, c['bg'], outline=c['color'], width=3)
        
        # Top color bar
        rounded_rect(draw, (x, y, x + card_w, y + 80), 20, c['color'])
        draw.rectangle((x, y + 60, x + card_w, y + 80), fill=c['color'])
        
        # Name on color bar
        name_font = font(36)
        bbox = draw.textbbox((0, 0), c['name'], font=name_font)
        nw = bbox[2] - bbox[0]
        draw.text((x + (card_w - nw) // 2, y + 18), c['name'], font=name_font, fill='#ffffff')
        
        # Tag
        tag_font = font(32)
        bbox = draw.textbbox((0, 0), c['tag'], font=tag_font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, y + 120), c['tag'], font=tag_font, fill=c['color'])
        
        # Separator
        draw.line([(x + 40, y + 180), (x + card_w - 40, y + 180)], fill=c['color'], width=2)
        
        # Description lines
        desc_font = font(28)
        lines = c['desc'].split('\n')
        for j, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            lw = bbox[2] - bbox[0]
            draw.text((x + (card_w - lw) // 2, y + 220 + j * 55), line, font=desc_font, fill='#555555')
    
    img.save(os.path.join(output_dir, '02_products.png'))
    print("✅ 02_products.png")

# =========================================================
# Image 3: Comparison Table - 对比表图
# =========================================================
def gen_comparison():
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Title
    title_font = font(44)
    text_center_x(draw, "三大 Agent 功能对比", 50, title_font, '#222222')
    
    # Table dimensions
    col_w = 240
    row_h = 100
    label_w = 200
    table_w = label_w + col_w * 3
    start_x = (W - table_w) // 2
    start_y = 150
    
    colors = ['#22c55e', '#3b82f6', '#f97316']
    headers = ['OpenCode', 'Claude Code', 'Codex']
    rows = [
        ('模型支持', ['多模型自由', 'Claude 系列', 'GPT 系列']),
        ('费用', ['API 费用', '订阅制', 'API 费用']),
        ('核心能力', ['灵活定制', '代码质量高', '平台整合']),
        ('开源', ['✅ 完全开源', '❌ 闭源', '❌ 闭源']),
        ('生态', ['社区插件', 'Anthropic', 'OpenAI']),
        ('上手难度', ['中等', '简单', '简单']),
        ('适合', ['极客/自由', '团队/企业', 'OpenAI用户']),
    ]
    
    # Header row
    # Label column header
    rounded_rect(draw, (start_x, start_y, start_x + label_w, start_y + row_h), 0, '#e5e7eb')
    hdr_font = font(28)
    draw.text((start_x + 30, start_y + 30), "对比项", font=hdr_font, fill='#666666')
    
    for i, (hdr, clr) in enumerate(zip(headers, colors)):
        x = start_x + label_w + i * col_w
        rounded_rect(draw, (x, start_y, x + col_w, start_y + row_h), 0, clr)
        bbox = draw.textbbox((0, 0), hdr, font=hdr_font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (col_w - tw) // 2, start_y + 30), hdr, font=hdr_font, fill='#ffffff')
    
    # Data rows
    cell_font = font(24)
    for ri, (label, vals) in enumerate(rows):
        y = start_y + row_h * (ri + 1)
        bg = '#f9fafb' if ri % 2 == 0 else '#ffffff'
        
        # Label
        draw.rectangle((start_x, y, start_x + label_w, y + row_h), fill='#f3f4f6')
        draw.text((start_x + 20, y + 32), label, font=cell_font, fill='#444444')
        
        # Values
        for ci, val in enumerate(vals):
            x = start_x + label_w + ci * col_w
            draw.rectangle((x, y, x + col_w, y + row_h), fill=bg, outline='#e5e7eb', width=1)
            bbox = draw.textbbox((0, 0), val, font=cell_font)
            tw = bbox[2] - bbox[0]
            draw.text((x + (col_w - tw) // 2, y + 32), val, font=cell_font, fill='#333333')
    
    # Table border
    total_h = row_h * (len(rows) + 1)
    draw.rectangle((start_x, start_y, start_x + table_w, start_y + total_h), outline='#d1d5db', width=2)
    
    img.save(os.path.join(output_dir, '03_comparison.png'))
    print("✅ 03_comparison.png")

# =========================================================
# Image 4: Decision Flow - 3步决策法图
# =========================================================
def gen_decision():
    img = Image.new('RGB', (W, H), '#f0f4ff')
    draw = ImageDraw.Draw(img)
    
    # Title
    title_font = font(48)
    text_center_x(draw, "3步选出你的 Agent", 60, title_font, '#1e293b')
    
    subtitle_font = font(28)
    text_center_x(draw, "跟着走，不纠结", 130, subtitle_font, '#64748b')
    
    # Three steps
    steps = [
        {'num': 'Step 1', 'title': '看模型生态', 'desc': '你主用哪家模型？\nOpenAI → Codex\nAnthropic → Claude Code\n多模型 → OpenCode', 'color': '#6366f1'},
        {'num': 'Step 2', 'title': '算预算结构', 'desc': '按量付费 → OpenCode/Codex\n订阅制 → Claude Code\n零预算 → OpenCode', 'color': '#8b5cf6'},
        {'num': 'Step 3', 'title': '评锁定接受度', 'desc': '不想被锁定 → OpenCode\n接受生态锁定 → Claude Code\n已在OpenAI → Codex', 'color': '#a855f7'},
    ]
    
    card_w = 800
    card_h = 200
    start_x = (W - card_w) // 2
    start_y = 210
    gap = 50
    
    for i, s in enumerate(steps):
        y = start_y + i * (card_h + gap)
        
        # Card
        rounded_rect(draw, (start_x, y, start_x + card_w, y + card_h), 16, '#ffffff', outline=s['color'], width=3)
        
        # Step number circle
        cx, cy = start_x + 70, y + card_h // 2
        draw.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=s['color'])
        num_font = font(24)
        bbox = draw.textbbox((0, 0), s['num'], font=num_font)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((cx - nw // 2, cy - nh // 2 - 4), s['num'], font=num_font, fill='#ffffff')
        
        # Title
        t_font = font(36)
        draw.text((start_x + 140, y + 20), s['title'], font=t_font, fill=s['color'])
        
        # Description
        d_font = font(22)
        lines = s['desc'].split('\n')
        for j, line in enumerate(lines):
            draw.text((start_x + 140, y + 75 + j * 30), line, font=d_font, fill='#555555')
        
        # Arrow between cards
        if i < 2:
            arrow_y = y + card_h + 10
            ax = W // 2
            draw.polygon([(ax - 15, arrow_y + 5), (ax + 15, arrow_y + 5), (ax, arrow_y + 30)], fill=s['color'])
    
    img.save(os.path.join(output_dir, '04_decision.png'))
    print("✅ 04_decision.png")

# =========================================================
# Image 5: Audience Recommendations - 人群推荐图
# =========================================================
def gen_audience():
    img = Image.new('RGB', (W, H), '#fafafe')
    draw = ImageDraw.Draw(img)
    
    # Title
    title_font = font(48)
    text_center_x(draw, "你是哪类开发者？", 60, title_font, '#1e293b')
    
    # Four recommendation cards in 2x2 grid
    recs = [
        {'audience': '🧑‍💻 独立开发者', 'rec': 'OpenCode', 'reason': '灵活 · 开源 · 省钱', 'color': '#22c55e', 'bg': '#f0fdf4'},
        {'audience': '👥 团队协作', 'rec': 'Claude Code', 'reason': '稳定 · 质量 · 规范', 'color': '#3b82f6', 'bg': '#eff6ff'},
        {'audience': '🤖 OpenAI 用户', 'rec': 'Codex', 'reason': '无缝 · 整合 · 熟悉', 'color': '#f97316', 'bg': '#fff7ed'},
        {'audience': '🌱 编程新手', 'rec': 'OpenCode', 'reason': '社区 · 教程 · 免费', 'color': '#22c55e', 'bg': '#f0fdf4'},
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
        
        # Audience label
        aud_font = font(32)
        bbox = draw.textbbox((0, 0), r['audience'], font=aud_font)
        aw = bbox[2] - bbox[0]
        draw.text((x + (card_w - aw) // 2, y + 40), r['audience'], font=aud_font, fill='#333333')
        
        # Arrow
        arrow_font = font(28)
        text_center_x(draw, "↓", y + 100, arrow_font, '#999999', img_w=x * 2 + card_w)
        bbox = draw.textbbox((0, 0), "↓", font=arrow_font)
        aw2 = bbox[2] - bbox[0]
        draw.text((x + (card_w - aw2) // 2, y + 100), "↓", font=arrow_font, fill='#999999')
        
        # Recommendation
        rec_font = font(42)
        bbox = draw.textbbox((0, 0), r['rec'], font=rec_font)
        rw = bbox[2] - bbox[0]
        draw.text((x + (card_w - rw) // 2, y + 150), r['rec'], font=rec_font, fill=r['color'])
        
        # Reason
        reason_font = font(24)
        bbox = draw.textbbox((0, 0), r['reason'], font=reason_font)
        rew = bbox[2] - bbox[0]
        draw.text((x + (card_w - rew) // 2, y + 230), r['reason'], font=reason_font, fill='#777777')
    
    img.save(os.path.join(output_dir, '05_audience.png'))
    print("✅ 05_audience.png")

# =========================================================
# Image 6: Conclusion Quote - 结论金句图
# =========================================================
def gen_conclusion():
    img = Image.new('RGB', (W, H), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Decorative elements
    for i in range(0, W, 80):
        draw.line([(i, 0), (i, H)], fill='#1a2744', width=1)
    for i in range(0, H, 80):
        draw.line([(0, i), (W, i)], fill='#1a2744', width=1)
    
    # Decorative quote marks
    quote_font = font(120)
    draw.text((120, 250), """, font=quote_font, fill='#3a7bfd')
    draw.text((850, 600), """, font=quote_font, fill='#3a7bfd')
    
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
    text_center_x(draw, "OpenCode · Claude Code · Codex  |  选型指南", 920, brand_font, '#475569')
    
    # Corner accents
    draw.line([(40, 40), (120, 40)], fill='#3a7bfd', width=3)
    draw.line([(40, 40), (40, 120)], fill='#3a7bfd', width=3)
    draw.line([(W-120, H-40), (W-40, H-40)], fill='#3a7bfd', width=3)
    draw.line([(W-40, H-120), (W-40, H-40)], fill='#3a7bfd', width=3)
    
    img.save(os.path.join(output_dir, '06_conclusion.png'))
    print("✅ 06_conclusion.png")

# Generate all
gen_cover()
gen_products()
gen_comparison()
gen_decision()
gen_audience()
gen_conclusion()
print("\n🎉 All 6 images generated!")
print(f"Output directory: {output_dir}")
