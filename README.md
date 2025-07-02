# 🎨 Image Editor - Background Removal & Vectorization Tool

A powerful Python tool for removing backgrounds from images and converting them to vector formats (SVG).

## ✨ Features

- **AI-Powered Background Removal**: Uses the `rembg` library with neural networks to intelligently remove backgrounds
- **Image Vectorization**: Converts raster images to scalable SVG vector format
- **Color-Preserved Vectorization**: Creates SVG files while maintaining original colors
- **Complete Processing Pipeline**: One-click background removal + vectorization
- **Interactive CLI**: User-friendly command-line interface with emoji indicators
- **Multiple File Format Support**: JPG, PNG, BMP, TIFF, WebP

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Run the Image Editor
```bash
python src/main.py
```

### 3. Follow the Interactive Prompts
- Enter the path to your image file
- Choose from 5 processing options
- View results and process multiple images

## 📁 Project Structure

```
image-editor-project/
├── venv/                    # Virtual environment
├── src/
│   ├── main.py             # Main application entry point
│   ├── image_processor.py  # Main processing orchestrator
│   ├── background_remover.py # Background removal functionality
│   ├── vectorizer.py       # Image vectorization functionality
│   └── utils/
│       └── __init__.py
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

## 🔧 Processing Options

### 1. Remove Background Only
- Removes background using AI models
- Outputs: `image_no_bg.png`

### 2. Vectorize Image Only
- Converts image to SVG format
- Creates contour-based vector graphics
- Outputs: `image_vector.svg`

### 3. Remove Background + Vectorize
- Two-step process combining both operations
- Perfect for creating clean vector graphics

### 4. Vectorize with Colors
- Advanced vectorization preserving original colors
- Uses K-means clustering for color reduction
- Customizable color count (2-32 colors)
- Outputs: `image_color_vector.svg`

### 5. Complete Processing Pipeline
- Background removal → Vectorization
- Provides all intermediate and final files

## 🛠 Technical Details

### Background Removal
- **Library**: `rembg` (AI-powered background removal)
- **Models**: u2net (default), silueta, and others
- **Input**: Any common image format
- **Output**: PNG with transparent background

### Vectorization
- **Method**: OpenCV contour detection
- **Color Processing**: K-means clustering for color reduction
- **Output Format**: SVG (Scalable Vector Graphics)
- **Optimization**: Simplified paths for smaller file sizes

## 📦 Dependencies

Core libraries installed in the virtual environment:
- `Pillow` - Image processing
- `opencv-python` - Computer vision and contour detection
- `numpy` - Numerical computations
- `rembg` - AI background removal
- `scipy` - Scientific computing
- `matplotlib` - Plotting and visualization
- `scikit-image` - Image processing algorithms
- `scikit-learn` - Machine learning (K-means clustering)

## 🎯 Usage Examples

### Example 1: Basic Background Removal
```bash
python src/main.py
# Enter image path: /path/to/your/image.jpg
# Choose option: 1
# Result: image_no_bg.png
```

### Example 2: Colored Vectorization
```bash
python src/main.py
# Enter image path: /path/to/your/image.jpg
# Choose option: 4
# Enter colors: 12
# Result: image_color_vector.svg
```

## 🔍 File Output Naming

- Background removed: `originalname_no_bg.png`
- Vectorized: `originalname_vector.svg`
- Colored vectorized: `originalname_color_vector.svg`

## ⚡ Performance Tips

1. **Image Size**: Larger images take longer to process
2. **Background Complexity**: Complex backgrounds may require different models
3. **Color Count**: Fewer colors = faster vectorization, simpler SVG
4. **File Formats**: PNG recommended for transparency support

## 🐛 Troubleshooting

### Common Issues:
- **"File not found"**: Check file path and ensure file exists
- **"Unsupported format"**: Use JPG, PNG, BMP, TIFF, or WebP
- **Memory errors**: Try with smaller images or reduce color count
- **Slow processing**: Normal for large images; be patient

### Virtual Environment Issues:
```bash
# Reactivate environment
source venv/bin/activate

# Reinstall packages if needed
pip install -r requirements.txt
```

## 🎨 Tips for Best Results

1. **Background Removal**:
   - Use high-contrast images (subject vs background)
   - Avoid images where subject blends with background
   - Portrait photos work particularly well

2. **Vectorization**:
   - Simple images vectorize better than complex ones
   - Start with 8 colors and adjust as needed
   - Logos and graphics work excellently

3. **Complete Pipeline**:
   - Perfect for creating logos from photos
   - Great for t-shirt designs or print graphics
   - Ideal for web graphics that need to scale

## 📝 License

This project is for educational and personal use. Please respect the licenses of the underlying libraries.

---

Made with ❤️ using Python, OpenCV, and AI-powered background removal!