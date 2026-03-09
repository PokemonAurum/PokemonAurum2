from PIL import Image
import os

SHEET_DIR = '/home/ibalaji/git/hg-engine/incoming_sprites/Mega Evolution'
OUT_DIR = '/home/ibalaji/git/hg-engine/data/graphics/sprites'

SPRITE_MAP = {
    '026-XMega.png': 'mega_raichu_x',
    '071-Mega.png':  'mega_victreebel',
    '160-Mega.png':  'mega_feraligatr',
    '227-Mega.png':  'mega_skarmory',
    '398-Mega.png':  'mega_staraptor',
    '545-Mega.png':  'mega_scolipede',
    '609-Mega.png':  'mega_chandelure',
    '652-Mega.png':  'mega_chesnaught',
    '655-Mega.png':  'mega_delphox',
    '658-Mega.png':  'mega_greninja',
    '668-Mega.png':  'mega_pyroar',
    '691-Mega.png':  'mega_dragalge',
    '701-Mega.png':  'mega_hawlucha',
    '870-Mega.png':  'mega_falinks',
    '970-Mega.png':  'mega_glimmora',
}

def process_sprite(crop, canvas_w=160, canvas_h=80):
    # Convert crop to RGBA
    rgba = crop.convert('RGBA')
    
    # Place on canvas centered
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    x = (canvas_w - crop.width) // 2
    y = (canvas_h - crop.height) // 2
    canvas.paste(rgba, (x, y))
    
    # Get all unique RGBA colors
    pixels = list(canvas.getdata())
    
    # Separate transparent and opaque pixels
    transparent = (0, 0, 0, 0)
    opaque_colors = []
    for p in pixels:
        if p[3] == 0:
            continue
        rgb = p[:3]
        if rgb not in opaque_colors:
            opaque_colors.append(rgb)
    
    # Build palette with transparency at index 0
    # Max 15 opaque colors + 1 transparent = 16 total
    if len(opaque_colors) > 15:
        # Need to reduce - convert to RGB and quantize to 15 colors
        rgb_canvas = canvas.convert('RGB')
        quantized = rgb_canvas.quantize(colors=15, method=Image.Quantize.FASTOCTREE)
        pal_data = quantized.getpalette()[:15*3]
        opaque_colors = [(pal_data[i*3], pal_data[i*3+1], pal_data[i*3+2]) for i in range(15)]
    
    # Build 16-color palette: index 0 = transparent (0,0,0), indices 1-15 = opaque colors
    palette = [(0, 0, 0)] + opaque_colors[:15]
    # Pad to 16 colors
    while len(palette) < 16:
        palette.append((0, 0, 0))
    
    # Build flat palette list (PIL needs 256*3)
    flat_palette = []
    for r, g, b in palette:
        flat_palette.extend([r, g, b])
    # Pad to 256 colors
    flat_palette.extend([0] * (256*3 - len(flat_palette)))
    
    # Create color lookup
    color_to_idx = {}
    for i, (r, g, b) in enumerate(palette):
        color_to_idx[(r, g, b)] = i
    
    # Create output image
    out = Image.new('P', (canvas_w, canvas_h))
    out.putpalette(flat_palette)
    
    # Map pixels
    out_pixels = []
    for p in pixels:
        if p[3] == 0:
            out_pixels.append(0)  # transparent = index 0
        else:
            rgb = p[:3]
            # Find closest color in palette
            if rgb in color_to_idx:
                out_pixels.append(color_to_idx[rgb])
            else:
                # Find nearest
                best_idx = 1
                best_dist = float('inf')
                for i, (r, g, b) in enumerate(palette[1:], 1):
                    dist = (rgb[0]-r)**2 + (rgb[1]-g)**2 + (rgb[2]-b)**2
                    if dist < best_dist:
                        best_dist = dist
                        best_idx = i
                out_pixels.append(best_idx)
    
    out.putdata(out_pixels)
    out.putpalette(flat_palette[:48])
    out.info['transparency'] = 0
    return out

for filename, folder in SPRITE_MAP.items():
    path = os.path.join(SHEET_DIR, filename)
    if not os.path.exists(path):
        print(f'MISSING: {filename}')
        continue

    sheet = Image.open(path)
    w, h = sheet.size
    sprite_w = w // 4

    front       = sheet.crop((0*sprite_w, 0, 1*sprite_w, h))
    back        = sheet.crop((1*sprite_w, 0, 2*sprite_w, h))
    shiny_front = sheet.crop((2*sprite_w, 0, 3*sprite_w, h))
    shiny_back  = sheet.crop((3*sprite_w, 0, 4*sprite_w, h))

    male_dir   = os.path.join(OUT_DIR, folder, 'male')
    female_dir = os.path.join(OUT_DIR, folder, 'female')

    process_sprite(front).save(os.path.join(male_dir, 'front.png'))
    process_sprite(back).save(os.path.join(male_dir, 'back.png'))
    process_sprite(front).save(os.path.join(female_dir, 'front.png'))
    process_sprite(back).save(os.path.join(female_dir, 'back.png'))

    process_sprite(shiny_front).save(os.path.join(male_dir, 'front_shiny.png'))
    process_sprite(shiny_back).save(os.path.join(male_dir, 'back_shiny.png'))

    print(f'Done: {folder}')

print('All done!')
