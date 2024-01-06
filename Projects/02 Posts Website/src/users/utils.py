from pathlib import Path
from flask_login import current_user
from PIL import Image

ROOT_PATH = Path(__file__).parent

def save_picture(form_picture):
    suffix = Path(form_picture.filename).suffix
    picture_filename = f"user{current_user.id}_profile" + suffix
    picture_path = ROOT_PATH / f"static/profile_pics/{picture_filename}"
    image = Image.open(form_picture)
    image.thumbnail(size=(125, 125))
    image.save(picture_path)

    return picture_filename
