import argparse

from google.cloud import vision
from google.cloud.vision import types

from PIL import Image, ImageFilter, ImageDraw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--amount", type=int, default=100)
    args = parser.parse_args()

    image = blur_faces(args.filename, args.amount)
    image.show()

def blur_faces(filename, amount):
    client = vision.ImageAnnotatorClient()

    with open(filename, 'rb') as image_file:
        content = image_file.read()
    face_image = types.Image(content=content)

    face_annotations = client.face_detection(image=face_image).face_annotations

    im = Image.open(filename)
    draw = ImageDraw.Draw(im)

    for face in face_annotations:
        vs = face.bounding_poly.vertices
        box = [vs[0].x, vs[0].y, vs[2].x, vs[2].y]

        ic = im.crop(box)
        for i in range(amount):
            ic = ic.filter(ImageFilter.BLUR)

        im.paste(ic, box)

        # draw.rectangle(box, outline='red')

    return im

if __name__ == "__main__":
    main()
