# Notes for during talk

## Cloud Project Setup

Create project.

- We'll create a new Google Cloud Project. This lets us create and manage
resources, and keep all the things that we do in the workshop contained
in one place - and then at the end, we can just delete it, without
getting any extra costs.
- [Create a new Google Cloud Project](https://console.cloud.google.com/projectcreate)

Enable APIs.

- In our new project, we need to enable the Google Cloud Vision API. This
will let us actually interact with the Face Detection API.
- [Enable the Cloud Vision API](https://console.cloud.google.com/apis/api/vision.googleapis.com)

Create credentials.

- To actually access the API, we need to somehow authenticate (prove who
we are) to the service. All of Google's APIs and services use a similar
way of doing this.
- For this project, we're going to create a "Service Account" and then
use the credentials for that account to access the API.
- [Create a Service Account Key](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
    - Choose "Project > Owner" for Role
    - Download the credentials as JSON

## Installing dependencies

Install dependencies using pipenv. Just copy the Pipfile to your own project.

```bash
$ pipenv install
$ pipenv shell
```

If you don't have pipenv installed, or don't want to use it, you can use pip
directly instead:

```bash
$ pip install -r requirements.txt
```

## Doing the image detection

Import the Google Cloud python libraries.

```python
from google.cloud import vision
from google.cloud.vision import types
```

Create a `vision.ImageAnnotatorClient`. This is the object we'll use to
communicate with the API and get responses back.

```python
client = vision.ImageAnnotatorClient()
```

Find our image.

```python
FILENAME = "resources/justin.jpg"
```

Load the image to send off to the Face Recognition API.

```python
with open(FILENAME, 'rb') as f:
    image_raw = f.read()

image_for_api = types.Image(content=image_raw)
```

Get the face annotations!

```python
response = client.face_detection(image=image_for_api)
face_annotations = response.face_annotations
```

## Do the post-processing

Import the pillow libraries for image processing.

```python
from PIL import Image, ImageDraw, ImageFilter
```

Open our image for processing.

```
image = Image.open(FILENAME)
```

Draw a rectangle around the faces.

```python
for face in face_annotations:
    verts = face.bounding_poly.vertices
    box = [
        verts[0].x,
        verts[0].y,
        verts[2].x,
        verts[2].y
    ]

    draw = ImageDraw.Draw(image)
    draw.rectangle(box, outline='red')
```

Blur the faces.

```python
for face in face_annotations:
    ...

    ic = im.crop(box)
    for i in range(100):
        ic = ic.filter(ImageFilter.BLUR)
    im.paste(ic, box)
```
