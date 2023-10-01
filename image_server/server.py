"""Small server to diplay local images in a grid
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.responses import StreamingResponse
import os
import io
from PIL import Image
from rich.progress import track
from rich.console import Console
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader


# Configure the Environment to use the ChoiceLoader
env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader('templates'),  
        PackageLoader('image_server', 'templates') 
    ])
)

console = Console()

app = FastAPI()


def create_thumbnails(image_files, directory):
    thumbnails_dir = os.path.join(directory, "thumbnails")

    if os.path.exists(thumbnails_dir):
        console.print(f"{thumbnails_dir} already exists, skipping creation")
    else:
        base_height = 240
        os.makedirs(thumbnails_dir, exist_ok=True)
        for img_file in track(image_files, description="Creating thumbnails..."):
            _, ext = os.path.splitext(img_file)
            if ext not in [".jpg", ".png", ".jpeg"]:
                continue
            
            # Open an image with PIL
            img = Image.open(os.path.join(directory, img_file))

            # Resize while maintaining the aspect ratio
            hpercent = base_height / float(img.size[1])
            wsize = int(float(img.size[0]) * float(hpercent))
            img = img.resize((wsize, base_height), Image.LANCZOS)

            # Save image to buffer
            img.save(os.path.join(directory, "thumbnails", img_file), format='JPEG', quality=85)

    return thumbnails_dir


@app.get("/")
async def read_root(request: Request, images_dir: str = "images"):
    console.print(f"Processing images from {images_dir} :optical_disk:")

    if not os.path.exists(images_dir):
        raise HTTPException(status_code=404, detail="Directory not found")

    # List all files in the image directory
    image_files = sorted([f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))])
    thumbnail_dir_name = create_thumbnails(image_files, images_dir)
    image_thumbs = sorted([f for f in os.listdir(thumbnail_dir_name) if os.path.isfile(os.path.join(thumbnail_dir_name, f))])

    thumbs_dir_for_js = thumbnail_dir_name.replace("\\", "/") # replace the \\ with / for correct interpretation by javascript
    images_dir_for_js = images_dir.replace("\\", "/") # replace the \\ with / for correct interpretation by javascript
    img_data = [(img,info.replace("\\", "/")) for img,info in zip(image_thumbs, image_files)]
    template = env.get_template('index.html')
    html_content = template.render(url_for=request.url_for, images=img_data, thumbs_dir=thumbs_dir_for_js, images_dir=images_dir_for_js)
    return HTMLResponse(content=html_content)


@app.get("/images/{path:path}")
async def serve_image(path: str):
    file_path = path
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
          
    with open(file_path, "rb") as f:
        content = f.read()
    return StreamingResponse(io.BytesIO(content), media_type="image/jpeg")


def main():
    import uvicorn
    console.print(":globe_showing_americas: Welcome to Image server :globe_showing_europe-africa:")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # For images in images directory: http://127.0.0.1:8000/?images_dir=images
    # For another directory other_folder: http://127.0.0.1:8000/?images_dir=other_folder
    # For windows http://127.0.0.1:8000/?images_dir=C:\\Users\\msalvaris\\Documents\\ml_group_ppt_images
    
if __name__=="__main__":
    main()
