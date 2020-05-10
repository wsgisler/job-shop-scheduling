# This is just a helper file that generates a JSON file with visually distinct color. We will use this to visualize the tasks in the blocking job shop

from math import sqrt
from random import randint
import json
import colorsys

def color_difference(c1, c2):
    lab1 = rgb2lab(c1) # we convert the colors to CIE-Lab first, since the color distance is easier to compare in that format
    lab2 = rgb2lab(c2)
    return sqrt((lab1[0]-lab2[0])**2 + (lab1[1]-lab2[1])**2 + (lab1[2]-lab2[2])**2)
    
def rgb2lab(c):
    R = c[0]
    G = c[1]
    B = c[2]
    eps = 216.0 / 24389.0
    k = 24389.0 / 27.0
    Xr = 0.964221
    Yr = 1.0
    Zr = 0.825211

    r = R / 255.0
    g = G / 255.0
    b = B / 255.0

    if r <= 0.04045:
        r = r / 12
    else:
        r = ((r + 0.055) / 1.055)**2.4

    if g <= 0.04045:
        g = g / 12
    else:
        g = ((g + 0.055)/ 1.055)**2.4

    if b <= 0.04045:
        b = b / 12
    else:
        b = ((b + 0.055) / 1.055)**2.4

    X = 0.436052025 * r + 0.385081593 * g + 0.143087414 * b
    Y = 0.222491598 * r + 0.71688606 * g + 0.060621486 * b
    Z = 0.013929122 * r + 0.097097002 * g + 0.71418547 * b

    xr = X / Xr;
    yr = Y / Yr;
    zr = Z / Zr;

    if xr > eps:
        fx = xr**(1/3)
    else:
        fx = (k * xr + 16) / 116

    if yr > eps:
        fy = yr**(1/3)
    else:
        fy = (k * yr + 16) / 116

    if zr > eps:
        fz = zr**(1/3)
    else:
        fz = (k * zr + 16) / 116

    Ls = (116 * fy) - 16
    ass = 500 * (fx - fy)
    bs = 200 * (fy - fz)
    
    return (int(2.55*Ls+0.5), int(ass+0.5), int(bs+0.5))

def step (r,g,b, repetitions=1): # we use this for sorting
	lum = sqrt( .241 * r + .691 * g + .068 * b )

	h, s, v = colorsys.rgb_to_hsv(r,g,b)

	h2 = int(h * repetitions)
	lum2 = int(lum * repetitions)
	v2 = int(v * repetitions)

	if h2 % 2 == 1:
		v2 = repetitions - v2
		lum = repetitions - lum

	return (h2, lum, v2)

def generate_colors(n = 5, iterations = 100):
    # returns a list of n colors in the following format: (r, g, b, hex value of the color, hex value for white or black, depending on which one is more visually distinct)
    best_colors = []
    global_max_diff = 0
    for i in range(iterations):
        min_diff = 200000
        colors = []
        for c in range(n):
            r = randint(0,255)
            g = randint(0,255)
            b = randint(0,255)
            colors.append((r,g,b))
        for i1, c1 in enumerate(colors):
            for i2, c2 in enumerate(colors):
                if i1 != i2:
                    cd = color_difference(c1, c2)
                    min_diff = cd if cd < min_diff else min_diff
        if global_max_diff < min_diff:
            print(min_diff)
            global_max_diff = min_diff
            best_colors = colors
    f = open('colorsamples.html', 'w')
    print('Min difference: %f'%global_max_diff)
    print('---------------------------')
    print()
    for i, c in enumerate(best_colors):
        print('Color %i'%i)
        print('RGB(%i,%i,%i) or #%02x%02x%02x'%(c[0],c[1],c[2],c[0],c[1],c[2]))
        print('')
        hex_color = '#%02x%02x%02x'%(c[0],c[1],c[2])
        text_color = '#000000' if color_difference(c, (0,0,0)) > color_difference(c, (255,255,255)) else '#FFFFFF'
        f.write('<div style="position: absolute; left: %ipx; top: 10px; width: 70px; height: 70px; background-color: %s; color: %s; text-align: center"><div style="position: absolute; text-align: center; width: 70px; margin: 0; top: 50%%; -ms-transform: translateY(-50%%); transform: translateY(-50%%)">%s</div></div>'%(10+80*i, hex_color, text_color, hex_color))
    f.close()
    best_colors.sort(key=lambda c: step(c[0]/255.0,c[1]/255.0,c[2]/255.0,8) )
    best_colors = [(c[0], c[1], c[2], '#%02x%02x%02x'%(c[0],c[1],c[2]), '#000000' if color_difference(c, (0,0,0)) > color_difference(c, (255,255,255)) else '#FFFFFF') for c in best_colors]
    return best_colors
        
# generate_colors(15, 100) # generate 15 visually distinct colors using 100 iterations

solution_dict = {}
for i in range(2, 30):
    solution_dict[i] = generate_colors(i, 10000)
with open('colors.json', 'w') as fp:
    json.dump(solution_dict, fp, sort_keys=True, indent=4)