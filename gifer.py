#.txt to .png conversion ripped from Kobe John https://github.com/kobejohn

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import os
import imageio

n_frame = 0

with Image.open('wow.gif') as im:
    n_frame = im.n_frames
    print(str(n_frame) + " frames")
    if (im.is_animated):
        for i in range(0, n_frame):
            im.seek(i)
            im.save('{}.png'.format(i))
    else:
        print("TODO: handle non animated gifs")


#CONVERT GIFS TO TXTS ====================================================
# def monochrome(imgname, extension):
#     photo = Image.open(imgname+extension)
#     photo = photo.convert('1')  
#     return photo


# def readpixels(img, x, y):
#     pixel = img.load()  
#     return pixel[x,y] 


# def makeascii(img, imgname):
#     width, height = img.size
#     x = 0  
#     y = 0  

#     chars = {0: '$', 255: ' '}

#     text_file = open(imgname+'.txt', 'w')

#     while y <= height - 1:
#         rgb = readpixels(img, x, y)
#         text_file.write(chars[rgb])

#         x += 1  

#         if x == width - 1:
#             text_file.write('\n')
#             x = 0
#             y += 1

#     text_file.close()

# for i in range(0, n_frame):
#     makeascii(monochrome(str(i), ".png"), str(i))

#SAVE TXTs TO PNGs ================================================

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"


def main(i):
    image = text_image(str(i) + '.txt')
    image.save(str(i) + '.png')


def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0]) 
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image

for i in range(0, n_frame):
    main(i)

#SAVE OUTPUT TO GIF ====================================================
png_dir = '.'
images = []
for file_name in os.listdir(png_dir):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))

imageio.mimsave('../gif_test/output.gif', images)

for i in range(0, n_frame):
    os.remove(str(i) + ".png")
    os.remove(str(i) + ".txt")