import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import rawpy
import pillow_heif
pillow_heif.register_heif_opener()

# On définit une valeur cible de DPI pour le calcul du cadre, ici 300 DPI.
TARGET_DPI = 300

def add_watermark_and_frame(file_path, signature, border_cm=2, target_dpi=TARGET_DPI):
    """
    Ouvre une image (JPG, JPEG, PNG, HEIC) sans corriger son orientation,
    applique un cadre blanc dont la largeur est calculée pour obtenir border_cm (ici 2 cm) à target_dpi,
    puis incruste la signature en bas à droite en noir avec une police manuscrite.
    """
    # Calcul du nombre de pixels correspondant à border_cm (ici 2 cm)
    border_pixels = int((target_dpi / 2.54) * border_cm)
    
    try:
        img = Image.open(file_path)
    except Exception as e:
        print(f"Erreur lors de l'ouverture de {file_path} : {e}")
        return

    # Pas de correction d'orientation, vous la ferez manuellement
    # Ajout du cadre blanc
    img_with_border = ImageOps.expand(img, border=border_pixels, fill="white")
    
    # Préparation pour incruster le watermark
    draw = ImageDraw.Draw(img_with_border)
    
    try:
        # Utilisation d'une police manuscrite, par exemple MarkerFelt
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/MarkerFelt.ttc", 50)
    except Exception as e:
        print(f"Erreur lors du chargement de la police pour {file_path} : {e}")
        return
    
    text = signature
    # Calcul de la taille du texte (avec textbbox, méthode compatible avec Pillow 10+)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    width, height = img_with_border.size
    x = width - text_width - 10
    y = height - text_height - 10
    
    # Dessiner le texte en noir
    draw.text((x, y), text, font=font, fill="black")
    
    try:
        # On sauvegarde en ajoutant le DPI cible pour cohérence
        img_with_border.save(file_path, dpi=(target_dpi, target_dpi))
        print(f"Watermark et cadre ajoutés à : {file_path} (utilisation de {target_dpi} DPI)")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {file_path} : {e}")

def process_dng(file_path, signature, border_cm=2, target_dpi=TARGET_DPI):
    """
    Ouvre un fichier DNG avec rawpy, convertit en image RGB,
    applique un cadre blanc avec une largeur calculée selon target_dpi,
    incruste le watermark, puis sauvegarde le résultat sous un nouveau nom avec le suffixe '_watermarked.jpg'.
    """
    border_pixels = int((target_dpi / 2.54) * border_cm)
    
    try:
        with rawpy.imread(file_path) as raw:
            rgb = raw.postprocess()  # Conversion en image RGB (8 bits)
        img = Image.fromarray(rgb)
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier DNG {file_path} : {e}")
        return
    
    # Pas de correction d'orientation (à faire manuellement si besoin)
    img_with_border = ImageOps.expand(img, border=border_pixels, fill="white")
    
    draw = ImageDraw.Draw(img_with_border)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/MarkerFelt.ttc", 50)
    except Exception as e:
        print(f"Erreur lors du chargement de la police pour {file_path} : {e}")
        return
    
    text = signature
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    width, height = img_with_border.size
    x = width - text_width - 10
    y = height - text_height - 10

    draw.text((x, y), text, font=font, fill="black")
    
    new_file = file_path.rsplit('.', 1)[0] + "_watermarked.jpg"
    try:
        img_with_border.save(new_file, dpi=(target_dpi, target_dpi))
        print(f"Fichier DNG traité et sauvegardé sous {new_file} (utilisation de {target_dpi} DPI)")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {file_path} : {e}")

def process_images(directory, signature):
    valid_exts = {".jpg", ".jpeg", ".png", ".heic"}
    dng_exts = {".dng"}
    
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(directory, filename)
        if ext in valid_exts:
            add_watermark_and_frame(file_path, signature)
        elif ext in dng_exts:
            process_dng(file_path, signature)
        else:
            print(f"Format non traité pour {filename}")

if __name__ == "__main__":
    export_dir = "/Volumes/backup"  # Dossier contenant vos images exportées
    signature = "Maxime Grenu"       # Votre signature
    process_images(export_dir, signature)