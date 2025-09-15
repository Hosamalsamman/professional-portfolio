import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import math

img_path = ""
lg_path = ""
logo_text = ""


def open_files(type):
    global img_path, lg_path  # declare first
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")]
    )
    if file_path:
        if type == "img":
            img_path = file_path
        elif type == "logo":
            lg_path = file_path
        print("You selected:", file_path)
    else:
        print("No file selected.")


def save_logo_text():
    global logo_text
    logo_text = w_m_entry.get()
    print(logo_text)


def apply_watermark(image_path, logo_path, watermark_text, spacing, output_path="watermarked_image.png"):
    # Open the main image
    base_img = Image.open(image_path).convert("RGBA")

    # Make a copy so we don’t overwrite the original
    watermark_img = base_img.copy()

    # Create a drawing context
    draw = ImageDraw.Draw(watermark_img)

    # Load font
    font = ImageFont.truetype("arial.ttf", 30)

    # Get text size
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Loop through image and draw text repeatedly
    for y in range(0, base_img.height, text_height + spacing):
        for x in range(0, base_img.width, text_width + spacing):
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 100))  # white, semi-transparent

    # --- Optional: Add logo ---
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((100, 100))
        position = (20, 20)
        watermark_img.paste(logo, position, logo)

    # Save watermarked image
    watermark_img.save(output_path)
    print(f"✅ Watermarked image saved at {output_path}")


def apply_watermark_optimized(image_path, logo_path, watermark_text, spacing, rotation_angle,
                              output_path="watermarked_image.png"):

    # Open the main image
    base_img = Image.open(image_path).convert("RGBA")
    watermark_img = base_img.copy()

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except OSError:
        font = ImageFont.load_default()

    # Get text dimensions
    bbox = font.getbbox(watermark_text)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate diagonal dimensions for rotated text
    if rotation_angle != 0:
        angle_rad = math.radians(rotation_angle)
        diagonal_width = abs(text_width * math.cos(angle_rad)) + abs(text_height * math.sin(angle_rad))
        diagonal_height = abs(text_width * math.sin(angle_rad)) + abs(text_height * math.cos(angle_rad))
    else:
        diagonal_width, diagonal_height = text_width, text_height

    # Create pattern with rotated text
    step_x = int(diagonal_width + spacing)
    step_y = int(diagonal_height + spacing)

    for y in range(-step_y, base_img.height + step_y, step_y):
        for x in range(-step_x, base_img.width + step_x, step_x):
            # Create text image
            text_img = Image.new('RGBA', (text_width + 40, text_height + 40), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((10, 10), watermark_text, font=font, fill=(255, 255, 255, 100))

            if rotation_angle != 0:
                text_img = text_img.rotate(rotation_angle, expand=True)

            # Paste with transparency
            watermark_img.paste(text_img, (x, y), text_img)

    # Add logo with transparent background
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")

            # Make white/light backgrounds transparent (if needed)
            # Uncomment this section if your logo has a white background to remove:
            logo_data = logo.getdata()
            new_logo_data = []
            for item in logo_data:
                # Change white (255,255,255) pixels to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:  # Close to white
                    new_logo_data.append((255, 255, 255, 0))  # Transparent
                else:
                    new_logo_data.append(item)
            logo.putdata(new_logo_data)

            # Resize logo
            logo.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Position logo (you can change this)
            position = (20, 20)
            watermark_img.paste(logo, position, logo)

        except Exception as e:
            print(f"⚠️ Error adding logo: {e}")

    # Save as PNG to preserve transparency
    watermark_img.save(output_path, "PNG")
    print(f"✅ Watermarked image saved at {output_path}")


def watermark_with_blend(image_path, logo_path, text, angle, alpha, spacing=200, output_path="watermarked_image.png"):
    # Open original
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    # Create overlay (transparent initially)
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 80))

    # Font
    font = ImageFont.truetype("arial.ttf", 80)

    # Draw repeated watermark text
    for y in range(0, height, spacing):
        for x in range(0, width, spacing):
            # Create a minimal canvas just for the text
            dummy_img = Image.new("RGBA", (1, 1))
            dummy_draw = ImageDraw.Draw(dummy_img)
            bbox = dummy_draw.textbbox((0, 0), text, font=font)
            text_size = ((bbox[2] - bbox[0]) + 1, (bbox[3] - bbox[1]) + 1)

            text_img = Image.new("RGBA", text_size, (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((0, 0), text, font=font, fill=(125, 125, 125, 100))

            # Rotate if needed
            if angle != 0:
                text_img = text_img.rotate(angle, expand=True)

            # Only paste if inside bounds
            if x + text_img.width <= width and y + text_img.height <= height:
                overlay.paste(text_img, (x, y), text_img)

    # Blend images
    watermarked = Image.blend(img, overlay, alpha=alpha)

    # Add logo if provided
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")

            # Make white close to transparent
            logo_data = logo.getdata()
            new_logo_data = []
            for item in logo_data:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:  # almost white
                    new_logo_data.append((255, 255, 255, 0))
                else:
                    new_logo_data.append(item)
            logo.putdata(new_logo_data)

            # Resize logo
            logo.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Position logo (top-left here, can be changed)
            position = (20, 20)
            watermarked.paste(logo, position, logo)

        except Exception as e:
            print(f"⚠️ Error adding logo: {e}")

    # Save
    watermarked.save(output_path, "PNG")
    print(f"✅ Watermarked image saved at {output_path}")

window = tk.Tk()
window.title("💧 Watermarker")
window.config(padx=40, pady=30, bg="#f0f8ff")  # light aqua background

# --------- STYLES ----------
# Shared style settings for buttons
BTN_STYLE = {
    "font": ("Arial", 12, "bold"),   # Font family, size, and weight
    "bg": "#4682B4",                 # Button background color (steel blue)
    "fg": "white",                   # Button text color (foreground)
    "activebackground": "#5A9BD5",   # Background when button is pressed/hovered
    "activeforeground": "green",     # Text color when button is pressed/hovered
    "relief": "raised",              # Button border style (flat, raised, sunken, groove, ridge)
    "bd": 3,                         # Border thickness in pixels
    "width": 20,                     # Button width in text units (approx. characters)
    "height": 2                      # Button height in text units (approx. text rows)
}

# Shared style settings for labels
LBL_STYLE = {
    "font": ("Arial", 14),           # Font family and size
    "bg": "#f0f8ff",                 # Label background color (Alice blue)
    "fg": "#333333"                  # Label text color (dark gray)
}

# --------- HEADER ----------
header = tk.Label(window, text="✨ Watermark Your Images ✨",
                  font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#2F4F4F")
header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# --------- IMAGE SELECTION ----------
img_label = tk.Label(window, text="Step 1: Select an image", **LBL_STYLE)
img_label.grid(row=1, column=0, sticky="w", pady=(5, 5))

add_img = tk.Button(window, text="📂 Add Image", command=lambda: open_files("img"), **BTN_STYLE)
add_img.grid(row=1, column=1, padx=10, pady=5)

# --------- TEXT INPUT ----------
txt_label = tk.Label(window, text="Step 2: Enter watermark text", **LBL_STYLE)
txt_label.grid(row=2, column=0, sticky="w", pady=(15, 5))

w_m_entry = tk.Entry(window, width=30, fg="black", bg="white",
                     font=("Arial", 16), justify="center")
w_m_entry.grid(row=2, column=1, padx=10, pady=5)

save_logo_text_btn = tk.Button(window, text="💾 Save Text", command=save_logo_text, **BTN_STYLE)
save_logo_text_btn.grid(row=3, column=1, padx=10, pady=5)

# --------- LOGO SELECTION ----------
logo_label = tk.Label(window, text="Step 3: Select a logo (optional)", **LBL_STYLE)
logo_label.grid(row=4, column=0, sticky="w", pady=(15, 5))

w_m_logo = tk.Button(window, text="🖼 Select Logo", command=lambda: open_files("logo"), **BTN_STYLE)
w_m_logo.grid(row=4, column=1, padx=10, pady=5)

# --------- APPLY BUTTON ----------
apply = tk.Button(window, text="🚀 Apply Watermark",
                  command=lambda: apply_watermark_optimized(img_path, lg_path, logo_text, 300, 45),
                  **BTN_STYLE)
apply.config(width=25, height=2, bg="#228B22", activebackground="#32CD32")  # green for action
apply.grid(row=5, column=0, columnspan=2, pady=(30, 10))

# --------- FOOTER ----------
footer = tk.Label(window, text="© 2025 Watermarker App", bg="#f0f8ff", fg="#666",
                  font=("Arial", 10))
footer.grid(row=6, column=0, columnspan=2, pady=(20, 0))

window.mainloop()
