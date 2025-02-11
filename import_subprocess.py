import os
import subprocess

def add_signature_exif(file_path, signature):
    # Commande pour modifier les métadonnées avec exiftool
    cmd = [
        "exiftool",
        "-overwrite_original",  # écrase le fichier original (assurez-vous d'avoir une sauvegarde !)
        f"-Artist={signature}",
        f"-Copyright={signature}",
        f"-UserComment={signature}",
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Signature EXIF ajoutée à : {file_path}")
    else:
        print(f"Erreur pour {file_path} : {result.stderr}")

def process_exif(directory, signature):
    # Extensions d'images à traiter
    valid_exts = {".jpg", ".jpeg", ".heic", ".dng"}
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_exts:
            file_path = os.path.join(directory, filename)
            add_signature_exif(file_path, signature)

if __name__ == "__main__":
    export_dir = "/Volumes/backup"  # dossier contenant vos fichiers exportés
    signature = "Maxime Grenu"       # votre signature
    process_exif(export_dir, signature)