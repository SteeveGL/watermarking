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

    ## Copyright ##
    # Open the watermark image
    watermark_image = Image.open("watermark.png")

    # Calculate the scaling factor to maintain the aspect ratio
    width_ratio = original_image.width / watermark_image.width
    height_ratio = original_image.height / watermark_image.height
    scaling_factor = min(width_ratio, height_ratio)

    # Apply a scaling parameter (adjust as needed)
    scaling_parameter = 0.5  # Adjust the scale as a fraction (e.g., 0.5 for 50% scale)

    # Calculate the scaled dimensions of the watermark
    new_width = int(watermark_image.width * scaling_factor * scaling_parameter)
    new_height = int(watermark_image.height * scaling_factor * scaling_parameter)
    watermark_image = watermark_image.resize((new_width, new_height))

    # Calculate the position to center the watermark on the original image
    x_position = (original_image.width - watermark_image.width) // 2
    y_position = (original_image.height - watermark_image.height) // 2

    # Adjust the opacity of the watermark by modifying the alpha channel
    watermark_image = watermark_image.convert("RGBA")
    watermark_data = watermark_image.getdata()
    watermark_data_with_opacity = [(r, g, b, int(a * 0.6)) for r, g, b, a in watermark_data]
    watermark_image.putdata(watermark_data_with_opacity)

    # Create a transparent watermark image with the same size as the original
    watermark = Image.new("RGBA", original_image.size)
    watermark.paste(watermark_image, (x_position, y_position), watermark_image)

    # Blend the original image and watermark
    watermarked_image = Image.alpha_composite(original_image.convert("RGBA"), watermark)

    # Get the dimensions of the watermarked image
    image_width, image_height = watermarked_image.size

    # Determine the font size based on the image size (adjust as needed)
    font_size = int(min(image_width, image_height) * 0.05)  # 5% of image size

    # Create a font with the determined size
    font = ImageFont.truetype("Rapscallion-q341.ttf", size=font_size)

    # Get the filename without the file extension
    filename = os.path.splitext(file)[0]  # Replace "original.jpg" with your actual filename

    # Add the filename at the bottom of the image with 50% transparency
    draw = ImageDraw.Draw(watermarked_image)

    # Calculate the text dimensions and position
    text = f"# {filename.replace("IMG_", "")} #"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (image_width - text_width) // 2
    text_y = image_height - text_height - 100  # Adjust the position as needed

    # Define the text colors
    text_color = (255, 255, 255, 200)  # RGBA color with 50% transparency
    border_color = (0, 0, 0, 128)  # RGBA color for the black border

    # Draw the black border
    border_width = 5  # Adjust the border width as needed
    for i in range(-border_width, border_width + 1):
        for j in range(-border_width, border_width + 1):
            draw.text((text_x + i, text_y + j), text, font=font, fill=border_color)

    # Draw the actual text on top of the border
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Save the watermarked image
    copyrighted_path = f"{sys.argv[1]}/copyrighted"
    if not os.path.exists(copyrighted_path):
      os.mkdir(copyrighted_path)
    watermarked_image.convert("RGB").save(f"{copyrighted_path}/{file}", "JPEG")

    ## Watermarked ##
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