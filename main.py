from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from models import SessionLocal, Image, Depth
from fastapi.staticfiles import StaticFiles
import cv2
from typing import Optional
import zlib
from fastapi.openapi.utils import get_openapi



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_index():
    print('root')
    return FileResponse('templates/index.html')


def compress_image(image_matrix):
    is_success, buffer = cv2.imencode(".png", image_matrix)
    if not is_success:
        raise HTTPException(status_code=500, detail="Failed to compress image")
    compressed_image = zlib.compress(buffer, level=9)
    return compressed_image


def resize_image(image_matrix, width=150, keep_aspect_ratio=False):
    if keep_aspect_ratio:
        height = int(image_matrix.shape[0] * (width / image_matrix.shape[1]))
    else:
        height = image_matrix.shape[0]
    resized_image = cv2.resize(
        image_matrix, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image


@app.post("/images")
def create_image(file: UploadFile = File(...),  keep_aspect_ratio: Optional[bool] = False, resize_width: Optional[int] = 150, db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    image_name = file.filename
    depths = df['depth'].values
    image_matrix = df.drop(['depth'], axis=1).to_numpy(dtype=np.uint8)
    resized_image_matrix = resize_image(
        image_matrix, resize_width, keep_aspect_ratio)
    compressed_image = compress_image(resized_image_matrix)
    db_image = Image(image_data=compressed_image, name=image_name)
    db.add(db_image)
    for index, depth_value in enumerate(depths):
        db_depth = Depth(value=depth_value, raw_number=index, image=db_image)
        db.add(db_depth)
    db.commit()

    return {"message": "Image and depths stored successfully", "image_id": db_image.id}


@app.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()

    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    db.query(Depth).filter(Depth.image_id == image_id).delete()
    db.delete(db_image)
    db.commit()

    return {"message": "Image and associated depths deleted successfully"}


@app.get("/images/{image_id}")
def get_image_frame(image_id: int, depth_min: Optional[int] = 0, depth_max: Optional[int] = -1, apply_color_map: Optional[bool] = True, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:

        raise HTTPException(status_code=404, detail="Image not found")

    decompressed_image_data = zlib.decompress(db_image.image_data)
    nparr = np.frombuffer(decompressed_image_data, np.uint8)
    image_matrix = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if depth_max == -1:
        first_index = 0
        depth_max = image_matrix.shape[0]

    first_index = db.query(Depth).filter(
        Depth.image_id == image_id, Depth.value == depth_min).first()
    last_index = db.query(Depth).filter(
        Depth.image_id == image_id, Depth.value == depth_max).first()

    if not first_index or not last_index:
        raise HTTPException(
            status_code=404, detail="Depth range not found for this image")
    else:
        first_index = first_index.raw_number
        last_index = last_index.raw_number

    cropped_image = image_matrix[first_index:last_index + 1]
    colored_image = cv2.applyColorMap(cropped_image, cv2.COLORMAP_JET)

    is_success, buffer = cv2.imencode(
        ".png", colored_image if apply_color_map else cropped_image)
    if not is_success:
        raise HTTPException(status_code=500, detail="Failed to process  image")

    return Response(content=buffer.tobytes(), media_type="image/png")


@app.get("/images")
def get_img(db: Session = Depends(get_db)):
    images = db.query(Image.id, Image.name).all()
    return {"images": [{'id': image.id, 'name': image.name} for image in images]}
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi