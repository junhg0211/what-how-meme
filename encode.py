import argparse
from os.path import join, dirname

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *


IMAGE_PATH = 'output.png'
AUDIO_PATH = join(dirname(__file__), 'what_how.mp3')

parser = argparse.ArgumentParser(description='Encodes the mEme.')
parser.add_argument('--image', type=str, help='Image of a meme.')
parser.add_argument('--text', type=str, help='Text of a meme.')
parser.add_argument('--output', type=str, help='The directory to be out at')

args = parser.parse_args()

def draw_image():
    WIDTH, HEIGHT = 1280, 720
    FONT_PATH = join(dirname(__file__), 'res', 'font', 'TIMES.TTF')
    PADDING = 8

    cropped_image = Image.open(args.image)
    image_width, image_height = cropped_image.size
    unit = min(image_height / 3, image_width / 4)
    cropped_image = cropped_image.crop((
        left := (image_width - 4 * unit) / 2, upper := (image_height - 3 * unit) / 2,
        left + unit * 4, upper + unit * 3
    ))
    image_width, image_height = cropped_image.size
    proportion = WIDTH / image_width * .8
    cropped_image.thumbnail((image_height * proportion, image_height * proportion))
    image_width, image_height = cropped_image.size

    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))

    image.paste(cropped_image, (left := (WIDTH - image_width) // 2, upper := (HEIGHT - image_height) // 2 - HEIGHT // 16))

    draw = ImageDraw.Draw(image)
    draw.line((left - PADDING, upper - PADDING, left - PADDING, upper + image_height + PADDING))
    draw.line((left - PADDING, upper - PADDING, left + image_width + PADDING, upper - PADDING))
    draw.line((left + image_width + PADDING, upper + image_height + PADDING, left - PADDING, upper + image_height + PADDING))
    draw.line((left + image_width + PADDING, upper + image_height + PADDING, left + image_width + PADDING, upper - PADDING))

    font = ImageFont.truetype(FONT_PATH, 64)
    text_width, text_height = draw.textsize(args.text, font=font)
    draw.text((a := (WIDTH - text_width) / 2, upper + image_height + PADDING * 3), args.text, (255, 255, 255), font=font)

    image.save(IMAGE_PATH)


draw_image()

clip = ImageClip(IMAGE_PATH, duration=10)
clip.fps = 24
audio_clip = AudioFileClip(AUDIO_PATH)
clip = clip.set_audio(audio_clip)
if args.output:
    path = join(args.output, 'output.mp4')
else:
    path = 'output.mp4'
clip.write_videofile(path)
