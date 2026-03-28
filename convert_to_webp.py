#!/usr/bin/env python3
"""
Batch convert PNG resources to WebP format
- Spritesheets use lossless conversion
- Backgrounds use lossy conversion (quality 85)
"""

import os
from PIL import Image

# Paths
FRONTEND_DIR = "/root/.openclaw/workspace/star-office-ui/frontend"
STATIC_DIR = os.path.join(FRONTEND_DIR, "")

# File classification configuration
# Lossless conversion: spritesheets, needs to maintain transparency precision
LOSSLESS_FILES = [
    "star-idle-spritesheet.png",
    "star-researching-spritesheet.png",
    "star-working-spritesheet.png",
    "sofa-busy-spritesheet.png",
    "plants-spritesheet.png",
    "posters-spritesheet.png",
    "coffee-machine-spritesheet.png",
    "serverroom-spritesheet.png"
]

# Lossy conversion: backgrounds, quality 85
LOSSY_FILES = [
    "office_bg.png",
    "sofa-idle.png",
    "desk.png"
]


def convert_to_webp(input_path, output_path, lossless=True, quality=85):
    """Convert a single file to WebP"""
    try:
        img = Image.open(input_path)
        
        # Save as WebP
        if lossless:
            img.save(output_path, 'WebP', lossless=True, method=6)
        else:
            img.save(output_path, 'WebP', quality=quality, method=6)
        
        # Calculate file size
        orig_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        savings = (1 - new_size / orig_size) * 100
        
        print(f"✅ {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        print(f"   Original size: {orig_size/1024:.1f}KB -> New size: {new_size/1024:.1f}KB (-{savings:.1f}%)")
        
        return True
    except Exception as e:
        print(f"❌ {os.path.basename(input_path)} conversion failed: {e}")
        return False


def main():
    print("=" * 60)
    print("PNG → WebP Batch Conversion Tool")
    print("=" * 60)
    
    # Check directory
    if not os.path.exists(STATIC_DIR):
        print(f"❌ Directory does not exist: {STATIC_DIR}")
        return
    
    success_count = 0
    fail_count = 0
    
    print("\n📁 Starting conversion...\n")
    
    # Convert lossless files
    print("--- Lossless conversion (Spritesheets) ---")
    for filename in LOSSLESS_FILES:
        input_path = os.path.join(STATIC_DIR, filename)
        if not os.path.exists(input_path):
            print(f"⚠️  File does not exist, skipping: {filename}")
            continue
        
        output_path = os.path.join(STATIC_DIR, filename.replace(".png", ".webp"))
        if convert_to_webp(input_path, output_path, lossless=True):
            success_count += 1
        else:
            fail_count += 1
    
    # Convert lossy files
    print("\n--- Lossy conversion (Backgrounds, quality 85) ---")
    for filename in LOSSY_FILES:
        input_path = os.path.join(STATIC_DIR, filename)
        if not os.path.exists(input_path):
            print(f"⚠️  File does not exist, skipping: {filename}")
            continue
        
        output_path = os.path.join(STATIC_DIR, filename.replace(".png", ".webp"))
        if convert_to_webp(input_path, output_path, lossless=False, quality=85):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"Conversion complete! Success: {success_count}, Failed: {fail_count}")
    print("=" * 60)
    print("\n📝 Note:")
    print("  - Original PNG files are kept, not deleted")
    print("  - You need to modify the frontend code to reference .webp files")
    print("  - If rollback is needed, simply change the code back to reference .png")


if __name__ == "__main__":
    main()
