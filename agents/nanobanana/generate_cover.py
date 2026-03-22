#!/usr/bin/env python3
"""Generate a 1024x1024 cover image: 3 AI coding tool robot assistants comparison."""

from PIL import Image, ImageDraw
import math, random

W, H = 1024, 1024
img = Image.new("RGBA", (W, H))
draw = ImageDraw.Draw(img)

# --- Gradient background (soft blue-purple) ---
for y in range(H):
    r = int(30 + (60 - 30) * y / H)
    g = int(35 + (30 - 35) * y / H)
    b = int(120 + (180 - 120) * y / H)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# --- Subtle grid/dots pattern ---
for gx in range(0, W, 40):
    for gy in range(0, H, 40):
        opacity = random.randint(15, 35)
        draw.ellipse([gx-1, gy-1, gx+1, gy+1], fill=(200, 210, 255, opacity))

# --- Soft glow circles in background ---
def draw_glow(cx, cy, radius, color, steps=20):
    for i in range(steps, 0, -1):
        alpha = int(color[3] * (i / steps) * 0.3)
        r = int(radius * (i / steps))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(color[0], color[1], color[2], alpha))

draw_glow(200, 200, 200, (100, 150, 255, 60))
draw_glow(800, 300, 180, (180, 100, 255, 50))
draw_glow(500, 800, 220, (100, 200, 255, 40))

# --- Robot drawing helpers ---
def rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    r = min(radius, (x2-x1)//2, (y2-y1)//2)
    # Fill main body
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    # Four corners
    draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
    draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)
    if outline and width > 0:
        # outline arcs
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)


def draw_robot(cx, cy, style, accent, eye_color, antenna_style):
    """Draw a stylized robot at center (cx, cy).
    style: 'round', 'square', 'hexagonal'
    """
    # Shadow/glow under robot
    draw_glow(cx, cy + 180, 120, (accent[0], accent[1], accent[2], 80))
    
    # --- Platform/base ---
    base_color = (accent[0]//3 + 40, accent[1]//3 + 40, accent[2]//3 + 60, 200)
    rounded_rect(draw, [cx-80, cy+140, cx+80, cy+170], 15, fill=base_color)
    
    # --- Body ---
    body_w, body_h = 130, 150
    if style == 'round':
        body_color = (60, 70, 110, 240)
        body_highlight = (80, 90, 140, 240)
        # Rounded body
        rounded_rect(draw, [cx-body_w//2, cy-20, cx+body_w//2, cy+140], 35, fill=body_color)
        # Chest panel
        panel_color = (accent[0]//2+30, accent[1]//2+30, accent[2]//2+50, 180)
        rounded_rect(draw, [cx-40, cy+20, cx+40, cy+90], 12, fill=panel_color)
        # Chest light bars
        for i in range(3):
            bar_alpha = 200 - i * 40
            bar_color = (accent[0], accent[1], accent[2], bar_alpha)
            rounded_rect(draw, [cx-30, cy+30+i*20, cx+30, cy+40+i*20], 4, fill=bar_color)
    elif style == 'square':
        body_color = (55, 65, 105, 240)
        # More angular body
        rounded_rect(draw, [cx-body_w//2, cy-20, cx+body_w//2, cy+140], 12, fill=body_color)
        # Chest screen
        screen_color = (20, 30, 50, 220)
        rounded_rect(draw, [cx-45, cy+15, cx+45, cy+95], 8, fill=screen_color)
        # Code lines on screen
        for i in range(4):
            line_w = random.randint(30, 70)
            line_x = cx - 35
            line_y = cy + 25 + i * 16
            code_color = (accent[0], accent[1], accent[2], 180)
            draw.line([(line_x, line_y), (line_x + line_w, line_y)], fill=code_color, width=3)
    else:  # hexagonal style
        body_color = (65, 75, 115, 240)
        # Hex-ish body (octagon approximation)
        inset = 25
        pts = [
            (cx - body_w//2 + inset, cy - 20),
            (cx + body_w//2 - inset, cy - 20),
            (cx + body_w//2, cy - 20 + inset),
            (cx + body_w//2, cy + 140 - inset),
            (cx + body_w//2 - inset, cy + 140),
            (cx - body_w//2 + inset, cy + 140),
            (cx - body_w//2, cy + 140 - inset),
            (cx - body_w//2, cy - 20 + inset),
        ]
        draw.polygon(pts, fill=body_color)
        # Central energy core
        draw_glow(cx, cy + 60, 35, (accent[0], accent[1], accent[2], 150), steps=15)
        draw.ellipse([cx-12, cy+48, cx+12, cy+72], fill=(accent[0], accent[1], accent[2], 220))
    
    # --- Head ---
    head_w, head_h = 110, 90
    head_color = (70, 80, 130, 245)
    if style == 'round':
        # Round head
        draw.ellipse([cx-head_w//2, cy-110, cx+head_w//2, cy-20], fill=head_color)
        # Visor
        visor_color = (30, 35, 60, 230)
        draw.ellipse([cx-40, cy-90, cx+40, cy-45], fill=visor_color)
        # Eyes (two circles)
        draw.ellipse([cx-25, cy-78, cx-10, cy-58], fill=eye_color)
        draw.ellipse([cx+10, cy-78, cx+25, cy-58], fill=eye_color)
        # Eye highlights
        draw.ellipse([cx-22, cy-75, cx-16, cy-68], fill=(255, 255, 255, 180))
        draw.ellipse([cx+13, cy-75, cx+19, cy-68], fill=(255, 255, 255, 180))
    elif style == 'square':
        # Square head with slight rounding
        rounded_rect(draw, [cx-head_w//2, cy-115, cx+head_w//2, cy-25], 15, fill=head_color)
        # Visor bar
        visor_color = (25, 30, 55, 230)
        rounded_rect(draw, [cx-42, cy-95, cx+42, cy-55], 10, fill=visor_color)
        # Rectangular eyes
        draw.rectangle([cx-30, cy-85, cx-12, cy-65], fill=eye_color)
        draw.rectangle([cx+12, cy-85, cx+30, cy-65], fill=eye_color)
        # Eye highlights
        draw.rectangle([cx-28, cy-83, cx-20, cy-75], fill=(255, 255, 255, 150))
        draw.rectangle([cx+14, cy-83, cx+22, cy-75], fill=(255, 255, 255, 150))
    else:
        # Diamond/hex head
        head_pts = [
            (cx, cy - 120),
            (cx + head_w//2, cy - 70),
            (cx + head_w//2 - 10, cy - 25),
            (cx - head_w//2 + 10, cy - 25),
            (cx - head_w//2, cy - 70),
        ]
        draw.polygon(head_pts, fill=head_color)
        # Single visor
        visor_pts = [
            (cx, cy - 100),
            (cx + 35, cy - 70),
            (cx + 25, cy - 45),
            (cx - 25, cy - 45),
            (cx - 35, cy - 70),
        ]
        draw.polygon(visor_pts, fill=(25, 30, 55, 230))
        # Triangular eye
        draw.ellipse([cx-15, cy-80, cx+15, cy-55], fill=eye_color)
        draw.ellipse([cx-8, cy-75, cx+2, cy-62], fill=(255, 255, 255, 150))
    
    # --- Antenna ---
    if antenna_style == 'single':
        draw.line([(cx, cy-110), (cx, cy-145)], fill=(180, 190, 220, 200), width=3)
        draw.ellipse([cx-6, cy-152, cx+6, cy-140], fill=accent + (230,))
    elif antenna_style == 'double':
        draw.line([(cx-15, cy-110), (cx-20, cy-140)], fill=(180, 190, 220, 200), width=3)
        draw.line([(cx+15, cy-110), (cx+20, cy-140)], fill=(180, 190, 220, 200), width=3)
        draw.ellipse([cx-26, cy-148, cx-14, cy-136], fill=accent + (230,))
        draw.ellipse([cx+14, cy-148, cx+26, cy-136], fill=accent + (230,))
    else:  # crown
        for dx in [-20, 0, 20]:
            h = 135 if dx == 0 else 145
            draw.line([(cx+dx, cy-115), (cx+dx, cy-h)], fill=(180, 190, 220, 200), width=2)
            draw.ellipse([cx+dx-4, cy-h-8, cx+dx+4, cy-h], fill=accent + (230,))
    
    # --- Arms ---
    arm_color = (55, 65, 105, 220)
    # Left arm
    draw.line([(cx-body_w//2, cy+20), (cx-body_w//2-30, cy+80)], fill=arm_color, width=10)
    draw.ellipse([cx-body_w//2-42, cy+72, cx-body_w//2-18, cy+96], fill=(80, 90, 140, 220))
    # Right arm
    draw.line([(cx+body_w//2, cy+20), (cx+body_w//2+30, cy+80)], fill=arm_color, width=10)
    draw.ellipse([cx+body_w//2+18, cy+72, cx+body_w//2+42, cy+96], fill=(80, 90, 140, 220))
    
    # --- Legs ---
    leg_color = (50, 60, 100, 220)
    # Left leg
    draw.line([(cx-30, cy+140), (cx-35, cy+180)], fill=leg_color, width=8)
    rounded_rect(draw, [cx-50, cy+175, cx-20, cy+195], 5, fill=(70, 80, 120, 230))
    # Right leg
    draw.line([(cx+30, cy+140), (cx+35, cy+180)], fill=leg_color, width=8)
    rounded_rect(draw, [cx+20, cy+175, cx+50, cy+195], 5, fill=(70, 80, 120, 230))


# --- Draw three robots ---
# Robot 1 (left) - Round style, green accent - "Friendly"
draw_robot(
    cx=200, cy=450,
    style='round',
    accent=(80, 220, 160),
    eye_color=(80, 255, 180, 255),
    antenna_style='single'
)

# Robot 2 (center) - Square style, blue accent - "Analytical"  
draw_robot(
    cx=512, cy=420,
    style='square',
    accent=(80, 160, 255),
    eye_color=(100, 180, 255, 255),
    antenna_style='double'
)

# Robot 3 (right) - Hex style, purple accent - "Creative"
draw_robot(
    cx=824, cy=450,
    style='hexagonal',
    accent=(180, 100, 255),
    eye_color=(200, 130, 255, 255),
    antenna_style='crown'
)

# --- Decorative floating particles/icons ---
random.seed(42)
for _ in range(40):
    px = random.randint(20, W-20)
    py = random.randint(20, H-20)
    ps = random.randint(2, 5)
    pa = random.randint(40, 100)
    pc = random.choice([
        (100, 200, 255, pa),
        (180, 130, 255, pa),
        (100, 255, 180, pa),
        (255, 255, 255, pa),
    ])
    draw.ellipse([px-ps, py-ps, px+ps, py+ps], fill=pc)

# --- Floating code bracket decorations ---
bracket_color = (180, 200, 255, 60)
# < > symbols as simple lines
for bx, by, scale in [(100, 700, 1.0), (920, 680, 0.8), (500, 200, 0.6), (150, 280, 0.7), (850, 150, 0.9)]:
    s = int(20 * scale)
    w = max(2, int(3 * scale))
    # < bracket
    draw.line([(bx, by), (bx-s, by+s)], fill=bracket_color, width=w)
    draw.line([(bx-s, by+s), (bx, by+2*s)], fill=bracket_color, width=w)
    # > bracket
    draw.line([(bx+s*2, by), (bx+s*3, by+s)], fill=bracket_color, width=w)
    draw.line([(bx+s*3, by+s), (bx+s*2, by+2*s)], fill=bracket_color, width=w)

# --- Connection lines between robots (subtle) ---
line_color = (150, 170, 220, 40)
for i in range(5):
    y_off = 380 + i * 30
    draw.line([(260, y_off), (450, y_off - 10)], fill=line_color, width=1)
    draw.line([(574, y_off - 10), (764, y_off)], fill=line_color, width=1)

# --- Subtle vignette ---
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vdraw = ImageDraw.Draw(vignette)
for i in range(80):
    alpha = int(60 * (1 - i/80))
    margin = i * 3
    vdraw.rectangle([margin, margin, W-margin, H-margin], outline=(0, 0, 10, alpha))
img = Image.alpha_composite(img, vignette)

# --- Save ---
output_path = "/Users/lucifinil_chen/.openclaw/workspace/agents/nano-banana/ai_tools_cover.png"
img = img.convert("RGB")
img.save(output_path, "PNG", quality=95)
print(f"Image saved to: {output_path}")
print(f"Size: {img.size}")
