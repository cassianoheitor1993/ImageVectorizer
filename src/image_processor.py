import os
from pathlib import Path
from background_remover import BackgroundRemover
from vectorizer import Vectorizer

class ImageProcessor:
    def __init__(self):
        self.bg_remover = BackgroundRemover()
        self.vectorizer = Vectorizer()
    
    def remove_background(self, image_path):
        """Remove background from an image using AI"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create output filename
        input_path = Path(image_path)
        output_path = input_path.parent / f"{input_path.stem}_no_bg{input_path.suffix}"
        
        # Remove background
        result_path = self.bg_remover.remove_background(image_path, str(output_path))
        return result_path
    
    def remove_background_smart(self, image_path):
        """Smart background removal with color detection and suggestions"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Use the enhanced background removal with suggestions
        results = self.bg_remover.remove_background_with_suggestions(image_path)
        return results
    
    def vectorize_image(self, image_path, quality='standard'):
        """Convert image to vector format"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create output filename for SVG
        input_path = Path(image_path)
        
        if quality == 'high':
            output_path = input_path.parent / f"{input_path.stem}_vector_hq.svg"
            result_path = self.vectorizer.vectorize_hq(image_path, str(output_path), 'high')
        elif quality == 'ultra':
            output_path = input_path.parent / f"{input_path.stem}_vector_ultra.svg"
            result_path = self.vectorizer.vectorize_hq(image_path, str(output_path), 'ultra')
        else:
            output_path = input_path.parent / f"{input_path.stem}_vector.svg"
            result_path = self.vectorizer.vectorize(image_path, str(output_path))
        
        return result_path
    
    def vectorize_with_colors_hq(self, image_path, num_colors=8, quality='high'):
        """High-quality colored vectorization"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        input_path = Path(image_path)
        output_path = input_path.parent / f"{input_path.stem}_color_vector_hq.svg"
        
        result_path = self.vectorizer.vectorize_with_colors_hq(
            image_path, str(output_path), num_colors, quality
        )
        return result_path
    
    def process_complete_hq(self, image_path):
        """Complete high-quality processing: smart background removal + vectorization"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # First do smart background removal
        bg_results = self.remove_background_smart(image_path)
        
        if not bg_results or not bg_results.get('processed'):
            return {'error': 'No background removal results'}
        
        # Vectorize the best result (first processed image)
        best_bg_removed = bg_results['processed'][0]['path']
        vector_path = self.vectorize_image(best_bg_removed, quality='high')
        
        return {
            'original': image_path,
            'background_removal_results': bg_results,
            'final_vector': vector_path
        }
    
    def remove_color_background_interactive(self, image_path):
        """Interactive color-based background removal"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create output filename
        input_path = Path(image_path)
        output_path = input_path.parent / f"{input_path.stem}_color_bg_removed.png"
        
        # Use interactive color removal
        result_path = self.bg_remover.remove_background_interactive(image_path, str(output_path))
        return result_path
    
    def remove_color_background(self, image_path, target_color='white', tolerance=30):
        """Remove background based on specific color"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create output filename
        input_path = Path(image_path)
        color_name = target_color if isinstance(target_color, str) else f"rgb_{target_color[0]}_{target_color[1]}_{target_color[2]}"
        output_path = input_path.parent / f"{input_path.stem}_{color_name}_removed.png"
        
        # Remove color background
        result_path = self.bg_remover.remove_color_background(image_path, str(output_path), target_color, tolerance)
        return result_path