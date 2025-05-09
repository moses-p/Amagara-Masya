from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(filename='test_image.jpg', size=(800, 600), text="Test Image"):
    try:
        # Create a new image with a white background
        image = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(image)
        
        # Add some shapes
        draw.rectangle([100, 100, 700, 500], outline='blue', width=5)
        draw.ellipse([200, 200, 600, 400], fill='lightblue')
        
        # Add text with fallback fonts
        font = None
        font_sizes = [36, 24, 18]  # Try different sizes
        
        # Try different font paths
        font_paths = [
            "arial.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        
        for font_path in font_paths:
            try:
                for size in font_sizes:
                    try:
                        font = ImageFont.truetype(font_path, size)
                        break
                    except:
                        continue
                if font:
                    break
            except:
                continue
        
        if not font:
            font = ImageFont.load_default()
        
        # Calculate text position
        try:
            text_width = draw.textlength(text, font=font)
        except:
            text_width = len(text) * 20  # Rough estimate if textlength fails
        
        text_position = ((size[0] - text_width) // 2, size[1] // 2)
        draw.text(text_position, text, fill='black', font=font)
        
        # Save the image
        image.save(filename, 'JPEG', quality=95)
        print(f"✅ Created test image: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating test image: {str(e)}")
        return False

if __name__ == '__main__':
    create_test_image() 