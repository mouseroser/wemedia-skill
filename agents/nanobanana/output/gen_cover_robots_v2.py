#!/usr/bin/env python3
"""Generate a clean 1024x1024 cover image with 3 stylized robot assistants."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

W, H = 1024, 1024
output_dir = os.path.expanduser('~/.openclaw/workspace/agents/nano-banana/output')
os.makedirs(output_dir, exist_ok=True)

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_gradient_bg(img):
    draw = ImageDraw.Draw(img)
    c_top_left = (210, 220, 255)
    c_top_right = (220, 210, 250)
    c_bot_left = (195, 210, 255)
    c_bot_right = (235, 210, 255)
    for y in range(H):
        ty = y / H
        c_left = lerp_color(c_top_left, c_bot_left, ty)
        c_right = lerp_color(c_top_right, c_bot_right, ty)
        for x in range(W):
            tx = x / W
            c = lerp_color(c_left, c_right, tx)
            draw.point((x, y), fill=c)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=outline_width)

def draw_circle(draw, cx, cy, r, fill, outline=None, width=2):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)

def draw_soft_glow(overlay_draw, cx, cy, radius, color, max_alpha=40):
    """Draw soft glow using filled circles on RGBA overlay."""
    for r in range(radius, 0, -2):
        t = 1.0 - (r / radius)
        alpha = int(max_alpha * t * t)
        fill = color + (alpha,)
        overlay_draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)

def draw_robot_rounded(draw, cx, cy, accent, body):
    """Friendly rounded robot (green)."""
    # Shadow
    draw.ellipse((cx-70, cy+135, cx+70, cy+155), fill=accent + (30,))
    # Legs
    draw_rounded_rect(draw, (cx-40, cy+95, cx-15, cy+135), 8, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+15, cy+95, cx+40, cy+135), 8, body, outline=accent, outline_width=3)
    # Feet
    draw_rounded_rect(draw, (cx-48, cy+125, cx-10, cy+145), 10, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+10, cy+125, cx+48, cy+145), 10, body, outline=accent, outline_width=3)
    # Arms
    draw_rounded_rect(draw, (cx-95, cy-15, cx-65, cy+55), 12, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+65, cy-15, cx+95, cy+55), 12, body, outline=accent, outline_width=3)
    # Body
    draw_rounded_rect(draw, (cx-65, cy-30, cx+65, cy+100), 22, body, outline=accent, outline_width=3)
    # Head
    draw_rounded_rect(draw, (cx-55, cy-115, cx+55, cy-20), 24, body, outline=accent, outline_width=3)
    # Antenna
    draw.line([(cx, cy-115), (cx, cy-148)], fill=accent, width=3)
    draw_circle(draw, cx, cy-153, 9, accent)
    # Eyes
    draw_circle(draw, cx-22, cy-75, 15, (255,255,255))
    draw_circle(draw, cx+22, cy-75, 15, (255,255,255))
    draw_circle(draw, cx-22, cy-75, 9, accent)
    draw_circle(draw, cx+22, cy-75, 9, accent)
    draw_circle(draw, cx-20, cy-77, 4, (30,30,50))
    draw_circle(draw, cx+24, cy-77, 4, (30,30,50))
    # Eye shines
    draw_circle(draw, cx-25, cy-79, 3, (255,255,255))
    draw_circle(draw, cx+19, cy-79, 3, (255,255,255))
    # Smile
    draw.arc((cx-22, cy-60, cx+22, cy-38), 10, 170, fill=accent, width=3)
    # Chest: code symbol </>
    draw.line([(cx-22, cy+18), (cx-32, cy+35), (cx-22, cy+52)], fill=accent, width=3)
    draw.line([(cx+22, cy+18), (cx+32, cy+35), (cx+22, cy+52)], fill=accent, width=3)
    draw.line([(cx+6, cy+14), (cx-6, cy+56)], fill=accent, width=3)

def draw_robot_angular(draw, cx, cy, accent, body):
    """Professional angular robot (blue)."""
    # Shadow
    draw.ellipse((cx-70, cy+140, cx+70, cy+160), fill=accent + (30,))
    # Legs
    draw_rounded_rect(draw, (cx-40, cy+100, cx-14, cy+148), 6, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+14, cy+100, cx+40, cy+148), 6, body, outline=accent, outline_width=3)
    # Arms - segmented
    draw_rounded_rect(draw, (cx-92, cy-18, cx-62, cy+12), 6, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx-92, cy+16, cx-62, cy+58), 6, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+62, cy-18, cx+92, cy+12), 6, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+62, cy+16, cx+92, cy+58), 6, body, outline=accent, outline_width=3)
    # Body
    draw_rounded_rect(draw, (cx-62, cy-32, cx+62, cy+105), 10, body, outline=accent, outline_width=3)
    # Head
    draw_rounded_rect(draw, (cx-52, cy-120, cx+52, cy-22), 10, body, outline=accent, outline_width=3)
    # Two antennas
    draw.line([(cx-22, cy-120), (cx-32, cy-152)], fill=accent, width=3)
    draw.line([(cx+22, cy-120), (cx+32, cy-152)], fill=accent, width=3)
    draw_circle(draw, cx-32, cy-155, 6, accent)
    draw_circle(draw, cx+32, cy-155, 6, accent)
    # Eyes - rectangular visor style
    draw_rounded_rect(draw, (cx-38, cy-92, cx-6, cy-62), 5, (255,255,255))
    draw_rounded_rect(draw, (cx+6, cy-92, cx+38, cy-62), 5, (255,255,255))
    draw_rounded_rect(draw, (cx-32, cy-86, cx-12, cy-68), 3, accent)
    draw_rounded_rect(draw, (cx+12, cy-86, cx+32, cy-68), 3, accent)
    # Visor line
    draw.line([(cx-42, cy-56), (cx+42, cy-56)], fill=accent, width=2)
    # Serious mouth
    draw.line([(cx-16, cy-45), (cx+16, cy-45)], fill=accent, width=3)
    # Chest: shield/panel
    draw_rounded_rect(draw, (cx-22, cy+8, cx+22, cy+60), 6, accent + (40,), outline=accent, outline_width=2)
    draw.line([(cx, cy+8), (cx, cy+60)], fill=accent, width=2)
    draw.line([(cx-22, cy+34), (cx+22, cy+34)], fill=accent, width=2)
    # Small status lights
    draw_circle(draw, cx-12, cy+20, 3, (200, 230, 255))
    draw_circle(draw, cx+12, cy+20, 3, (200, 230, 255))

def draw_robot_circular(draw, cx, cy, accent, body):
    """Playful circular robot (orange)."""
    # Shadow
    draw.ellipse((cx-65, cy+130, cx+65, cy+150), fill=accent + (30,))
    # Legs - short and stubby
    draw_rounded_rect(draw, (cx-28, cy+95, cx-10, cy+128), 8, body, outline=accent, outline_width=3)
    draw_rounded_rect(draw, (cx+10, cy+95, cx+28, cy+128), 8, body, outline=accent, outline_width=3)
    # Feet - round
    draw.ellipse((cx-36, cy+118, cx-4, cy+142), fill=body, outline=accent, width=3)
    draw.ellipse((cx+4, cy+118, cx+36, cy+142), fill=body, outline=accent, width=3)
    # Body - egg/oval
    draw.ellipse((cx-55, cy-22, cx+55, cy+100), fill=body, outline=accent, width=3)
    # Head - circle
    draw_circle(draw, cx, cy-68, 52, body, outline=accent, width=3)
    # Antenna - curly
    draw.line([(cx, cy-120), (cx-8, cy-135), (cx+8, cy-150), (cx, cy-162)], fill=accent, width=3)
    draw_circle(draw, cx, cy-166, 7, accent)
    # Big expressive eyes
    draw_circle(draw, cx-20, cy-75, 17, (255,255,255))
    draw_circle(draw, cx+20, cy-75, 17, (255,255,255))
    draw_circle(draw, cx-18, cy-73, 11, accent)
    draw_circle(draw, cx+22, cy-73, 11, accent)
    draw_circle(draw, cx-18, cy-73, 6, (50,30,10))
    draw_circle(draw, cx+22, cy-73, 6, (50,30,10))
    # Eye shines (bigger for cute look)
    draw_circle(draw, cx-22, cy-78, 5, (255,255,255))
    draw_circle(draw, cx+18, cy-78, 5, (255,255,255))
    draw_circle(draw, cx-16, cy-70, 3, (255,255,255))
    draw_circle(draw, cx+24, cy-70, 3, (255,255,255))
    # Happy open mouth
    draw.arc((cx-18, cy-55, cx+18, cy-35), 0, 180, fill=accent, width=3)
    # Blush circles
    draw_circle(draw, cx-35, cy-55, 8, accent + (40,))
    draw_circle(draw, cx+35, cy-55, 8, accent + (40,))
    # Arms - one waving
    draw.line([(cx-55, cy+5), (cx-78, cy-20), (cx-92, cy-40)], fill=accent, width=4)
    draw_circle(draw, cx-95, cy-43, 9, body, outline=accent, width=3)
    draw.line([(cx+55, cy+10), (cx+78, cy+0), (cx+92, cy+10)], fill=accent, width=4)
    draw_circle(draw, cx+95, cy+8, 9, body, outline=accent, width=3)
    # Chest: gear/sun icon
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = cx + int(14 * math.cos(rad))
        y1 = cy + 38 + int(14 * math.sin(rad))
        x2 = cx + int(20 * math.cos(rad))
        y2 = cy + 38 + int(20 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=accent, width=2)
    draw_circle(draw, cx, cy+38, 11, accent)
    draw_circle(draw, cx, cy+38, 6, body)

def draw_sparkle(draw, cx, cy, size, color):
    """Draw a 4-pointed sparkle."""
    draw.line([(cx, cy-size), (cx, cy+size)], fill=color, width=2)
    draw.line([(cx-size, cy), (cx+size, cy)], fill=color, width=2)
    s = int(size * 0.5)
    draw.line([(cx-s, cy-s), (cx+s, cy+s)], fill=color, width=1)
    draw.line([(cx+s, cy-s), (cx-s, cy+s)], fill=color, width=1)

def main():
    # Create base RGB image with gradient
    img = Image.new('RGB', (W, H))
    draw_gradient_bg(img)
    
    # Convert to RGBA for glow overlays
    img = img.convert('RGBA')
    
    # Create glow overlay
    glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    draw_soft_glow(glow_draw, 160, 280, 140, (130, 180, 255), max_alpha=25)
    draw_soft_glow(glow_draw, 860, 230, 120, (190, 140, 255), max_alpha=20)
    draw_soft_glow(glow_draw, 512, 820, 160, (150, 160, 255), max_alpha=18)
    # Apply blur to glow for smoothness
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=20))
    img = Image.alpha_composite(img, glow_layer)
    
    # Main drawing layer
    main_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(main_layer)
    
    # Subtle dots grid instead of lines (cleaner)
    for x in range(32, W, 64):
        for y in range(32, H, 64):
            draw_circle(draw, x, y, 1, (170, 180, 220, 50))
    
    # Small floating code elements (very subtle)
    try:
        code_font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 14)
    except:
        code_font = ImageFont.load_default()
    
    code_elements = [
        (75, 130, '{  }'), (920, 160, '< />'), (100, 870, '0 1'),
        (900, 830, '{ }'), (490, 100, '//'), (50, 530, '[ ]'),
        (960, 480, '( )'), (500, 920, '=> '),
    ]
    for x, y, text in code_elements:
        draw.text((x, y), text, font=code_font, fill=(160, 170, 215, 80))
    
    # Platform shadows under each robot
    robot_y = 500
    for rx in [205, 512, 819]:
        draw.ellipse((rx-75, robot_y+142, rx+75, robot_y+165), fill=(100, 110, 180, 25))
        draw.ellipse((rx-55, robot_y+147, rx+55, robot_y+160), fill=(100, 110, 180, 20))
    
    # Connection dots between robots
    conn_y = robot_y - 5
    for x in range(310, 415, 12):
        draw_circle(draw, x, conn_y, 2, (150, 165, 215, 60))
    for x in range(610, 715, 12):
        draw_circle(draw, x, conn_y, 2, (150, 165, 215, 60))
    
    # Draw the three robots
    green = (34, 197, 94)
    green_body = (232, 248, 236)
    blue = (59, 130, 246)
    blue_body = (232, 240, 255)
    orange = (249, 115, 22)
    orange_body = (255, 240, 220)
    
    draw_robot_rounded(draw, 205, robot_y, green, green_body)
    draw_robot_angular(draw, 512, robot_y, blue, blue_body)
    draw_robot_circular(draw, 819, robot_y, orange, orange_body)
    
    # Sparkles / decorative elements around robots
    draw_sparkle(draw, 120, 350, 8, green + (120,))
    draw_sparkle(draw, 290, 320, 6, green + (100,))
    draw_sparkle(draw, 85, 600, 5, green + (80,))
    
    draw_sparkle(draw, 420, 380, 7, blue + (100,))
    draw_sparkle(draw, 610, 360, 6, blue + (90,))
    draw_sparkle(draw, 512, 700, 5, blue + (70,))
    
    draw_sparkle(draw, 740, 370, 8, orange + (120,))
    draw_sparkle(draw, 920, 400, 6, orange + (100,))
    draw_sparkle(draw, 880, 680, 5, orange + (80,))
    draw_sparkle(draw, 760, 660, 4, orange + (70,))
    
    # Small floating circles
    draw_circle(draw, 340, 200, 4, green + (60,))
    draw_circle(draw, 680, 190, 4, blue + (60,))
    draw_circle(draw, 950, 300, 5, orange + (60,))
    draw_circle(draw, 170, 750, 3, green + (50,))
    draw_circle(draw, 850, 780, 3, orange + (50,))
    
    # Composite main layer
    img = Image.alpha_composite(img, main_layer)
    
    # Convert back to RGB for saving
    final = img.convert('RGB')
    
    output_path = os.path.join(output_dir, 'cover_robots_1024.png')
    final.save(output_path, 'PNG')
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {final.size}")

if __name__ == '__main__':
    main()
