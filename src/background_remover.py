import os
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from rembg import remove
from collections import Counter
from sklearn.cluster import KMeans
import warnings

class BackgroundRemover:
    def __init__(self):
        """Initialize the background remover"""
        # Suppress sklearn warnings for cleaner output
        warnings.filterwarnings('ignore', category=RuntimeWarning, module='sklearn')
        pass
    
    def remove_background(self, input_path, output_path):
        """
        Remove background from an image using rembg (AI-based)
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save output image
            
        Returns:
            str: Path to the processed image
        """
        try:
            # Read input image
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background
            output_data = remove(input_data)
            
            # Save the result
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            print(f"AI background removal completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error removing background: {str(e)}")
            raise
    
    def remove_color_background(self, input_path, output_path, target_color='white', tolerance=30):
        """
        Remove background based on specific color
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save output image
            target_color (str or tuple): Color to remove ('white', 'black', or RGB tuple)
            tolerance (int): Color tolerance (0-255)
            
        Returns:
            str: Path to the processed image
        """
        try:
            # Load image
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Parse target color
            if isinstance(target_color, str):
                color_rgb = self._parse_color_name(target_color)
            elif isinstance(target_color, (tuple, list)) and len(target_color) == 3:
                color_rgb = target_color
            else:
                raise ValueError("Invalid target_color. Use color name or RGB tuple.")
            
            # Create mask for the target color
            mask = self._create_color_mask(image_rgb, color_rgb, tolerance)
            
            # Create transparent background image
            result = self._apply_transparency_mask(image_rgb, mask)
            
            # Save result
            result_pil = Image.fromarray(result, 'RGBA')
            result_pil.save(output_path, 'PNG')
            
            print(f"Color-based background removal completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error removing color background: {str(e)}")
            raise
    
    def remove_background_interactive(self, input_path, output_path):
        """
        Interactive background removal with user color selection
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save output image
            
        Returns:
            str: Path to the processed image
        """
        try:
            print("\n🎨 Color-based Background Removal")
            print("Choose target color to remove:")
            print("   1. White")
            print("   2. Black") 
            print("   3. Custom RGB color")
            print("   4. Pick color from image")
            
            choice = input("   Enter choice (1-4): ").strip()
            tolerance = self._get_tolerance_input()
            
            if choice == '1':
                target_color = 'white'
            elif choice == '2':
                target_color = 'black'
            elif choice == '3':
                target_color = self._get_custom_color()
            elif choice == '4':
                target_color = self._pick_color_from_image(input_path)
            else:
                print("Invalid choice. Using white as default.")
                target_color = 'white'
            
            return self.remove_color_background(input_path, output_path, target_color, tolerance)
            
        except Exception as e:
            print(f"Error in interactive background removal: {str(e)}")
            raise
    
    def detect_background_colors(self, input_path, num_suggestions=5):
        """
        Detect potential background colors from image edges and corners
        
        Args:
            input_path (str): Path to input image
            num_suggestions (int): Number of color suggestions to return
            
        Returns:
            list: List of tuples (color_rgb, percentage, description)
        """
        try:
            # Suppress warnings for this function
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', RuntimeWarning)
                
                # Load image with high quality
                image = cv2.imread(input_path, cv2.IMREAD_COLOR)
                if image is None:
                    raise ValueError(f"Could not load image: {input_path}")
                
                # Convert to RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width = image_rgb.shape[:2]
                
                # Extract edge pixels (likely background)
                edge_pixels = []
                
                # Top and bottom edges (full width)
                edge_thickness = max(5, min(height // 20, 20))  # Adaptive edge thickness
                edge_pixels.extend(image_rgb[:edge_thickness, :].reshape(-1, 3))
                edge_pixels.extend(image_rgb[-edge_thickness:, :].reshape(-1, 3))
                
                # Left and right edges (remaining height)
                edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, :edge_thickness].reshape(-1, 3))
                edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, -edge_thickness:].reshape(-1, 3))
                
                # Convert to numpy array with proper data type and range checking
                edge_pixels = np.array(edge_pixels, dtype=np.float64)  # Use float64 for better precision
                
                if len(edge_pixels) == 0:
                    return []
                
                # Remove any invalid values and ensure valid range
                edge_pixels = edge_pixels[np.isfinite(edge_pixels).all(axis=1)]
                edge_pixels = np.clip(edge_pixels, 0, 255)  # Ensure valid color range
                
                if len(edge_pixels) < 10:  # Need minimum samples
                    return self._fallback_color_detection_simple(input_path)
                
                # Remove duplicate pixels to reduce computational load and improve stability
                unique_pixels, inverse_indices = np.unique(edge_pixels, axis=0, return_inverse=True)
                
                if len(unique_pixels) < 5:
                    return self._fallback_color_detection_simple(input_path)
                
                # Use K-means clustering with improved stability
                k = min(num_suggestions * 2, len(unique_pixels) // 5, 20)  # More conservative K
                k = max(2, k)  # Ensure minimum clusters
                
                # Normalize pixel values to 0-1 range for better numerical stability
                unique_pixels_normalized = unique_pixels / 255.0
                
                # Add small random noise to identical pixels to prevent numerical issues
                noise = np.random.normal(0, 1e-6, unique_pixels_normalized.shape)
                unique_pixels_normalized += noise
                unique_pixels_normalized = np.clip(unique_pixels_normalized, 0, 1)
                
                try:
                    # Use more robust K-means parameters
                    kmeans = KMeans(
                        n_clusters=k,
                        init='k-means++',
                        n_init=5,  # Reduced iterations for stability
                        max_iter=50,  # Reduced max iterations
                        tol=1e-3,  # Less strict tolerance
                        random_state=42,
                        algorithm='lloyd'  # Use Lloyd algorithm for stability
                    )
                    
                    cluster_labels = kmeans.fit_predict(unique_pixels_normalized)
                    cluster_centers = kmeans.cluster_centers_ * 255.0  # Scale back
                    
                    # Map back to original pixels
                    original_labels = cluster_labels[inverse_indices]
                    
                except Exception as e:
                    print(f"K-means failed, using histogram method: {str(e)}")
                    return self._fallback_color_detection(edge_pixels)
                
                # Count pixels in each cluster
                cluster_counts = Counter(original_labels)
                total_edge_pixels = len(edge_pixels)
                
                # Calculate color suggestions with percentages
                suggestions = []
                for cluster_id, count in cluster_counts.most_common(num_suggestions):
                    color_rgb = tuple(map(int, np.clip(cluster_centers[cluster_id], 0, 255)))
                    percentage = (count / total_edge_pixels) * 100
                    description = self._describe_color(color_rgb)
                    suggestions.append((color_rgb, percentage, description))
                
                return suggestions
            
        except Exception as e:
            print(f"Error detecting background colors: {str(e)}")
            return self._fallback_color_detection_simple(input_path)
    
    def detect_background_colors_gui(self, input_path, num_suggestions=6):
        """
        GUI-friendly version of background color detection that returns suggestions
        without CLI prompts for user selection in the GUI.
        
        Returns:
            list: List of (color_rgb, percentage, description) tuples
        """
        try:
            # Load and analyze image
            image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
            if image is None:
                return []
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get edge colors using existing analysis method
            color_candidates = self._analyze_edge_colors(image_rgb)
            
            if not color_candidates:
                return self._fallback_corner_sampling(input_path)
            
            # Format suggestions for GUI
            suggestions = []
            for i, (color_rgb, percentage) in enumerate(color_candidates[:num_suggestions]):
                description = self._describe_color(color_rgb)
                suggestions.append((tuple(color_rgb), percentage, description))
            
            return suggestions
            
        except Exception as e:
            print(f"Error in GUI color detection: {e}")
            return self._fallback_corner_sampling(input_path)

    def _analyze_edge_colors(self, image_rgb):
        """Analyze edge colors to find potential background colors"""
        try:
            height, width = image_rgb.shape[:2]
            
            # Extract edge pixels (likely background)
            edge_pixels = []
            
            # Top and bottom edges
            edge_thickness = max(5, min(height // 20, 20))
            edge_pixels.extend(image_rgb[:edge_thickness, :].reshape(-1, 3))
            edge_pixels.extend(image_rgb[-edge_thickness:, :].reshape(-1, 3))
            
            # Left and right edges
            edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, :edge_thickness].reshape(-1, 3))
            edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, -edge_thickness:].reshape(-1, 3))
            
            edge_pixels = np.array(edge_pixels, dtype=np.uint8)
            
            if len(edge_pixels) < 10:
                return []
            
            # Use K-means clustering for color analysis
            unique_pixels, inverse_indices = np.unique(edge_pixels, axis=0, return_inverse=True)
            
            if len(unique_pixels) < 3:
                return [(color, 100.0/len(unique_pixels)) for color in unique_pixels]
            
            # Cluster colors
            k = min(8, len(unique_pixels))
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(unique_pixels)
            cluster_centers = kmeans.cluster_centers_.astype(np.uint8)
            
            # Map back to original pixels
            original_labels = cluster_labels[inverse_indices]
            
            # Count pixels in each cluster
            cluster_counts = Counter(original_labels)
            total_pixels = len(edge_pixels)
            
            # Calculate color candidates with percentages
            color_candidates = []
            for cluster_id, count in cluster_counts.most_common():
                color_rgb = cluster_centers[cluster_id]
                percentage = (count / total_pixels) * 100
                color_candidates.append((color_rgb, percentage))
            
            return color_candidates
            
        except Exception as e:
            print(f"Error in edge color analysis: {e}")
            return []

    def _describe_color(self, color_rgb):
        """Generate human-readable color description"""
        r, g, b = color_rgb[:3]  # Handle both tuples and arrays
        
        # Define color ranges
        if r > 240 and g > 240 and b > 240:
            return "White/Very Light"
        elif r < 15 and g < 15 and b < 15:
            return "Black/Very Dark"
        elif abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20:
            if r > 200:
                return "Light Gray"
            elif r > 100:
                return "Medium Gray"
            else:
                return "Dark Gray"
        else:
            # Determine dominant color
            max_val = max(r, g, b)
            if r == max_val and r > g + 30 and r > b + 30:
                return "Red-ish"
            elif g == max_val and g > r + 30 and g > b + 30:
                return "Green-ish"
            elif b == max_val and b > r + 30 and b > g + 30:
                return "Blue-ish"
            elif r > 200 and g > 200 and b < 100:
                return "Yellow-ish"
            elif r > 200 and g < 100 and b > 200:
                return "Magenta-ish"
            elif r < 100 and g > 200 and b > 200:
                return "Cyan-ish"
            else:
                return "Mixed Color"

    def _fallback_corner_sampling(self, input_path):
        """Simple fallback using corner sampling"""
        try:
            image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image_rgb.shape[:2]
            
            # Sample corners and edges
            corner_pixels = [
                image_rgb[0, 0],                    # Top-left
                image_rgb[0, width-1],              # Top-right
                image_rgb[height-1, 0],             # Bottom-left
                image_rgb[height-1, width-1],       # Bottom-right
                image_rgb[0, width//2],             # Top-center
                image_rgb[height-1, width//2],      # Bottom-center
            ]
            
            color_candidates = []
            for color in corner_pixels:
                color_rgb = tuple(color.astype(int))
                color_candidates.append((color_rgb, 16.7))  # Equal weight
            
            return color_candidates[:5]  # Return top 5
            
        except Exception as e:
            print(f"Error in fallback sampling: {e}")
            return []

    def remove_background_with_suggestions(self, input_path, output_dir=None):
        """
        Remove background with automatic color detection and suggestions
        
        Args:
            input_path (str): Path to input image
            output_dir (str): Directory to save outputs (optional)
            
        Returns:
            dict: Results with suggested colors and processing options
        """
        try:
            input_path_obj = Path(input_path) if isinstance(input_path, str) else input_path
            
            # Set output directory
            if output_dir is None:
                output_dir = input_path_obj.parent
            else:
                output_dir = Path(output_dir)
                output_dir.mkdir(exist_ok=True)
            
            print("\n🔍 Analyzing image for potential background colors...")
            
            # Detect potential background colors
            suggestions = self.detect_background_colors(input_path, num_suggestions=6)
            
            if not suggestions:
                print("❌ Could not detect background colors")
                return None
            
            print(f"\n🎨 Found {len(suggestions)} potential background colors:")
            for i, (color, percentage, description) in enumerate(suggestions, 1):
                print(f"   {i}. RGB{color} - {description} ({percentage:.1f}% of edges)")
            
            print("\n🔧 Choose processing option:")
            print("   1. Remove ONE selected background color")
            print("   2. Generate images for ALL suggested colors")
            print("   3. Custom color removal")
            print("   0. Cancel")
            
            choice = input("\n   Enter choice (0-3): ").strip()
            
            results = {'original': str(input_path), 'processed': []}
            
            if choice == '1':
                # Single color removal
                color_choice = self._get_color_choice(suggestions)
                if color_choice is not None:
                    color_rgb, _, description = suggestions[color_choice]
                    output_path = output_dir / f"{input_path_obj.stem}_no_{description.lower().replace('/', '_').replace(' ', '_')}.png"
                    
                    tolerance = self._get_tolerance_input()
                    result = self.remove_color_background_hq(input_path, str(output_path), color_rgb, tolerance)
                    results['processed'].append({'color': color_rgb, 'description': description, 'path': result})
                    
            elif choice == '2':
                # Process all suggested colors
                print(f"\n🔄 Processing {len(suggestions)} background colors...")
                tolerance = self._get_tolerance_input()
                
                for i, (color_rgb, _, description) in enumerate(suggestions, 1):
                    print(f"   Processing {i}/{len(suggestions)}: {description}")
                    output_path = output_dir / f"{input_path_obj.stem}_no_{description.lower().replace('/', '_').replace(' ', '_')}.png"
                    
                    try:
                        result = self.remove_color_background_hq(input_path, str(output_path), color_rgb, tolerance)
                        results['processed'].append({'color': color_rgb, 'description': description, 'path': result})
                    except Exception as e:
                        print(f"   ⚠️ Failed to process {description}: {str(e)}")
                        
            elif choice == '3':
                # Custom color removal
                target_color = self._get_custom_color()
                tolerance = self._get_tolerance_input()
                output_path = output_dir / f"{input_path_obj.stem}_custom_removed.png"
                result = self.remove_color_background_hq(input_path, str(output_path), target_color, tolerance)
                results['processed'].append({'color': target_color, 'description': 'Custom', 'path': result})
            
            return results
            
        except Exception as e:
            print(f"Error in background removal with suggestions: {str(e)}")
            raise
    
    def _get_color_choice(self, suggestions):
        """Get user's color choice from suggestions"""
        while True:
            try:
                choice = input(f"\n   Select color (1-{len(suggestions)}): ").strip()
                if not choice:
                    return None
                choice_num = int(choice) - 1
                if 0 <= choice_num < len(suggestions):
                    return choice_num
                else:
                    print(f"   Please enter a number between 1 and {len(suggestions)}")
            except ValueError:
                print("   Please enter a valid number")
    
    def remove_color_background_hq(self, input_path, output_path, target_color, tolerance=30):
        """
        High-quality color-based background removal with enhanced edge processing
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save output image
            target_color (tuple): RGB color to remove
            tolerance (int): Color tolerance
            
        Returns:
            str: Path to the processed image
        """
        try:
            # Load image with maximum quality
            image = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Could not load image: {input_path}")
            
            # Convert to RGB with high precision
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            original_dtype = image_rgb.dtype
            
            # Work in float32 for better precision
            image_float = image_rgb.astype(np.float32)
            target_color_float = np.array(target_color, dtype=np.float32)
            
            # Enhanced color matching with multiple methods
            mask = self._create_enhanced_color_mask(image_float, target_color_float, tolerance)
            
            # Apply morphological operations for cleaner edges
            mask = self._refine_mask(mask)
            
            # Create high-quality result with anti-aliasing
            result = self._apply_hq_transparency_mask(image_rgb, mask)
            
            # Save with maximum quality
            result_pil = Image.fromarray(result, 'RGBA')
            result_pil.save(output_path, 'PNG', optimize=False, compress_level=1)
            
            print(f"✅ High-quality background removal completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error in HQ background removal: {str(e)}")
            raise
    
    def _create_enhanced_color_mask(self, image_float, target_color_float, tolerance):
        """Create enhanced color mask with multiple matching methods"""
        # Method 1: Euclidean distance
        color_diff = image_float - target_color_float
        euclidean_distance = np.sqrt(np.sum(color_diff ** 2, axis=2))
        mask_euclidean = euclidean_distance <= tolerance
        
        # Method 2: Manhattan distance (L1 norm)
        manhattan_distance = np.sum(np.abs(color_diff), axis=2)
        manhattan_threshold = tolerance * 1.5  # Adjust for different scale
        mask_manhattan = manhattan_distance <= manhattan_threshold
        
        # Method 3: Individual channel tolerance
        mask_channels = np.all(np.abs(color_diff) <= tolerance * 0.7, axis=2)
        
        # Combine masks (union of all methods for better coverage)
        combined_mask = mask_euclidean | mask_manhattan | mask_channels
        
        return combined_mask
    
    def _refine_mask(self, mask):
        """Refine mask with morphological operations for cleaner edges"""
        # Convert to uint8 for morphological operations
        mask_uint8 = mask.astype(np.uint8) * 255
        
        # Apply morphological opening to remove noise
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask_cleaned = cv2.morphologyEx(mask_uint8, cv2.MORPH_OPEN, kernel_small)
        
        # Apply morphological closing to fill small gaps
        kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_filled = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel_medium)
        
        # Apply Gaussian blur for smooth edges
        mask_smooth = cv2.GaussianBlur(mask_filled, (3, 3), 0.5)
        
        # Convert back to boolean
        return mask_smooth > 127
    
    def _apply_hq_transparency_mask(self, image_rgb, mask):
        """Apply transparency mask with anti-aliasing for high quality"""
        # Create RGBA image
        result = np.zeros((image_rgb.shape[0], image_rgb.shape[1], 4), dtype=np.uint8)
        result[:, :, :3] = image_rgb  # Copy RGB channels
        
        # Create smooth alpha channel
        alpha_channel = np.ones(mask.shape, dtype=np.float32) * 255
        alpha_channel[mask] = 0
        
        # Apply Gaussian blur to alpha for anti-aliasing
        alpha_smooth = cv2.GaussianBlur(alpha_channel, (3, 3), 0.5)
        
        # Apply alpha channel
        result[:, :, 3] = alpha_smooth.astype(np.uint8)
        
        return result

    def _parse_color_name(self, color_name):
        """Convert color name to RGB tuple"""
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128)
        }
        
        color_name_lower = color_name.lower()
        if color_name_lower in color_map:
            return color_map[color_name_lower]
        else:
            raise ValueError(f"Unknown color name: {color_name}")
    
    def _create_color_mask(self, image_rgb, target_color, tolerance):
        """Create mask for target color with tolerance"""
        target_color = np.array(target_color)
        
        # Calculate color distance
        color_diff = np.abs(image_rgb.astype(np.float32) - target_color.astype(np.float32))
        color_distance = np.sqrt(np.sum(color_diff ** 2, axis=2))
        
        # Create mask (True for pixels to remove)
        mask = color_distance <= tolerance
        
        return mask
    
    def _apply_transparency_mask(self, image_rgb, mask):
        """Apply transparency mask to image"""
        # Create RGBA image
        result = np.zeros((image_rgb.shape[0], image_rgb.shape[1], 4), dtype=np.uint8)
        result[:, :, :3] = image_rgb  # Copy RGB channels
        result[:, :, 3] = 255  # Set alpha to opaque
        
        # Set alpha to 0 (transparent) for masked pixels
        result[mask, 3] = 0
        
        return result
    
    def _get_tolerance_input(self):
        """Get tolerance value from user"""
        print("   Enter color tolerance (0-100, default: 30):")
        print("   Higher values remove more similar colors")
        try:
            tolerance_input = input("   Tolerance: ").strip()
            if not tolerance_input:
                return 30
            tolerance = int(tolerance_input)
            return max(0, min(100, tolerance))
        except ValueError:
            print("   Invalid input. Using default tolerance (30)")
            return 30
    
    def _get_custom_color(self):
        """Get custom RGB color from user"""
        print("   Enter RGB values (0-255):")
        try:
            r = int(input("   Red (0-255): ").strip())
            g = int(input("   Green (0-255): ").strip())
            b = int(input("   Blue (0-255): ").strip())
            
            # Clamp values
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            return (r, g, b)
        except ValueError:
            print("   Invalid RGB values. Using white as default.")
            return (255, 255, 255)
    
    def _pick_color_from_image(self, input_path):
        """Pick color from image coordinates (simplified version)"""
        try:
            image = cv2.imread(input_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image_rgb.shape[:2]
            
            print(f"   Image size: {width}x{height}")
            print("   Enter pixel coordinates to sample color:")
            
            x = int(input(f"   X coordinate (0-{width-1}): ").strip())
            y = int(input(f"   Y coordinate (0-{height-1}): ").strip())
            
            # Clamp coordinates
            x = max(0, min(width-1, x))
            y = max(0, min(height-1, y))
            
            # Get color at coordinates
            color = tuple(image_rgb[y, x])
            print(f"   Sampled color: RGB{color}")
            
            return color
            
        except Exception as e:
            print(f"   Error picking color: {str(e)}")
            print("   Using white as default.")
            return (255, 255, 255)
    
    def remove_background_with_model(self, input_path, output_path, model_name='u2net'):
        """
        Remove background with specific AI model
        
        Args:
            input_path (str): Path to input image  
            output_path (str): Path to save output image
            model_name (str): Model to use ('u2net', 'silueta', etc.)
            
        Returns:
            str: Path to the processed image
        """
        try:
            from rembg import remove, new_session
            
            # Create session with specific model
            session = new_session(model_name)
            
            # Read input image
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background with specific model
            output_data = remove(input_data, session=session)
            
            # Save the result
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            print(f"AI background removal with {model_name} model: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error removing background with model {model_name}: {str(e)}")
            raise
    
    def detect_background_colors_gui(self, image_path, num_suggestions=6):
        """
        Detect potential background colors from image - GUI version without CLI prompts
        Returns list of (color_rgb, percentage, description) tuples
        """
        try:
            # Load and preprocess image
            image = cv2.imread(str(image_path))
            if image is None:
                return []
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get edge-based color analysis
            color_candidates = self._get_edge_colors(image_rgb)
            
            if not color_candidates:
                return []
            
            # Format results for GUI
            suggestions = []
            for i, (color, percentage) in enumerate(color_candidates[:num_suggestions]):
                description = self._get_color_description(color)
                suggestions.append((tuple(color), percentage, description))
            
            return suggestions
            
        except Exception as e:
            print(f"Error detecting background colors: {e}")
            return []
    
    def _get_edge_colors(self, image_rgb):
        """Extract and analyze edge colors from image"""
        height, width = image_rgb.shape[:2]
        
        # Extract edge pixels (likely background)
        edge_pixels = []
        
        # Top and bottom edges (full width)
        edge_thickness = max(5, min(height // 20, 20))  # Adaptive edge thickness
        edge_pixels.extend(image_rgb[:edge_thickness, :].reshape(-1, 3))
        edge_pixels.extend(image_rgb[-edge_thickness:, :].reshape(-1, 3))
        
        # Left and right edges (remaining height)
        edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, :edge_thickness].reshape(-1, 3))
        edge_pixels.extend(image_rgb[edge_thickness:-edge_thickness, -edge_thickness:].reshape(-1, 3))
        
        # Convert to numpy array with proper data type
        edge_pixels = np.array(edge_pixels, dtype=np.float64)
        
        if len(edge_pixels) == 0:
            return []
        
        # Remove any invalid values and ensure valid range
        edge_pixels = edge_pixels[np.isfinite(edge_pixels).all(axis=1)]
        edge_pixels = np.clip(edge_pixels, 0, 255)
        
        if len(edge_pixels) < 10:
            return []
        
        # Remove duplicate pixels
        unique_pixels, inverse_indices = np.unique(edge_pixels, axis=0, return_inverse=True)
        
        if len(unique_pixels) < 5:
            return []
        
        # Use K-means clustering
        k = min(8, len(unique_pixels) // 5, 20)
        k = max(2, k)
        
        # Normalize pixel values
        unique_pixels_normalized = unique_pixels / 255.0
        
        # Add small random noise to prevent numerical issues
        noise = np.random.normal(0, 1e-6, unique_pixels_normalized.shape)
        unique_pixels_normalized += noise
        unique_pixels_normalized = np.clip(unique_pixels_normalized, 0, 1)
        
        try:
            kmeans = KMeans(
                n_clusters=k,
                init='k-means++',
                n_init=5,
                max_iter=50,
                tol=1e-3,
                random_state=42,
                algorithm='lloyd'
            )
            
            cluster_labels = kmeans.fit_predict(unique_pixels_normalized)
            cluster_centers = kmeans.cluster_centers_ * 255.0
            
            # Map back to original pixels
            original_labels = cluster_labels[inverse_indices]
            
        except Exception:
            return self._fallback_color_detection_gui(edge_pixels)
        
        # Count pixels in each cluster
        cluster_counts = Counter(original_labels)
        total_edge_pixels = len(edge_pixels)
        
        # Calculate color suggestions with percentages
        color_candidates = []
        for cluster_id, count in cluster_counts.most_common():
            color_rgb = np.clip(cluster_centers[cluster_id], 0, 255).astype(int)
            percentage = (count / total_edge_pixels) * 100
            color_candidates.append((color_rgb, percentage))
        
        return color_candidates
    
    def _get_color_description(self, color_rgb):
        """Generate human-readable color description"""
        r, g, b = color_rgb
        
        # Define color ranges
        if r > 240 and g > 240 and b > 240:
            return "White/Very Light"
        elif r < 15 and g < 15 and b < 15:
            return "Black/Very Dark"
        elif abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20:
            if r > 200:
                return "Light Gray"
            elif r > 100:
                return "Medium Gray"
            else:
                return "Dark Gray"
        else:
            # Determine dominant color
            max_val = max(r, g, b)
            if r == max_val and r > g + 30 and r > b + 30:
                return "Red-ish"
            elif g == max_val and g > r + 30 and g > b + 30:
                return "Green-ish"
            elif b == max_val and b > r + 30 and b > g + 30:
                return "Blue-ish"
            elif r > 200 and g > 200 and b < 100:
                return "Yellow-ish"
            elif r > 200 and g < 100 and b > 200:
                return "Magenta-ish"
            elif r < 100 and g > 200 and b > 200:
                return "Cyan-ish"
            else:
                return "Mixed Color"
    
    def _fallback_color_detection_gui(self, edge_pixels):
        """GUI-friendly fallback color detection using histogram analysis"""
        try:
            # Convert to integers for histogram
            edge_pixels_int = edge_pixels.astype(np.uint8)
            
            # Create color histogram
            colors, counts = np.unique(edge_pixels_int.reshape(-1, 3), axis=0, return_counts=True)
            
            # Sort by frequency
            sorted_indices = np.argsort(counts)[::-1]
            
            color_candidates = []
            total_pixels = len(edge_pixels_int)
            
            for i in range(min(6, len(sorted_indices))):
                idx = sorted_indices[i]
                color_rgb = colors[idx]
                percentage = (counts[idx] / total_pixels) * 100
                color_candidates.append((color_rgb, percentage))
            
            return color_candidates
            
        except Exception:
            return []
    
    def _fallback_color_detection_simple_gui(self, input_path):
        """Simple GUI-friendly fallback using corner sampling"""
        try:
            image = cv2.imread(input_path, cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image_rgb.shape[:2];
            
            # Sample corners and edges
            corner_pixels = [
                image_rgb[0, 0],           # Top-left
                image_rgb[0, width-1],     # Top-right
                image_rgb[height-1, 0],    # Bottom-left
                image_rgb[height-1, width-1],  # Bottom-right
                image_rgb[0, width//2],    # Top-center
                image_rgb[height-1, width//2],  # Bottom-center
            ]
            
            color_candidates = []
            for color in corner_pixels:
                color_rgb = color.astype(int)
                color_candidates.append((color_rgb, 16.7))  # Equal weight
            
            return color_candidates[:5]  # Return top 5
            
        except Exception:
            return []
    
    def process_selected_colors(self, image_path, selected_colors, tolerance=30):
        """
        Process selected colors for background removal - GUI version
        
        Args:
            image_path (str): Path to input image
            selected_colors (list): List of (color_rgb, description) tuples
            tolerance (int): Color tolerance for removal
            
        Returns:
            dict: Results with processed images
        """
        try:
            input_path_obj = Path(image_path)
            output_dir = input_path_obj.parent
            
            results = {'original': str(image_path), 'processed': []}
            
            for color_rgb, description in selected_colors:
                output_path = output_dir / f"{input_path_obj.stem}_no_{description.lower().replace('/', '_').replace(' ', '_')}.png"
                
                try:
                    result = self.remove_color_background_hq(
                        image_path, str(output_path), color_rgb, tolerance
                    )
                    results['processed'].append({
                        'color': color_rgb, 
                        'description': description, 
                        'path': result
                    })
                except Exception as e:
                    print(f"Failed to process {description}: {str(e)}")
            
            return results
            
        except Exception as e:
            print(f"Error processing selected colors: {str(e)}")
            raise