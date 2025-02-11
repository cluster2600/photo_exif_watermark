# Image Watermark and Frame Processor

This Python program adds a consistent white border and a handwritten-style watermark signature to images exported from Apple Photos. It ensures that each image gets a border that is exactly 2 cm wide (in physical size) by using a constant target DPI (set to 300 DPI by default). The program supports common image formats (JPG, JPEG, PNG, HEIC) and also processes RAW DNG files (using rawpy) by converting them to JPEGs with a "_watermarked.jpg" suffix.

## Features

- **Consistent Border Size:** A white border of 2 cm is added to each image, calculated using a fixed target DPI to maintain uniformity.
- **Watermark Signature:** A handwritten-style watermark (e.g., "Maxime Grenu") is added in black at the bottom-right.
- **Supports Multiple Formats:** Supports JPG, JPEG, PNG, HEIC (via `pillow-heif`) and DNG (via `rawpy`).
- **DPI-Based Border Calculation:** The script ensures the physical border size remains 2 cm across images of different resolutions by using a fixed target DPI.
- **Manual Orientation Handling:** No automatic rotation is applied; you must correct image orientation manually if needed.

## Requirements

- Python 3.x
- Dependencies: Pillow, pillow-heif, rawpy

## Installation

Install the required modules in your virtual environment using pip:

```bash
pip install pillow pillow-heif rawpy
```

## How It Works

1. **Border Calculation:**  
   The border width in pixels is calculated as:

   ```python
   border_pixels = (target_dpi / 2.54) * 2
   ```

   At 300 DPI, this results in approximately 236 pixels, ensuring a 2 cm border.

2. **Processing Workflow:**
   - Loads the image without modifying its orientation.
   - Reads DPI metadata from the image; if unavailable, it defaults to 300 DPI.
   - Adds a white border of the computed width.
   - Incrusts the watermark signature in the bottom-right corner using the MarkerFelt font (rendered in black).
   - Saves the image with the DPI information set to the target DPI.
   - **For DNG files:** Converts the RAW file to an RGB image using rawpy, applies the border and watermark, and saves the result as a JPEG with a “_watermarked.jpg” suffix.

## Usage

Place the exported images in a directory (e.g., `/Volumes/backup`) and run the script:

```bash
python incrust.py
```

The script will process all supported images in the specified directory, adding a consistent white border and your watermark signature.

## Customization

- **Signature Text:** Modify the signature variable in the script to change the watermark text.
- **Border Size:** Adjust the `border_pixels` calculation or the `target_dpi` value to change the physical size of the border.
- **Font Selection:** The script uses the MarkerFelt font located at `/System/Library/Fonts/Supplemental/MarkerFelt.ttc`. You can change the font by updating the path and size in the `ImageFont.truetype()` call.

## License

This program is provided “as is” without any warranty. Use it at your own risk.
