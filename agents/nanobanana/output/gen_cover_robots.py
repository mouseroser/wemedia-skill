#!/usr/bin/env python3
"""Generate a 1024x1024 cover image with 3 stylized robot assistants for AI coding tools comparison."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

W, H = 1024, 1024
output_dir = os.path.expanduser('~/.openclaw/workspace/agents/nano-banana/output')
os.makedirs(output_dir, exist_ok=True)

def lerp_color(c1, c2, t):
    """Linear interpolation between two RGB colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_gradient_bg(img):
    """Draw soft blue-purple gradient background."""
    draw = ImageDraw.Draw(img)
    # Top-left: soft blue, bottom-right: soft purple
    c_top_left = (200, 215, 255)     # Light blue
    c_top_right = (210, 200, 250)    # Light lavender
    c_bot_left = (190, 200, 245)     # Mid blue
    c_bot_right = (225, 195, 250)    # Light purple
    
    for y in range(H):
        ty = y / H
        c_left = lerp_color(c_top_left, c_bot_left, ty)
        c_right = lerp_color(c_top_right, c_bot_right, ty)
        for x in range(W):
            tx = x / W
            c = lerp_color(c_left, c_right, tx)
            draw.point((x, y), fill=c)

def draw_subtle_grid(draw):
    """Draw very subtle grid pattern for tech feel."""
    grid_color = (180, 190, 230, 30)
    for x in range(0, W, 64):
        draw.line([(x, 0), (x, H)], fill=(180, 190, 230), width=1)
    for y in range(0, H, 64):
        draw.line([(0, y), (W, y)], fill=(180, 190, 230), width=1)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    """Draw rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=outline_width)

def draw_circle(draw, cx, cy, r, fill, outline=None, width=2):
    """Draw circle."""
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)


def draw_robot(draw, cx, cy, style, accent_color, body_color, eye_color, antenna_style='round'):
    """
    Draw a stylized robot at center (cx, cy).
    style: 'rounded', 'angular', 'circular' - determines robot personality
    """
    
    if style == 'rounded':
        # Friendly, rounded robot (OpenCode style - green)
        # Body
        draw_rounded_rect(draw, (cx-65, cy-30, cx+65, cy+100), 25, body_color, outline=accent_color, outline_width=3)
        # Head
        draw_rounded_rect(draw, (cx-55, cy-110, cx+55, cy-20), 22, body_color, outline=accent_color, outline_width=3)
        # Eyes - friendly round eyes
        draw_circle(draw, cx-22, cy-72, 14, '#ffffff')
        draw_circle(draw, cx+22, cy-72, 14, '#ffffff')
        draw_circle(draw, cx-22, cy-72, 8, eye_color)
        draw_circle(draw, cx+22, cy-72, 8, eye_color)
        # Pupils
        draw_circle(draw, cx-20, cy-74, 4, '#1a1a2e')
        draw_circle(draw, cx+24, cy-74, 4, '#1a1a2e')
        # Smile
        draw.arc((cx-25, cy-60, cx+25, cy-35), 10, 170, fill=accent_color, width=3)
        # Antenna - single round
        draw.line([(cx, cy-110), (cx, cy-140)], fill=accent_color, width=3)
        draw_circle(draw, cx, cy-145, 8, accent_color)
        # Arms - rounded stubs
        draw_rounded_rect(draw, (cx-90, cy-10, cx-65, cy+50), 10, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+65, cy-10, cx+90, cy+50), 10, body_color, outline=accent_color, outline_width=3)
        # Legs
        draw_rounded_rect(draw, (cx-40, cy+100, cx-15, cy+140), 8, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+15, cy+100, cx+40, cy+140), 8, body_color, outline=accent_color, outline_width=3)
        # Chest detail - code icon (< />)
        detail_color = accent_color
        draw.line([(cx-20, cy+20), (cx-30, cy+35), (cx-20, cy+50)], fill=detail_color, width=2)
        draw.line([(cx+20, cy+20), (cx+30, cy+35), (cx+20, cy+50)], fill=detail_color, width=2)
        draw.line([(cx+5, cy+15), (cx-5, cy+55)], fill=detail_color, width=2)
        
        # Floating particles around this robot
        draw_circle(draw, cx-80, cy-120, 3, accent_color)
        draw_circle(draw, cx+85, cy-100, 4, accent_color)
        draw_circle(draw, cx-70, cy+90, 3, accent_color)

    elif style == 'angular':
        # Professional, angular robot (Claude Code style - blue)
        # Body - more rectangular
        draw_rounded_rect(draw, (cx-60, cy-30, cx+60, cy+100), 10, body_color, outline=accent_color, outline_width=3)
        # Head - more square
        draw_rounded_rect(draw, (cx-50, cy-115, cx+50, cy-20), 10, body_color, outline=accent_color, outline_width=3)
        # Eyes - rectangular scanner-style
        draw_rounded_rect(draw, (cx-35, cy-85, cx-8, cy-60), 4, '#ffffff')
        draw_rounded_rect(draw, (cx+8, cy-85, cx+35, cy-60), 4, '#ffffff')
        draw_rounded_rect(draw, (cx-30, cy-80, cx-12, cy-65), 3, eye_color)
        draw_rounded_rect(draw, (cx+12, cy-80, cx+30, cy-65), 3, eye_color)
        # Visor line
        draw.line([(cx-40, cy-55), (cx+40, cy-55)], fill=accent_color, width=2)
        # Mouth - straight line (serious)
        draw.line([(cx-15, cy-45), (cx+15, cy-45)], fill=accent_color, width=3)
        # Antenna - two pointed
        draw.line([(cx-20, cy-115), (cx-30, cy-145)], fill=accent_color, width=3)
        draw.line([(cx+20, cy-115), (cx+30, cy-145)], fill=accent_color, width=3)
        draw_circle(draw, cx-30, cy-148, 5, accent_color)
        draw_circle(draw, cx+30, cy-148, 5, accent_color)
        # Arms - articulated
        draw_rounded_rect(draw, (cx-88, cy-15, cx-60, cy+10), 6, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx-88, cy+15, cx-60, cy+55), 6, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+60, cy-15, cx+88, cy+10), 6, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+60, cy+15, cx+88, cy+55), 6, body_color, outline=accent_color, outline_width=3)
        # Legs - sturdy
        draw_rounded_rect(draw, (cx-38, cy+100, cx-12, cy+145), 6, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+12, cy+100, cx+38, cy+145), 6, body_color, outline=accent_color, outline_width=3)
        # Chest detail - shield icon
        draw_rounded_rect(draw, (cx-18, cy+10, cx+18, cy+55), 8, accent_color + '33')
        draw.line([(cx, cy+10), (cx, cy+55)], fill=accent_color, width=2)
        draw.line([(cx-18, cy+32), (cx+18, cy+32)], fill=accent_color, width=2)
        
        # Floating geometric shapes
        draw_rounded_rect(draw, (cx-90, cy-130, cx-78, cy-118), 2, accent_color)
        draw_rounded_rect(draw, (cx+80, cy-110, cx+92, cy-98), 2, accent_color)

    elif style == 'circular':
        # Playful, rounded robot (Codex style - orange)
        # Body - oval/egg shape
        draw.ellipse((cx-55, cy-25, cx+55, cy+105), fill=body_color, outline=accent_color, width=3)
        # Head - circle
        draw_circle(draw, cx, cy-65, 50, body_color, outline=accent_color, width=3)
        # Eyes - big expressive eyes
        draw_circle(draw, cx-20, cy-72, 16, '#ffffff')
        draw_circle(draw, cx+20, cy-72, 16, '#ffffff')
        draw_circle(draw, cx-18, cy-70, 10, eye_color)
        draw_circle(draw, cx+22, cy-70, 10, eye_color)
        # Light reflections in eyes
        draw_circle(draw, cx-22, cy-76, 4, '#ffffff')
        draw_circle(draw, cx+18, cy-76, 4, '#ffffff')
        # Happy mouth - open smile
        draw.arc((cx-20, cy-55, cx+20, cy-35), 0, 180, fill=accent_color, width=3)
        # Antenna - zigzag
        draw.line([(cx, cy-115), (cx-10, cy-130), (cx+10, cy-145), (cx, cy-155)], fill=accent_color, width=3)
        draw_circle(draw, cx, cy-158, 6, accent_color)
        # Arms - wavy
        # Left arm raised (waving)
        draw.line([(cx-55, cy+5), (cx-75, cy-15), (cx-90, cy-35)], fill=accent_color, width=4)
        draw_circle(draw, cx-93, cy-38, 8, body_color, outline=accent_color, width=3)
        # Right arm
        draw.line([(cx+55, cy+5), (cx+80, cy+20), (cx+90, cy+10)], fill=accent_color, width=4)
        draw_circle(draw, cx+93, cy+8, 8, body_color, outline=accent_color, width=3)
        # Legs - short and stubby
        draw_rounded_rect(draw, (cx-30, cy+105, cx-10, cy+140), 8, body_color, outline=accent_color, outline_width=3)
        draw_rounded_rect(draw, (cx+10, cy+105, cx+30, cy+140), 8, body_color, outline=accent_color, outline_width=3)
        # Feet
        draw.ellipse((cx-38, cy+130, cx-5, cy+148), fill=body_color, outline=accent_color, width=3)
        draw.ellipse((cx+5, cy+130, cx+38, cy+148), fill=body_color, outline=accent_color, width=3)
        # Chest detail - gear/cog
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + int(12 * math.cos(rad))
            y1 = cy + 40 + int(12 * math.sin(rad))
            x2 = cx + int(18 * math.cos(rad))
            y2 = cy + 40 + int(18 * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=accent_color, width=2)
        draw_circle(draw, cx, cy+40, 10, accent_color)
        draw_circle(draw, cx, cy+40, 5, body_color)
        
        # Floating stars
        draw_star(draw, cx-80, cy-100, 6, accent_color)
        draw_star(draw, cx+85, cy-85, 5, accent_color)
        draw_star(draw, cx+75, cy+100, 4, accent_color)

def draw_star(draw, cx, cy, size, color):
    """Draw a simple 4-pointed star."""
    draw.line([(cx-size, cy), (cx+size, cy)], fill=color, width=2)
    draw.line([(cx, cy-size), (cx, cy+size)], fill=color, width=2)
    s2 = size * 0.6
    draw.line([(cx-s2, cy-s2), (cx+s2, cy+s2)], fill=color, width=1)
    draw.line([(cx+s2, cy-s2), (cx-s2, cy+s2)], fill=color, width=1)

def draw_platform_circles(draw):
    """Draw subtle platform circles under robots."""
    for cx, color in [(210, '#22c55e'), (512, '#3b82f6'), (814, '#f97316')]:
        # Ellipse shadow/platform
        draw.ellipse((cx-80, 700, cx+80, 740), fill=color + '20')
        draw.ellipse((cx-70, 705, cx+70, 735), fill=color + '15')

def draw_connection_lines(draw):
    """Draw subtle connection lines between robots."""
    # Dashed-style connection lines
    y = 520
    for x in range(300, 420, 8):
        draw.line([(x, y), (x+4, y)], fill=(120, 140, 200), width=1)
    for x in range(604, 724, 8):
        draw.line([(x, y), (x+4, y)], fill=(120, 140, 200), width=1)

def draw_floating_code_elements(draw):
    """Draw small floating code/tech elements in background."""
    elements = [
        (80, 150, '{  }'), (900, 180, '< />'), (120, 850, '01'),
        (880, 800, '{ }'), (500, 120, '//'), (60, 500, '[ ]'),
        (950, 450, '( )'), (480, 900, '=> '), 
    ]
    try:
        small_font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16)
    except:
        small_font = ImageFont.load_default()
    
    for x, y, text in elements:
        draw.text((x, y), text, font=small_font, fill=(150, 160, 210))

def draw_glow_circles(draw):
    """Draw soft glow circles in background."""
    glows = [
        (150, 300, 120, (100, 180, 255, 8)),
        (870, 250, 100, (180, 120, 255, 8)),
        (512, 800, 150, (140, 150, 255, 6)),
    ]
    for cx, cy, radius, color in glows:
        for r in range(radius, 0, -3):
            alpha_factor = (radius - r) / radius
            c = tuple(color[:3])
            draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=c)

def main():
    # Create base image with gradient
    img = Image.new('RGB', (W, H))
    draw_gradient_bg(img)
    
    draw = ImageDraw.Draw(img)
    
    # Add subtle grid
    draw_subtle_grid(draw)
    
    # Add glow effects
    draw_glow_circles(draw)
    
    # Add floating code elements
    draw_floating_code_elements(draw)
    
    # Add connection lines between robot positions
    draw_connection_lines(draw)
    
    # Add platform circles
    draw_platform_circles(draw)
    
    # Draw three robots with distinct personalities
    robot_y = 530  # Vertical center for robots
    
    # Robot 1: OpenCode (Green, friendly, rounded) - LEFT
    draw_robot(draw, 210, robot_y, 'rounded',
               accent_color='#22c55e',
               body_color='#e8f8ec',
               eye_color='#22c55e')
    
    # Robot 2: Claude Code (Blue, professional, angular) - CENTER
    draw_robot(draw, 512, robot_y, 'angular',
               accent_color='#3b82f6',
               body_color='#e8f0ff',
               eye_color='#3b82f6')
    
    # Robot 3: Codex (Orange, playful, circular) - RIGHT
    draw_robot(draw, 814, robot_y, 'circular',
               accent_color='#f97316',
               body_color='#fff0e0',
               eye_color='#f97316')
    
    # Add subtle vignette effect
    vignette = Image.new('RGB', (W, H), (0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    for i in range(0, 200, 2):
        alpha = int(255 * (1 - i/200) * 0.15)
        vignette_draw.rectangle((i, i, W-i, H-i), outline=(alpha, alpha, alpha))
    
    # Final soft blur pass on the background for smoothness (blur a copy, composite)
    # Actually let's just save as-is, the gradient already looks good
    
    output_path = os.path.join(output_dir, 'cover_robots_1024.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {img.size}")

if __name__ == '__main__':
    main()
