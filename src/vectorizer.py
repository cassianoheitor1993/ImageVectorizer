import cv2
import numpy as np
from PIL import Image
from skimage import measure, morphology
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches

class Vectorizer:
    def __init__(self):
        """Initialize the vectorizer"""
        pass
    
    def vectorize(self, input_path, output_path):
        """
        Convert image to vector format (SVG)
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save SVG output
            
        Returns:
            str: Path to the vectorized image
        """
        try:
            # Load and preprocess image
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Convert to grayscale for contour detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Create SVG content
            svg_content = self._create_svg_from_contours(contours, image.shape)
            
            # Save SVG file
            with open(output_path, 'w') as f:
                f.write(svg_content)
            
            print(f"Image vectorized successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error vectorizing image: {str(e)}")
            raise
    
    def vectorize_hq(self, input_path, output_path, detail_level='high'):
        """
        High-quality vectorization with enhanced detail preservation
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save SVG output
            detail_level (str): 'low', 'medium', 'high', 'ultra'
            
        Returns:
            str: Path to the vectorized image
        """
        try:
            # Load image with high quality
            image = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Set parameters based on detail level
            params = self._get_detail_params(detail_level)
            
            # Apply preprocessing for better edge detection
            processed_image = self._preprocess_for_vectorization(image, params)
            
            # Convert to grayscale with weighted channels for better contrast
            gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive threshold for better edge detection
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, params['adaptive_block_size'], params['adaptive_c']
            )
            
            # Apply morphological operations to clean up the binary image
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
            
            # Find contours with hierarchy for nested shapes
            contours, hierarchy = cv2.findContours(
                binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1
            )
            
            # Filter and simplify contours based on detail level
            filtered_contours = self._filter_and_simplify_contours(contours, params)
            
            # Create high-quality SVG content
            svg_content = self._create_hq_svg_from_contours(
                filtered_contours, image.shape, hierarchy, params
            )
            
            # Save SVG file
            with open(output_path, 'w') as f:
                f.write(svg_content)
            
            print(f"✅ High-quality vectorization completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error in HQ vectorization: {str(e)}")
            raise
    
    def _get_detail_params(self, detail_level):
        """Get parameters based on detail level"""
        params = {
            'low': {
                'blur_kernel': (5, 5),
                'adaptive_block_size': 11,
                'adaptive_c': 2,
                'min_contour_area': 100,
                'epsilon_factor': 0.02,
                'smooth_factor': 2.0
            },
            'medium': {
                'blur_kernel': (3, 3),
                'adaptive_block_size': 9,
                'adaptive_c': 2,
                'min_contour_area': 50,
                'epsilon_factor': 0.01,
                'smooth_factor': 1.5
            },
            'high': {
                'blur_kernel': (3, 3),
                'adaptive_block_size': 7,
                'adaptive_c': 1,
                'min_contour_area': 25,
                'epsilon_factor': 0.005,
                'smooth_factor': 1.0
            },
            'ultra': {
                'blur_kernel': (1, 1),
                'adaptive_block_size': 5,
                'adaptive_c': 1,
                'min_contour_area': 10,
                'epsilon_factor': 0.002,
                'smooth_factor': 0.5
            }
        }
        return params.get(detail_level, params['high'])
    
    def _preprocess_for_vectorization(self, image, params):
        """Preprocess image for better vectorization"""
        # Apply slight blur to reduce noise while preserving edges
        blurred = cv2.GaussianBlur(image, params['blur_kernel'], 0)
        
        # Enhance contrast using CLAHE
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def _filter_and_simplify_contours(self, contours, params):
        """Filter contours by area and simplify them"""
        filtered = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= params['min_contour_area']:
                # Simplify contour using Douglas-Peucker algorithm
                epsilon = params['epsilon_factor'] * cv2.arcLength(contour, True)
                simplified = cv2.approxPolyDP(contour, epsilon, True)
                filtered.append(simplified)
        
        return filtered
    
    def _create_hq_svg_from_contours(self, contours, image_shape, hierarchy, params):
        """Create high-quality SVG content from contours"""
        height, width = image_shape[:2]
        
        # Create SVG header with high DPI
        svg_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
  <style>
    .shape {{ fill: black; stroke: black; stroke-width: 0.5; stroke-linejoin: round; stroke-linecap: round; }}
  </style>
</defs>
'''
        
        svg_paths = ""
        for i, contour in enumerate(contours):
            if len(contour) >= 3:  # Only process contours with enough points
                path_data = self._create_smooth_path(contour, params['smooth_factor'])
                svg_paths += f'  <path d="{path_data}" class="shape"/>\n'
        
        svg_footer = "</svg>"
        
        return svg_header + svg_paths + svg_footer
    
    def _create_smooth_path(self, contour, smooth_factor):
        """Create smooth SVG path with curves"""
        if len(contour) < 3:
            return ""
        
        points = contour.reshape(-1, 2)
        
        # Start path
        path_data = f"M {points[0][0]},{points[0][1]}"
        
        # Create smooth curves using quadratic Bézier curves
        for i in range(1, len(points)):
            curr_point = points[i]
            
            if i < len(points) - 1 and smooth_factor > 0:
                next_point = points[i + 1]
                # Calculate control point for smooth curve
                control_x = curr_point[0] + (next_point[0] - curr_point[0]) * 0.5
                control_y = curr_point[1] + (next_point[1] - curr_point[1]) * 0.5
                path_data += f" Q {curr_point[0]},{curr_point[1]} {control_x},{control_y}"
            else:
                path_data += f" L {curr_point[0]},{curr_point[1]}"
        
        path_data += " Z"
        return path_data

    def vectorize_with_colors(self, input_path, output_path, num_colors=8):
        """
        Convert image to vector format with color preservation
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save SVG output
            num_colors (int): Number of colors to use in vectorization
            
        Returns:
            str: Path to the vectorized image
        """
        try:
            # Load image
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Reduce colors using K-means clustering
            reduced_image = self._reduce_colors(image_rgb, num_colors)
            
            # Create SVG with color regions
            svg_content = self._create_colored_svg(reduced_image)
            
            # Save SVG file
            with open(output_path, 'w') as f:
                f.write(svg_content)
            
            print(f"Colored image vectorized successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error vectorizing colored image: {str(e)}")
            raise
    
    def vectorize_with_colors_hq(self, input_path, output_path, num_colors=8, detail_level='high'):
        """
        High-quality colored vectorization with enhanced detail preservation
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save SVG output
            num_colors (int): Number of colors to use
            detail_level (str): Detail level for processing
            
        Returns:
            str: Path to the vectorized image
        """
        try:
            # Load image with high quality
            image = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get detail parameters
            params = self._get_detail_params(detail_level)
            
            # Preprocess image for better color quantization
            processed_image = self._preprocess_for_vectorization(image, params)
            processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            # Reduce colors using improved K-means clustering
            reduced_image = self._reduce_colors_hq(processed_rgb, num_colors)
            
            # Create high-quality SVG with color regions
            svg_content = self._create_colored_svg_hq(reduced_image, params)
            
            # Save SVG file
            with open(output_path, 'w') as f:
                f.write(svg_content)
            
            print(f"✅ High-quality colored vectorization completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error in HQ colored vectorization: {str(e)}")
            raise
    
    def _reduce_colors_hq(self, image, num_colors):
        """Improved color reduction using K-means with better initialization"""
        from sklearn.cluster import KMeans
        
        # Reshape image to be a list of pixels
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        # Use K-means++ initialization for better clustering
        kmeans = KMeans(
            n_clusters=num_colors, 
            init='k-means++', 
            n_init=20, 
            max_iter=300,
            random_state=42
        )
        
        # Fit and predict
        labels = kmeans.fit_predict(data)
        centers = kmeans.cluster_centers_
        
        # Convert back to uint8 and reshape
        centers = np.uint8(centers)
        reduced_data = centers[labels]
        reduced_image = reduced_data.reshape(image.shape)
        
        return reduced_image
    
    def _create_colored_svg_hq(self, image, params):
        """Create high-quality SVG with color regions and smooth edges"""
        height, width = image.shape[:2]
        
        svg_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
  <style>
    .color-region {{ stroke-width: 0.3; stroke-linejoin: round; stroke-linecap: round; }}
  </style>
</defs>
'''
        
        svg_content = ""
        
        # Get unique colors
        unique_colors = np.unique(image.reshape(-1, 3), axis=0)
        
        for color in unique_colors:
            # Create mask for this color
            mask = np.all(image == color, axis=2)
            
            # Apply morphological operations to clean up the mask
            mask_uint8 = mask.astype(np.uint8) * 255
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask_cleaned = cv2.morphologyEx(mask_uint8, cv2.MORPH_CLOSE, kernel)
            mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)
            
            # Find contours for this color
            contours, _ = cv2.findContours(
                mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1
            )
            
            # Convert color to hex
            color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            # Add paths for this color with area filtering
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= params['min_contour_area']:
                    # Simplify contour
                    epsilon = params['epsilon_factor'] * cv2.arcLength(contour, True)
                    simplified = cv2.approxPolyDP(contour, epsilon, True)
                    
                    if len(simplified) >= 3:
                        path_data = self._create_smooth_path(simplified, params['smooth_factor'])
                        svg_content += f'  <path d="{path_data}" fill="{color_hex}" stroke="{color_hex}" class="color-region"/>\n'
        
        svg_footer = "</svg>"
        
        return svg_header + svg_content + svg_footer