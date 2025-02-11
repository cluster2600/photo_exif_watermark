import os
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageOps
import rawpy
import pillow_heif
pillow_heif.register_heif_opener()
#copyright cluster2600
# On définit une valeur cible de DPI pour le calcul du cadre, ici 300 DPI.
TARGET_DPI = 300

def add_watermark_and_frame(file_path: str, signature: str, border_cm: int = 2, target_dpi: int = TARGET_DPI) -> None:
    """
    Ouvre une image (JPG, JPEG, PNG, HEIC) sans corriger son orientation,
    applique un cadre blanc dont la largeur est calculée pour obtenir border_cm (ici 2 cm) à target_dpi,
    puis incruste la signature en bas à droite en noir avec une police manuscrite.
    """
    # Calcul du nombre de pixels correspondant à border_cm (ici 2 cm)
    border_pixels = calculate_border_pixels(border_cm, target_dpi)
    
    img_with_border = add_border(file_path, border_pixels)
    if img_with_border is None:
        return

    if not add_watermark(img_with_border, signature):
        return

    save_image(img_with_border, file_path, target_dpi)

def process_dng(file_path: str, signature: str, border_cm: int = 2, target_dpi: int = TARGET_DPI) -> None:
    """
    Ouvre un fichier DNG avec rawpy, convertit en image RGB,
    applique un cadre blanc avec une largeur calculée selon target_dpi,
    incruste le watermark, puis sauvegarde le résultat sous un nouveau nom avec le suffixe '_watermarked.jpg'.
    """
    border_pixels = calculate_border_pixels(border_cm, target_dpi)
    img_with_border = process_raw_image(file_path, border_pixels)
    if img_with_border is None:
        return

    if not add_watermark(img_with_border, signature):
        return

    new_file = file_path.rsplit('.', 1)[0] + "_watermarked.jpg"
    save_image(img_with_border, new_file, target_dpi)

def process_images(directory: str, signature: str) -> None:
    valid_exts = {".jpg", ".jpeg", ".png", ".heic"}
    dng_exts = {".dng"}
    
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(directory, filename)
        if "_watermarked" in filename:
            print(f"Image déjà traitée, passage de {filename}")
            continue
        elif ext in valid_exts:
            add_watermark_and_frame(file_path, signature)
        elif ext in dng_exts:
            process_dng(file_path, signature)
        else:
            print(f"Format non traité pour {filename}")

def calculate_border_pixels(border_cm: int, target_dpi: int) -> int:
    return int((target_dpi / 2.54) * border_cm)

def add_border(file_path: str, border_pixels: int) -> Optional[Image.Image]:
    try:
        img = Image.open(file_path)
        return ImageOps.expand(img, border=border_pixels, fill="white")
    except Exception as e:
        print(f"Erreur lors de l'ouverture de {file_path} : {e}")
        return None

def add_watermark(img: Image.Image, signature: str) -> bool:
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/MarkerFelt.ttc", 50)
    except Exception as e:
        print(f"Erreur lors du chargement de la police : {e}")
        return False

    text = signature
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    width, height = img.size
    x = width - text_width - 10
    y = height - text_height - 10

    draw.text((x, y), text, font=font, fill="black")
    return True

def save_image(img: Image.Image, file_path: str, target_dpi: int) -> None:
    try:
        img.save(file_path, dpi=(target_dpi, target_dpi))
        print(f"Image sauvegardée sous {file_path} (utilisation de {target_dpi} DPI)")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {file_path} : {e}")

def process_raw_image(file_path: str, border_pixels: int) -> Optional[Image.Image]:
    try:
        with rawpy.imread(file_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
        return ImageOps.expand(img, border=border_pixels, fill="white")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier DNG {file_path} : {e}")
        return None

    export_dir = "/Volumes/backup"  # Dossier contenant vos images exportées
    signature = "Maxime Grenu"       # Votre signature
    process_images(export_dir, signature)
