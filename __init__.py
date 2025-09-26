# 1. Import the class from your RENAMED file.
from .latent_aspect_ratios import MultiAspectRatio

# 2. Update the dictionaries to use the new names.
NODE_CLASS_MAPPINGS = {
    "Latent Aspect Ratios": MultiAspectRatio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Latent Aspect Ratios": "✨ Latent Aspect Ratios"
}