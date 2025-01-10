from PIL import Image

def generate_overlay_image(original_path, mask_path):
    original = Image.open(original_path).convert("RGB")
    mask = Image.open(mask_path).convert("RGB")
    
    if original.size != mask.size:
        mask = mask.resize(original.size, Image.Resampling.LANCZOS)
    
    overlay = Image.blend(original, mask, alpha=0.5)
    return overlay