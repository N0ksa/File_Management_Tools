from PIL import Image, ImageEnhance

def preprocess_image(image: Image) -> Image:
    image = image.convert('L')  # Pretvorite sliku u crno-bijelu
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Poboljšajte kontrast
    return image
