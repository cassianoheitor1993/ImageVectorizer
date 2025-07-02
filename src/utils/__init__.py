"""
Image Editor Utilities Module
Shared utilities for image processing operations
"""

__version__ = "1.0.0"
__author__ = "Image Editor"

# Common image file extensions
SUPPORTED_IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'
}

def is_image_file(file_path):
    """Check if file has a supported image extension"""
    import os
    _, ext = os.path.splitext(file_path.lower())
    return ext in SUPPORTED_IMAGE_EXTENSIONS