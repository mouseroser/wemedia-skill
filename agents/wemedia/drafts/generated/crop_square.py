from PIL import Image
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
img = Image.open(src).convert("RGB")
pixels = img.load()
w, h = img.size
th = 15

def is_nonblack(px):
    return sum(px) > th*3

top = next((y for y in range(h) for x in range(0,w,max(1,w//400 or 1)) if is_nonblack(pixels[x,y])), 0)
bottom = next((y for y in range(h-1,-1,-1) for x in range(0,w,max(1,w//400 or 1)) if is_nonblack(pixels[x,y])), h-1)
left = next((x for x in range(w) for y in range(0,h,max(1,h//400 or 1)) if is_nonblack(pixels[x,y])), 0)
right = next((x for x in range(w-1,-1,-1) for y in range(0,h,max(1,h//400 or 1)) if is_nonblack(pixels[x,y])), w-1)
# clamp
left, top, right, bottom = max(0,left), max(0,top), min(w-1,right), min(h-1,bottom)
content_w = right-left+1
content_h = bottom-top+1
size = max(content_w, content_h)
# center square around content bounds
cx = (left + right) // 2
cy = (top + bottom) // 2
x0 = max(0, min(w - size, cx - size//2))
y0 = max(0, min(h - size, cy - size//2))
# if image smaller on one side, pad with black then crop square
if size > w or size > h:
    canvas = Image.new('RGB', (max(w,size), max(h,size)), (0,0,0))
    canvas.paste(img, ((canvas.width-w)//2, (canvas.height-h)//2))
    img = canvas
    w,h = img.size
    x0 = max(0, min(w - size, (w-size)//2))
    y0 = max(0, min(h - size, (h-size)//2))

cropped = img.crop((x0, y0, x0+size, y0+size))
if cropped.width < 1080:
    cropped = cropped.resize((1080,1080), Image.LANCZOS)
elif cropped.width != cropped.height:
    m = max(cropped.width, cropped.height)
    cropped = cropped.resize((m,m), Image.LANCZOS)
out.parent.mkdir(parents=True, exist_ok=True)
cropped.save(out, quality=95, subsampling=0)
print(out)
