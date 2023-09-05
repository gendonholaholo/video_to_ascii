import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw
import timeit

SCALING    = 1.0
YSTRETCH   = 0.5
FONTSIZE   = 10

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                            FONTSIZE, encoding="unic")
chars = list("$@B%8&M#*ahkbdqwmZO0QLCJUYXzcvnxrjft/\|()1{}[]?-_+~<>i!lI:,^`'. ")
vidcap = cv.VideoCapture('./WhatsApp Video 2023-09-04 at 15.55.48.mp4')

success,frame    = vidcap.read()
height, width, _ = frame.shape
height           = int(height * SCALING * YSTRETCH)
width            = int(width * SCALING)

property_id = int(cv.CAP_PROP_FRAME_COUNT) 
num_frames  = int(cv.VideoCapture.get(vidcap, property_id))

fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('outvid-2.mp4', fourcc, 60.0, (width * 4, height * 8))

count = 0
while success:
    frame = cv.resize(frame, (width, height), interpolation = cv.INTER_AREA)

    b, g, r = cv.split(frame)
    frame = np.maximum(b, g, r)
    frame = frame // 4

    out_mat = [[0 for x in range(width+1)] for y in range(height)]
    for i in range(height):
        for j in range(width):
            brightness = frame[i][j]
            out_mat[i][j] = chars[brightness]
        out_mat[i][width] = '\n'


    out_frame = Image.new("RGB", (width * 4, height * 8), (255, 255, 255))
    draw = ImageDraw.Draw(out_frame)

    frame_text = ''.join([j for sub in out_mat for j in sub])
    start_time = timeit.default_timer()
    draw.multiline_text((0, 0), frame_text, font=font, fill=(0, 0, 0))
    print(timeit.default_timer() - start_time)

    out_frame = np.array(out_frame)
    out.write(out_frame)
    count += 1

    success, frame = vidcap.read()

    print("%.2f%%" % (count / num_frames * 100))

out.release()
