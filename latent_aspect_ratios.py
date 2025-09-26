import torch

# We now store all resolutions in a single dictionary for reliability.
RESOLUTIONS = {
    # FLUX Resolutions
    "768x768 (1:1) - Square Medium": (768, 768), "768x1024 (3:4) - Portrait Small": (768, 1024), "1024x768 (4:3) - Landscape Small": (1024, 768), "1152x768 (3:2) - Wide Small": (1152, 768), "768x1152 (2:3) - Portrait Medium": (768, 1152), "1536x768 (2:1) - Ultra Wide Small": (1536, 768), "768x1536 (1:2) - Portrait Large": (768, 1536), "1024x1024 (1:1) - Square Large": (1024, 1024), "896x1280 (7:10) - Portrait Small HD": (896, 1280), "1280x896 (10:7) - Landscape Small HD": (1280, 896), "1536x896 (12:7) - Wide Medium": (1536, 896), "896x1536 (7:12) - Portrait HD": (896, 1536), "2048x896 (8:7) - Ultra Wide Medium": (2048, 896), "896x2048 (7:8) - Portrait Ultra HD": (896, 2048), "1280x1280 (1:1) - Square HD": (1280, 1280), "1152x1664 (9:13) - Portrait Medium Plus": (1152, 1664), "1664x1152 (13:9) - Landscape Medium Plus": (1664, 1152), "1920x1152 (5:3) - Wide Large": (1920, 1152), "1152x1920 (3:5) - Portrait Large HD": (1152, 1920), "2560x1152 (16:9) - Ultra Wide Large": (2560, 1152), "1152x2560 (9:16) - Portrait Ultra Large": (1152, 2560), "1536x1536 (1:1) - Square Extra Large": (1536, 1536), "1408x1920 (11:15) - Portrait Extra HD": (1408, 1920), "1920x1408 (15:11) - Landscape Extra HD": (1920, 1408), "2304x1408 (12:7) - Wide Extra Large": (2304, 1408), "1408x2304 (7:12) - Portrait Super HD": (1408, 2304), "3072x1408 (16:9) - Ultra Wide Extra Large": (3072, 1408), "1408x3072 (9:16) - Portrait Super Ultra HD": (1408, 3072), "3840x2160 (16:9) - 4K UHD": (3840, 2160), "2160x3840 (9:16) - 4K UHD Portrait": (2160, 3840),
    # QWEN Resolutions
    "Qwen 1:1 Square (1328x1328)": (1328, 1328), "Qwen 16:9 Landscape (1664x928)": (1664, 928), "Qwen 9:16 Portrait (928x1664)": (928, 1664), "Qwen 4:3 Landscape (1472x1104)": (1472, 1104), "Qwen 3:4 Portrait (1104x1472)": (1104, 1472), "Qwen 3:2 Landscape (1584x1056)": (1584, 1056), "Qwen 2:3 Portrait (1056x1584)": (1056, 1584),
    # SDXL Resolutions
    "SDXL 1:1 Square (1024x1024)": (1024, 1024), "SDXL Portrait (896x1152)": (896, 1152), "SDXL Portrait (832x1216)": (832, 1216), "SDXL Portrait (768x1344)": (768, 1344), "SDXL Portrait (640x1536)": (640, 1536), "SDXL Landscape (1152x896)": (1152, 896), "SDXL Landscape (1216x832)": (1216, 832), "SDXL Landscape (1344x768)": (1344, 768), "SDXL Landscape (1536x640)": (1536, 640),
    # WAN Resolutions
    "WAN Square (512x512)": (512, 512), "WAN Square (768x768)": (768, 768), "WAN Square (960x960)": (960, 960), "WAN Square (1024x1024)": (1024, 1024), "WAN Square (2048x2048)": (2048, 2048), "WAN 16:9 Landscape (1280x720)": (1280, 720), "WAN 9:16 Portrait (720x1280)": (720, 1280), "WAN Portrait (832x1088)": (832, 1088), "WAN Landscape (1088x832)": (1088, 832),
}

class MultiAspectRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # We can now dynamically build the list with separators
        aspect_ratios = [
            "custom",
            "----- FLUX Resolutions -----",
            *[k for k in RESOLUTIONS if "FLUX" in k or "x" in k and "Qwen" not in k and "SDXL" not in k and "WAN" not in k], # A bit complex to keep it compatible
            "----- QWEN Resolutions -----",
            *[k for k in RESOLUTIONS if "Qwen" in k],
            "----- SDXL Resolutions -----",
            *[k for k in RESOLUTIONS if "SDXL" in k],
            "----- WAN Resolutions -----",
            *[k for k in RESOLUTIONS if "WAN" in k],
        ]
        return { "required": { "width": ("INT", {"default": 1024, "min": 64, "max": 8192}), "height": ("INT", {"default": 1024, "min": 64, "max": 8192}), "aspect_ratio": (aspect_ratios,), "swap_dimensions": (["Off", "On"],),"upscale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step":0.1}), "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}) } }
    
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "LATENT", )
    RETURN_NAMES = ("width", "height", "upscale_factor", "batch_size", "empty_latent", )
    FUNCTION = "Aspect_Ratio"
    CATEGORY = "My Nodes/Aspect Ratio"

    def Aspect_Ratio(self, width, height, aspect_ratio, swap_dimensions, upscale_factor, batch_size):
        # If a preset is chosen, overwrite the width and height.
        # Otherwise, the values from the input boxes are used.
        if aspect_ratio in RESOLUTIONS:
            width, height = RESOLUTIONS[aspect_ratio]
        
        # The swap logic remains the same.
        if swap_dimensions == "On":
            width, height = height, width
            
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        return(width, height, upscale_factor, batch_size, {"samples":latent}, )