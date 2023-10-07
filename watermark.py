import os, sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# transparency = 20

# watermark_file = Image.open("watermark.png")
# watermark_file2 = watermark_file.copy()
# watermark_file2.putalpha(int(255 * (transparency / 100)))
# watermark_file.paste(watermark_file2, watermark_file) # type: ignore

for file in os.listdir(sys.argv[1]):
  if file.lower().endswith(".jpg"):
    print(f"Processing '{file}'")

    # Open the original image
    original_image = Image.open(os.path.join(sys.argv[1], file))

    # Open the watermark image
    watermark_image = Image.open("watermark.png")

    # Calculate the scaling factor to maintain the aspect ratio
    width_ratio = original_image.width / watermark_image.width
    height_ratio = original_image.height / watermark_image.height
    scaling_factor = min(width_ratio, height_ratio)

    # Apply a scaling parameter (adjust as needed)
    scaling_parameter = 1 / scaling_factor  # Adjust the scale as a fraction (e.g., 0.5 for 50% scale)

    # if original_image.width > original_image.height:
    #   scaling_parameter = scaling_parameter / 2

    # Calculate the scaled dimensions of the watermark
    new_width = int(watermark_image.width * scaling_factor * scaling_parameter)
    new_height = int(watermark_image.height * scaling_factor * scaling_parameter)
    watermark_image = watermark_image.resize((new_width, new_height))

    # Calculate the position to center the watermark on the original image
    x_position = (original_image.width - watermark_image.width) - 100
    y_position = (original_image.height - watermark_image.height) - 100

    # Adjust the opacity of the watermark by modifying the alpha channel
    watermark_image = watermark_image.convert("RGBA")
    watermark_data = watermark_image.getdata()
    watermark_data_with_opacity = [(r, g, b, int(a * 0.9)) for r, g, b, a in watermark_data]
    watermark_image.putdata(watermark_data_with_opacity)

    # Create a transparent watermark image with the same size as the original
    watermark = Image.new("RGBA", original_image.size)
    watermark.paste(watermark_image, (x_position, y_position), watermark_image)

    # Blend the original image and watermark
    watermarked_image = Image.alpha_composite(original_image.convert("RGBA"), watermark)

    # Save the watermarked image
    watermarked_path = f"{sys.argv[1]}/watermarked"
    if not os.path.exists(watermarked_path):
      os.mkdir(watermarked_path)
    watermarked_image.convert("RGB").save(f"{watermarked_path}/{file}", "JPEG")