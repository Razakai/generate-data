import string
import random
from glob import glob
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from generateData.image import ImageUtil
#image_util = ImageUtil(128, 540)
image_util = ImageUtil(50, 200)

def textGenerator():
    return ''.join(random.choice(string.digits + string.ascii_uppercase + '-') for _ in range(random.randint(8, 15)))


def randomPadding():
    return random.randint(10, 25), random.randint(10, 25), random.randint(0, 3), random.randint(0, 3)

def randomFont():
    font = random.choice(list(glob('../fonts/*.ttf')))
    print('\n\n\n', font)
    return ImageFont.truetype(font, size = random.randint(30, 40))


def randomBackground(height, width):
    imagePath = random.choice(list(glob('../STOCK_IMAGES/*.PNG')))
    original = Image.open(imagePath)
    L = original.convert('L')
    original = Image.merge('RGB', (L, L, L))
    left = random.randint(0, original.size[0] - height)
    top = random.randint(0, original.size[1] - width)
    right = left + height
    bottom = top + width
    return original.crop((left, top, right, bottom))


def generateImage(text):
    font = randomFont()
    textWidth, textHeight = font.getsize(text)
    paddingLeft, paddingRight, paddingTop, paddingBottom = randomPadding()
    height = paddingLeft + textWidth + paddingRight
    width = paddingTop + textHeight + paddingBottom
    image = randomBackground(height, width)

    stroke_sat = int(np.array(image).mean())
    #sat = int((stroke_sat + 127) % 255)
    sat = 255
    #mask = Image.new('RGB', (height, width))
    #canvas = ImageDraw.Draw(mask)
    canvas = ImageDraw.Draw(image)
    canvas.text((paddingLeft, paddingTop), text, fill=65, font=font, stroke_width=1)

    #lower = int(-10 + (textWidth / 32))
    #upper = int(10 - (textWidth / 32))
    #if upper < lower:
     #   upper = lower
    #mask = mask.rotate(random.randint(lower, upper))
    #image.paste(mask, (0, 0), mask)

    image = np.array(image)
    image = image_util.preprocess(image)

    return image


def main():
    fp = open('../DATA/test.txt', 'w')
    for num in range(5000):
        print(num)
        text = textGenerator()
        image = generateImage(text)
        image = np.squeeze(image, axis=-1)
        image = Image.fromarray(np.uint8((image + 1.0) * 127.5))
        image.save(f'../DATA/TEST/{num}.jpg')
        fp.write(f'{num}.jpg {text}\n')


main()