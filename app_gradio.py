# app_gradio.py
import gradio as gr
import leaf_analysis
from PIL import Image
import numpy as np
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dossier pour sauvegarder les uploads temporairement
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def analyze_leaf(image):
    """
    Analyse une image de feuille et renvoie la gravité et l'image du masque infecté.
    
    Args:
        image: Image uploadée par l'utilisateur (PIL Image ou numpy array)
    
    Returns:
        tuple: (texte de gravité, chemin de l'image infectée)
    """
    try:
        # Sauvegarder l'image temporairement
        file_path = os.path.join(UPLOAD_FOLDER, "temp_leaf.jpg")
        if isinstance(image, np.ndarray):
            image_pil = Image.fromarray(image)
        else:
            image_pil = image
        image_pil.save(file_path)
        logger.debug(f"Image temporaire sauvegardée à : {file_path}")

        # Analyser l'image avec leaf_analysis
        logger.debug("Début de l'analyse de l'image")
        processed_image, leaf_mask, infected_mask = leaf_analysis.load_and_process_image(file_path)
        severity = leaf_analysis.calculate_severity(leaf_mask, infected_mask)
        logger.debug(f"Gravité calculée : {severity:.2f}%")

        # Sauvegarder le masque infecté pour affichage
        infected_mask_path = os.path.join(UPLOAD_FOLDER, "infected_mask.png")
        infected_image = Image.fromarray((infected_mask * 255).astype(np.uint8))
        infected_image.save(infected_mask_path)

        # Retourner les résultats
        return f"Gravité de l'infection : {severity:.2f}%", infected_mask_path

    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'image : {str(e)}")
        return f"Erreur : {str(e)}", None

# Interface Gradio
interface = gr.Interface(
    fn=analyze_leaf,  # La fonction à exécuter
    inputs=gr.Image(type="pil", label="Téléchargez une image de feuille"),  # Entrée : une image
    outputs=[
        gr.Textbox(label="Gravité de l'infection"),  # Sortie 1 : texte
        gr.Image(label="Masque des zones infectées")  # Sortie 2 : image
    ],
    title="Analyseur de maladies des feuilles",
    description="Téléchargez une image de feuille pour analyser la gravité de l'infection."
)

# Lancer l'application
if __name__ == "__main__":
    interface.launch()