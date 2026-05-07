"""Convert white-background JPGs to transparent PNGs."""
import os
import sys
from PIL import Image

ASSETS = '/Users/joshuasmall/development/rock-hill-map/assets'

def strip_white(infile, outfile, threshold=235):
    img = Image.open(infile).convert('RGBA')
    pixels = img.load()
    w, h = img.size
    # use a flood fill from corners to remove only the background, not internal whites
    from collections import deque
    visited = [[False]*h for _ in range(w)]
    queue = deque()
    for x in [0, w-1]:
        for y in range(h):
            queue.append((x,y))
    for y in [0, h-1]:
        for x in range(w):
            queue.append((x,y))
    while queue:
        x,y = queue.popleft()
        if x<0 or x>=w or y<0 or y>=h or visited[x][y]:
            continue
        r,g,b,a = pixels[x,y]
        if r >= threshold and g >= threshold and b >= threshold:
            pixels[x,y] = (r,g,b,0)
            visited[x][y] = True
            queue.append((x+1,y))
            queue.append((x-1,y))
            queue.append((x,y+1))
            queue.append((x,y-1))
    img.save(outfile, 'PNG', optimize=True)
    return os.path.getsize(outfile)

if __name__ == '__main__':
    files = [f for f in os.listdir(ASSETS) if f.endswith('.jpg')]
    for f in sorted(files):
        infile = os.path.join(ASSETS, f)
        outfile = os.path.join(ASSETS, f.replace('.jpg','.png'))
        sz = strip_white(infile, outfile)
        print(f'{f} -> {os.path.basename(outfile)} ({sz//1024} KB)')
