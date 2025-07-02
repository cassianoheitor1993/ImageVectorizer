#!/usr/bin/env python3
"""
Image Editor - Background Removal and Vectorization Tool
"""

import sys
import os
from pathlib import Path
from image_processor import ImageProcessor

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🎨 IMAGE EDITOR - Background Removal & Vectorization 🎨")
    print("=" * 60)
    print()

def get_image_path():
    """Get and validate image path from user"""
    while True:
        print("📁 Please provide the path to your image file:")
        print("   (or drag and drop the file here)")
        image_path = input("   Path: ").strip().strip('"').strip("'")
        
        if not image_path:
            print("❌ Please enter a valid path")
            continue
            
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            continue
            
        # Check if it's an image file
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        if Path(image_path).suffix.lower() not in valid_extensions:
            print(f"❌ Unsupported file format. Please use: {', '.join(valid_extensions)}")
            continue
            
        return image_path

def show_menu():
    """Display processing options menu"""
    print("\n🔧 Choose processing option:")
    print("   1. Remove Background (AI-based)")
    print("   2. Remove Background (Smart Color Detection)")
    print("   3. Remove Background (Manual Color)")
    print("   4. Vectorize Image Only")
    print("   5. High-Quality Vectorize")
    print("   6. Vectorize with Colors (HQ)")
    print("   7. Complete HQ Processing (Smart BG + Vector)")
    print("   0. Exit")
    
def main():
    """Main application function"""
    print_banner()
    
    try:
        # Get image path
        image_path = get_image_path()
        print(f"✅ Image loaded: {Path(image_path).name}")
        
        # Initialize processor
        processor = ImageProcessor()
        
        while True:
            show_menu()
            choice = input("\n   Enter your choice (0-7): ").strip()
            
            if choice == '0':
                print("👋 Thank you for using Image Editor!")
                sys.exit(0)
                
            elif choice == '1':
                print("\n🔄 Removing background (AI-based)...")
                try:
                    result = processor.remove_background(image_path)
                    print(f"✅ Background removed successfully!")
                    print(f"📄 Output: {result}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '2':
                print("\n🎨 Smart color detection background removal...")
                try:
                    results = processor.remove_background_smart(image_path)
                    if results and results.get('processed'):
                        print(f"✅ Smart background removal completed!")
                        print(f"📄 Processed {len(results['processed'])} variations:")
                        for i, result in enumerate(results['processed'], 1):
                            print(f"   {i}. {result['description']}: {result['path']}")
                    else:
                        print("❌ No background colors detected")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '3':
                print("\n🎨 Manual color-based background removal...")
                try:
                    result = processor.remove_color_background_interactive(image_path)
                    print(f"✅ Manual color-based background removal complete!")
                    print(f"📄 Output: {result}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '4':
                print("\n🔄 Vectorizing image...")
                try:
                    result = processor.vectorize_image(image_path)
                    print(f"✅ Image vectorized successfully!")
                    print(f"📄 Output: {result}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '5':
                print("\n🎨 High-quality vectorization...")
                try:
                    from vectorizer import Vectorizer
                    vectorizer = Vectorizer()
                    
                    input_path = Path(image_path)
                    output_path = input_path.parent / f"{input_path.stem}_hq_vector.svg"
                    
                    result = vectorizer.vectorize_high_quality(image_path, str(output_path))
                    print(f"✅ High-quality vectorization complete!")
                    print(f"📄 Output: {result}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '6':
                print("\n🎨 How many colors for HQ vectorization? (default: 8)")
                try:
                    colors = input("   Colors (2-32): ").strip()
                    num_colors = int(colors) if colors else 8
                    num_colors = max(2, min(32, num_colors))  # Clamp between 2-32
                    
                    print(f"🔄 Vectorizing with {num_colors} colors (HQ)...")
                    from vectorizer import Vectorizer
                    vectorizer = Vectorizer()
                    
                    input_path = Path(image_path)
                    output_path = input_path.parent / f"{input_path.stem}_color_hq_vector.svg"
                    
                    result = vectorizer.vectorize_with_colors_hq(image_path, str(output_path), num_colors)
                    print(f"✅ Colored high-quality vectorization complete!")
                    print(f"📄 Output: {result}")
                except ValueError:
                    print("❌ Invalid number. Using default (8 colors)")
                    num_colors = 8
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == '7':
                print("\n🔄 Complete high-quality processing pipeline...")
                try:
                    results = processor.process_complete_hq(image_path)
                    if 'error' in results:
                        print(f"❌ {results['error']}")
                    else:
                        print(f"✅ Complete processing finished!")
                        print(f"📄 Original: {results['original']}")
                        print(f"📄 Background removed: {results['best_background_removed']}")
                        print(f"📄 Final vector: {results['final_vector']}")
                        
                        # Show summary of all background removal results
                        bg_results = results['background_removal_results']
                        if bg_results and bg_results.get('processed'):
                            print(f"📄 Generated {len(bg_results['processed'])} background-removed variations:")
                            for i, result in enumerate(bg_results['processed'], 1):
                                print(f"   {i}. {result['description']}: {result['path']}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            else:
                print("❌ Invalid choice. Please select 0-7.")
                
            # Ask if user wants to continue
            print("\n" + "─" * 40)
            continue_choice = input("🔄 Process another option? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                break
                
        print("👋 Thank you for using Image Editor!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()