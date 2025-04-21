#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "cairosvg>=2.5.2",
#   "Pillow>=9.0.0",
# ]
# ///

"""
SVG to Favicon Converter

This script converts an SVG file to a multi-size favicon (.ico) file,
as well as generating individual PNG files that can be used for different devices.


    uv run scripts/svg_to_fav.py your_logo.svg -o /path/to/output


Requirements:
    - ImageMagick installed on the system
    - uv package manager (https://github.com/astral-sh/uv)

The script will create:
    - favicon.ico (multi-resolution icon file)
    - apple-touch-icon.png (180x180 for iOS)
    - android-chrome-192x192.png
    - android-chrome-512x512.png
    - favicon-16x16.png
    - favicon-32x32.png
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

# Since we're using script-level dependencies with uv,
# these imports should be available
import cairosvg
from PIL import Image

def check_imagemagick():
    """Check if ImageMagick is installed."""
    try:
        subprocess.run(["convert", "--version"], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def svg_to_png(svg_path, png_path, width, height):
    """Convert SVG to PNG at specified dimensions."""
    try:
        # Convert Path objects to strings for cairosvg
        svg_path_str = str(svg_path)
        png_path_str = str(png_path)
        
        cairosvg.svg2png(url=svg_path_str, 
                        write_to=png_path_str, 
                        output_width=width, 
                        output_height=height)
        return png_path
    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        return None

def create_favicon_ico(png_files, output_path):
    """Create a multi-size .ico file from a list of PNG files."""
    # Sort files by size for better organization
    png_files.sort(key=lambda x: os.path.getsize(x))
    
    # Build the ImageMagick convert command
    cmd = ["convert"] + png_files + [output_path]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Created favicon: {output_path}")
        return True
    except subprocess.SubprocessError as e:
        print(f"Error creating favicon: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert SVG to favicon")
    parser.add_argument("svg_file", help="Input SVG file")
    parser.add_argument("-o", "--output-dir", 
                        default=".", 
                        help="Output directory (default: current directory)")
    
    args = parser.parse_args()
    
    # Check if ImageMagick is installed
    if not check_imagemagick():
        print("Error: ImageMagick is not installed or not in PATH.")
        print("Please install ImageMagick and ensure 'convert' is available.")
        sys.exit(1)
    
    svg_path = args.svg_file
    output_dir = Path(args.output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the sizes to generate
    sizes = {
        "favicon-16x16.png": (16, 16),
        "favicon-32x32.png": (32, 32),
        "apple-touch-icon.png": (180, 180),
        "android-chrome-192x192.png": (192, 192),
        "android-chrome-512x512.png": (512, 512),
    }
    
    # Generate PNG files for each size
    temp_files = []
    output_files = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename, (width, height) in sizes.items():
            output_path = output_dir / filename
            png_path = svg_to_png(svg_path, output_path, width, height)
            
            if png_path:
                output_files.append(output_path)
                print(f"Created {filename}")
                
                # For favicon.ico, we need specific sizes
                if filename in ["favicon-16x16.png", "favicon-32x32.png"]:
                    temp_path = Path(temp_dir) / filename
                    temp_png = svg_to_png(svg_path, temp_path, width, height)
                    if temp_png:
                        temp_files.append(temp_path)
        
        # Create favicon.ico using the relevant temp files
        if temp_files:
            favicon_path = output_dir / "favicon.ico"
            create_favicon_ico(list(map(str, temp_files)), str(favicon_path))
    
    print("\nDone! Generated favicon files:")
    for f in output_files:
        print(f"- {f}")
    print(f"- {output_dir}/favicon.ico")
    
    print("\nHTML code to include:")
    print('<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">')
    print('<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">')
    print('<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">')
    print('<link rel="icon" href="/favicon.ico">')

if __name__ == "__main__":
    main()
