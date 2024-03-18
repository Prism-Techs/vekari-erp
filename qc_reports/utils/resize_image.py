
from PIL import Image as PILImage

def resize_to_image(image_path, output_path, new_width, new_height):
    image = PILImage.open(image_path)
    original_width, original_height = image.size
    
    # Calculate padding sizes
    left = (new_width - original_width) // 2
    top = (new_height - original_height) // 2
    right = new_width - original_width - left
    bottom = new_height - original_height - top
    
    # Add padding
    new_image = PILImage.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    new_image.paste(image, (left, top))
    
    new_image.save(output_path, format="PNG")
    return new_image

# image=resize_to_image(logo_path,output_path,350,100)
