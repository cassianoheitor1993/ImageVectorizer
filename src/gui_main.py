#!/usr/bin/env python3
"""
Image Editor GUI - PyQt6 Interface with Dark/Light Mode Support
"""

import sys
import os
import platform
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QPushButton, QLabel, QFileDialog, QTextEdit, 
    QProgressBar, QGroupBox, QSpinBox, QSlider, QComboBox,
    QCheckBox, QSplitter, QScrollArea, QFrame, QMessageBox,
    QTabWidget, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox,
    QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings
from PyQt6.QtGui import QPixmap, QFont, QIcon, QPalette, QColor, QAction

# Import our processing modules
from image_processor import ImageProcessor
from background_remover import BackgroundRemover
from vectorizer import Vectorizer


class ThemeManager:
    """Manages light and dark themes for the application"""
    
    @staticmethod
    def get_light_theme():
        return """
            /* Light Theme */
            QMainWindow {
                background-color: #f5f5f5;
                color: #2c2c2c;
            }
            
            QWidget {
                background-color: #f5f5f5;
                color: #2c2c2c;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #ffffff;
                color: #2c2c2c;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #2c2c2c;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #999999;
            }
            
            QLabel {
                color: #2c2c2c;
                background-color: transparent;
            }
            
            QTextEdit {
                background-color: #ffffff;
                color: #2c2c2c;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 8px;
                font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
            
            QListWidget {
                background-color: #ffffff;
                color: #2c2c2c;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 4px;
                alternate-background-color: #f9f9f9;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
                color: #2c2c2c;
            }
            
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            QListWidget::item:hover {
                background-color: #e8f5e8;
                color: #2c2c2c;
            }
            
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background-color: #ffffff;
            }
            
            QTabBar::tab {
                background-color: #e8e8e8;
                color: #2c2c2c;
                padding: 10px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #d0d0d0;
                height: 6px;
                background: #f0f0f0;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #45a049;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #45a049;
            }
            
            QComboBox, QSpinBox {
                background-color: #ffffff;
                color: #2c2c2c;
                border: 1px solid #d0d0d0;
                padding: 6px 12px;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QComboBox:hover, QSpinBox:hover {
                border-color: #4CAF50;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #666666;
                width: 6px;
                height: 6px;
                border-top: none;
                border-right: none;
                transform: rotate(-45deg);
            }
            
            QProgressBar {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: #f0f0f0;
                text-align: center;
                color: #2c2c2c;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            
            QScrollArea {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            
            QMenuBar {
                background-color: #ffffff;
                color: #2c2c2c;
                border-bottom: 1px solid #d0d0d0;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            QMenu {
                background-color: #ffffff;
                color: #2c2c2c;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 8px 16px;
            }
            
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            QStatusBar {
                background-color: #ffffff;
                color: #2c2c2c;
                border-top: 1px solid #d0d0d0;
            }
        """
    
    @staticmethod
    def get_dark_theme():
        return """
            /* Dark Theme */
            QMainWindow {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #2a2a2a;
                color: #e0e0e0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #e0e0e0;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #0d7377;
                color: #ffffff;
                border: none;
                padding: 12px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #14a085;
                box-shadow: 0 2px 4px rgba(0,0,0,0.4);
            }
            
            QPushButton:pressed {
                background-color: #0a5d61;
            }
            
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
            
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            
            QTextEdit {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #0d7377;
            }
            
            QListWidget {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 4px;
                alternate-background-color: #333333;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
                color: #e0e0e0;
            }
            
            QListWidget::item:selected {
                background-color: #0d7377;
                color: #ffffff;
            }
            
            QListWidget::item:hover {
                background-color: #404040;
                color: #ffffff;
            }
            
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2a2a2a;
            }
            
            QTabBar::tab {
                background-color: #404040;
                color: #e0e0e0;
                padding: 10px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #0d7377;
                color: #ffffff;
            }
            
            QTabBar::tab:hover {
                background-color: #505050;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #404040;
                height: 6px;
                background: #404040;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #0d7377;
                border: 1px solid #14a085;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #14a085;
            }
            
            QComboBox, QSpinBox {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #404040;
                padding: 6px 12px;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QComboBox:hover, QSpinBox:hover {
                border-color: #0d7377;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #e0e0e0;
                width: 6px;
                height: 6px;
                border-top: none;
                border-right: none;
                transform: rotate(-45deg);
            }
            
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #404040;
                selection-background-color: #0d7377;
            }
            
            QProgressBar {
                border: 1px solid #404040;
                border-radius: 4px;
                background-color: #404040;
                text-align: center;
                color: #e0e0e0;
            }
            
            QProgressBar::chunk {
                background-color: #0d7377;
                border-radius: 3px;
            }
            
            QScrollArea {
                border: 1px solid #404040;
                border-radius: 4px;
                background-color: #2a2a2a;
            }
            
            QMenuBar {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border-bottom: 1px solid #404040;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #0d7377;
                color: #ffffff;
            }
            
            QMenu {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 8px 16px;
            }
            
            QMenu::item:selected {
                background-color: #0d7377;
                color: #ffffff;
            }
            
            QStatusBar {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border-top: 1px solid #404040;
            }
        """


class ColorSelectionDialog(QDialog):
    """Dialog for selecting background colors to remove"""
    
    def __init__(self, color_suggestions, parent=None):
        super().__init__(parent)
        self.color_suggestions = color_suggestions
        self.selected_colors = []
        self.tolerance = 30
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🎨 Select Background Colors")
        self.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Select which background colors to remove:")
        instructions.setStyleSheet("font-weight: bold; margin-bottom: 10px; font-size: 14px;")
        layout.addWidget(instructions)
        
        # Color list with checkboxes
        self.color_list = QListWidget()
        for i, (color, percentage, description) in enumerate(self.color_suggestions):
            item = QListWidgetItem(f"RGB{color} - {description} ({percentage:.1f}% of edges)")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if i == 0 else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, (color, description))
            self.color_list.addItem(item)
        
        layout.addWidget(self.color_list)
        
        # Tolerance setting
        tolerance_group = QGroupBox("Color Tolerance")
        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(QLabel("Tolerance:"))
        
        self.tolerance_slider = QSlider(Qt.Orientation.Horizontal)
        self.tolerance_slider.setRange(1, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_value_label = QLabel("30")
        self.tolerance_value_label.setStyleSheet("font-weight: bold; min-width: 30px;")
        self.tolerance_slider.valueChanged.connect(
            lambda v: self.tolerance_value_label.setText(str(v))
        )
        
        tolerance_layout.addWidget(self.tolerance_slider)
        tolerance_layout.addWidget(self.tolerance_value_label)
        tolerance_group.setLayout(tolerance_layout)
        layout.addWidget(tolerance_group)
        
        # Processing options
        options_group = QGroupBox("Processing Options")
        options_layout = QVBoxLayout()
        
        self.process_all_btn = QPushButton("✅ Process All Selected Colors")
        self.process_all_btn.clicked.connect(self.accept_all)
        
        self.process_selected_btn = QPushButton("🎯 Process Only Checked Colors")
        self.process_selected_btn.clicked.connect(self.accept_selected)
        
        options_layout.addWidget(self.process_all_btn)
        options_layout.addWidget(self.process_selected_btn)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def accept_all(self):
        """Process all suggested colors"""
        self.selected_colors = [(color, desc) for color, _, desc in self.color_suggestions]
        self.tolerance = self.tolerance_slider.value()
        self.accept()
    
    def accept_selected(self):
        """Process only checked colors"""
        self.selected_colors = []
        for i in range(self.color_list.count()):
            item = self.color_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                color, desc = item.data(Qt.ItemDataRole.UserRole)
                self.selected_colors.append((color, desc))
        
        if not self.selected_colors:
            QMessageBox.warning(self, "Warning", "Please select at least one color to process.")
            return
        
        self.tolerance = self.tolerance_slider.value()
        self.accept()


class ProcessingThread(QThread):
    """Thread for background processing to keep GUI responsive"""
    progress_update = pyqtSignal(str)
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, operation, image_path, **kwargs):
        super().__init__()
        self.operation = operation
        self.image_path = image_path
        self.kwargs = kwargs
        self.processor = ImageProcessor()
        self.bg_remover = BackgroundRemover()
    
    def run(self):
        try:
            if self.operation == 'ai_background_removal':
                self.progress_update.emit("🤖 AI background removal in progress...")
                result = self.processor.remove_background(self.image_path)
                self.result_ready.emit({'type': 'single_file', 'path': result})
                
            elif self.operation == 'smart_background_removal':
                self.progress_update.emit("🔍 Analyzing image for background colors...")
                # Get color suggestions without user interaction
                suggestions = self.bg_remover.detect_background_colors(self.image_path, num_suggestions=6)
                
                if not suggestions:
                    self.error_occurred.emit("Could not detect background colors in image")
                    return
                
                # Pass suggestions back to GUI for user selection
                self.result_ready.emit({
                    'type': 'color_suggestions', 
                    'suggestions': suggestions
                })
                
            elif self.operation == 'process_selected_colors':
                selected_colors = self.kwargs.get('selected_colors', [])
                tolerance = self.kwargs.get('tolerance', 30)
                
                if not selected_colors:
                    self.error_occurred.emit("No colors selected for processing")
                    return
                
                self.progress_update.emit(f"🔄 Processing {len(selected_colors)} selected colors...")
                
                results = {'original': self.image_path, 'processed': []}
                input_path_obj = Path(self.image_path)
                output_dir = input_path_obj.parent
                
                for i, (color_rgb, description) in enumerate(selected_colors, 1):
                    self.progress_update.emit(f"   Processing {i}/{len(selected_colors)}: {description}")
                    output_path = output_dir / f"{input_path_obj.stem}_no_{description.lower().replace('/', '_').replace(' ', '_')}.png"
                    
                    try:
                        result = self.bg_remover.remove_color_background_hq(
                            self.image_path, str(output_path), color_rgb, tolerance
                        )
                        results['processed'].append({
                            'color': color_rgb, 
                            'description': description, 
                            'path': result
                        })
                    except Exception as e:
                        self.progress_update.emit(f"   ⚠️ Failed to process {description}: {str(e)}")
                
                self.result_ready.emit({'type': 'multiple_files', 'results': results})
                
            elif self.operation == 'vectorization':
                quality = self.kwargs.get('quality', 'standard')
                self.progress_update.emit(f"📐 Vectorizing image ({quality} quality)...")
                result = self.processor.vectorize_image(self.image_path, quality)
                self.result_ready.emit({'type': 'single_file', 'path': result})
                
            elif self.operation == 'colored_vectorization':
                num_colors = self.kwargs.get('num_colors', 8)
                quality = self.kwargs.get('quality', 'high')
                
                # Validate parameters
                if num_colors < 2 or num_colors > 32:
                    self.error_occurred.emit("Number of colors must be between 2 and 32")
                    return
                
                self.progress_update.emit(f"🎨 Colored vectorization ({num_colors} colors)...")
                result = self.processor.vectorize_with_colors_hq(self.image_path, num_colors, quality)
                self.result_ready.emit({'type': 'single_file', 'path': result})
                
            elif self.operation == 'complete_processing':
                self.progress_update.emit("🔄 Complete processing pipeline...")
                results = self.processor.process_complete_hq(self.image_path)
                self.result_ready.emit({'type': 'complete_pipeline', 'results': results})
                
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            # Ensure thread cleanup
            self.quit()
            self.wait()


class ImagePreviewWidget(QWidget):
    """Widget for displaying image previews"""
    
    def __init__(self):
        super().__init__()
        self.current_pixmap = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #808080;
                border-radius: 10px;
                min-height: 300px;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        self.image_label.setText("📷\nDrop image here or click 'Load Image'")
        
        # Scroll area for large images
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
    
    def load_image(self, image_path):
        """Load and display image"""
        try:
            # Clear previous pixmap to free memory
            if self.current_pixmap:
                self.current_pixmap = None
            
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                # Scale image to fit preview while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    600, 400, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                self.current_pixmap = scaled_pixmap
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")
                return True
            else:
                self.image_label.setText("❌ Failed to load image")
                return False
        except Exception as e:
            self.image_label.setText(f"❌ Error loading image:\n{str(e)}")
            return False


class ImageEditorGUI(QMainWindow):
    """Main GUI application for Image Editor"""
    
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.processing_thread = None
        self.pending_color_suggestions = None
        self.settings = QSettings()
        self.is_dark_mode = self.settings.value("dark_mode", False, type=bool)
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        self.setWindowTitle("🎨 Image Editor - Background Removal & Vectorization")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main splitter for resizable panes
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Image preview and results
        right_panel = self.create_preview_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([400, 800])
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready - Load an image to begin")
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Theme toggle action
        self.theme_action = QAction("🌙 Dark Mode" if not self.is_dark_mode else "☀️ Light Mode", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        self.settings.setValue("dark_mode", self.is_dark_mode)
        self.apply_theme()
        
        # Update menu text
        self.theme_action.setText("🌙 Dark Mode" if not self.is_dark_mode else "☀️ Light Mode")
    
    def apply_theme(self):
        """Apply the selected theme"""
        if self.is_dark_mode:
            self.setStyleSheet(ThemeManager.get_dark_theme())
        else:
            self.setStyleSheet(ThemeManager.get_light_theme())
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>🎨 Image Editor</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Description:</b> AI-powered background removal and image vectorization tool</p>
        <p><b>Features:</b></p>
        <ul>
        <li>🤖 AI-based background removal</li>
        <li>🔍 Smart color detection</li>
        <li>📐 High-quality vectorization</li>
        <li>🎨 Colored vectorization</li>
        <li>🌙 Dark/Light mode support</li>
        </ul>
        <p><b>Built with:</b> PyQt6, OpenCV, scikit-learn, rembg</p>
        """
        QMessageBox.about(self, "About Image Editor", about_text)

    def create_control_panel(self):
        """Create the left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # File operations group
        file_group = QGroupBox("📁 File Operations")
        file_layout = QVBoxLayout(file_group)
        
        self.load_btn = QPushButton("📂 Load Image")
        self.load_btn.clicked.connect(self.load_image)
        file_layout.addWidget(self.load_btn)
        
        self.image_info_label = QLabel("No image loaded")
        self.image_info_label.setStyleSheet("font-style: italic; padding: 5px;")
        file_layout.addWidget(self.image_info_label)
        
        layout.addWidget(file_group)
        
        # Background removal group
        bg_group = QGroupBox("🎨 Background Removal")
        bg_layout = QVBoxLayout(bg_group)
        
        self.ai_bg_btn = QPushButton("🤖 AI Background Removal")
        self.ai_bg_btn.clicked.connect(self.ai_background_removal)
        bg_layout.addWidget(self.ai_bg_btn)
        
        self.smart_bg_btn = QPushButton("🔍 Smart Color Detection")
        self.smart_bg_btn.clicked.connect(self.smart_background_removal)
        bg_layout.addWidget(self.smart_bg_btn)
        
        # Tolerance slider for color-based removal
        tolerance_layout = QHBoxLayout()
        tolerance_label = QLabel("Tolerance:")
        tolerance_label.setStyleSheet("font-weight: bold;")
        tolerance_layout.addWidget(tolerance_label)
        
        self.tolerance_slider = QSlider(Qt.Orientation.Horizontal)
        self.tolerance_slider.setRange(1, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_value_label = QLabel("30")
        self.tolerance_value_label.setStyleSheet("font-weight: bold; min-width: 30px;")
        self.tolerance_slider.valueChanged.connect(
            lambda v: self.tolerance_value_label.setText(str(v))
        )
        tolerance_layout.addWidget(self.tolerance_slider)
        tolerance_layout.addWidget(self.tolerance_value_label)
        bg_layout.addLayout(tolerance_layout)
        
        layout.addWidget(bg_group)
        
        # Vectorization group
        vector_group = QGroupBox("📐 Vectorization")
        vector_layout = QVBoxLayout(vector_group)
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setStyleSheet("font-weight: bold;")
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Standard", "High", "Ultra"])
        self.quality_combo.setCurrentText("High")
        quality_layout.addWidget(self.quality_combo)
        vector_layout.addLayout(quality_layout)
        
        self.vectorize_btn = QPushButton("📐 Vectorize Image")
        self.vectorize_btn.clicked.connect(self.vectorize_image)
        vector_layout.addWidget(self.vectorize_btn)
        
        # Colored vectorization
        colors_layout = QHBoxLayout()
        colors_label = QLabel("Colors:")
        colors_label.setStyleSheet("font-weight: bold;")
        colors_layout.addWidget(colors_label)
        
        self.colors_spinbox = QSpinBox()
        self.colors_spinbox.setRange(2, 32)
        self.colors_spinbox.setValue(8)
        colors_layout.addWidget(self.colors_spinbox)
        vector_layout.addLayout(colors_layout)
        
        self.colored_vector_btn = QPushButton("🎨 Colored Vectorization")
        self.colored_vector_btn.clicked.connect(self.colored_vectorization)
        vector_layout.addWidget(self.colored_vector_btn)
        
        layout.addWidget(vector_group)
        
        # Complete processing group
        complete_group = QGroupBox("⚡ Complete Processing")
        complete_layout = QVBoxLayout(complete_group)
        
        self.complete_btn = QPushButton("🚀 Complete Pipeline")
        self.complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B35;
                font-size: 14px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #CC4E1F;
            }
        """)
        self.complete_btn.clicked.connect(self.complete_processing)
        complete_layout.addWidget(self.complete_btn)
        
        layout.addWidget(complete_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Disable buttons initially
        self.update_button_states(False)
        
        layout.addStretch()
        return panel
    
    def create_preview_panel(self):
        """Create the right preview panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Original image tab
        self.original_preview = ImagePreviewWidget()
        self.tab_widget.addTab(self.original_preview, "📷 Original")
        
        # Results tab
        self.results_widget = QWidget()
        results_layout = QVBoxLayout(self.results_widget)
        
        # Results header with controls
        results_header = QHBoxLayout()
        results_label = QLabel("📁 Generated Files:")
        results_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        results_header.addWidget(results_label)
        
        # Add sort and delete controls
        results_header.addStretch()
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["📅 Newest First", "📅 Oldest First", "📝 A-Z", "📝 Z-A"])
        self.sort_combo.setCurrentText("📅 Newest First")
        self.sort_combo.currentTextChanged.connect(self.sort_results_list)
        results_header.addWidget(QLabel("Sort:"))
        results_header.addWidget(self.sort_combo)
        
        self.delete_selected_btn = QPushButton("🗑️ Delete Selected")
        self.delete_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #ffcdd2;
                color: #999999;
            }
        """)
        self.delete_selected_btn.clicked.connect(self.delete_selected_files)
        self.delete_selected_btn.setEnabled(False)
        results_header.addWidget(self.delete_selected_btn)
        
        self.clear_all_btn = QPushButton("🧹 Clear All")
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #f57c00;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ef6c00;
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_all_results)
        results_header.addWidget(self.clear_all_btn)
        
        results_layout.addLayout(results_header)
        
        # Results list with multi-selection
        self.results_list = QListWidget()
        self.results_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.results_list.itemDoubleClicked.connect(self.open_result_file)
        self.results_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Add context menu
        self.results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_list.customContextMenuRequested.connect(self.show_context_menu)
        
        results_layout.addWidget(self.results_list)
        
        # Log area
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(150)
        
        log_label = QLabel("📝 Processing Log:")
        log_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        results_layout.addWidget(log_label)
        results_layout.addWidget(self.log_area)
        
        self.tab_widget.addTab(self.results_widget, "📋 Results")
        
        layout.addWidget(self.tab_widget)
        return panel

    def update_button_states(self, enabled):
        """Enable/disable processing buttons based on image availability"""
        buttons = [
            self.ai_bg_btn, self.smart_bg_btn, self.vectorize_btn,
            self.colored_vector_btn, self.complete_btn
        ]
        for button in buttons:
            button.setEnabled(enabled)
    
    def load_image(self):
        """Load image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.webp);;All Files (*)"
        )
        
        if file_path:
            self.current_image_path = file_path
            
            # Load preview
            if self.original_preview.load_image(file_path):
                # Update image info
                path_obj = Path(file_path)
                self.image_info_label.setText(f"📷 {path_obj.name}")
                
                # Enable processing buttons
                self.update_button_states(True)
                
                # Update status
                self.statusBar().showMessage(f"Image loaded: {path_obj.name}")
                self.log_message(f"✅ Image loaded: {file_path}")
            else:
                self.show_error("Failed to load image")
    
    def log_message(self, message):
        """Add message to log area with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_area.append(formatted_message)
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.log_message(f"❌ Error: {message}")
    
    def show_success(self, message):
        """Show success message"""
        QMessageBox.information(self, "Success", message)
        self.log_message(f"✅ {message}")
    
    def start_processing(self, operation, **kwargs):
        """Start background processing"""
        if not self.current_image_path:
            self.show_error("Please load an image first")
            return
        
        # Disable buttons during processing
        self.update_button_states(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Start processing thread
        self.processing_thread = ProcessingThread(operation, self.current_image_path, **kwargs)
        self.processing_thread.progress_update.connect(self.log_message)
        self.processing_thread.result_ready.connect(self.handle_processing_result)
        self.processing_thread.error_occurred.connect(self.handle_processing_error)
        self.processing_thread.start()
    
    def handle_processing_result(self, result):
        """Handle processing completion"""
        self.progress_bar.setVisible(False)
        self.update_button_states(True)
        
        if result['type'] == 'single_file':
            file_path = result['path']
            self.add_result_file(file_path)
            self.show_success(f"Processing complete!\nSaved: {Path(file_path).name}")
            
        elif result['type'] == 'color_suggestions':
            # Handle color suggestions from smart background removal
            suggestions = result['suggestions']
            self.handle_color_suggestions(suggestions)
            return  # Don't switch tabs yet
            
        elif result['type'] == 'multiple_files':
            results = result['results']
            if results and results.get('processed'):
                for item in results['processed']:
                    self.add_result_file(item['path'], item['description'])
                self.show_success(f"Generated {len(results['processed'])} files!")
            else:
                self.show_error("No results generated")
                
        elif result['type'] == 'complete_pipeline':
            results = result['results']
            if 'error' in results:
                self.show_error(results['error'])
            else:
                # Add all generated files
                bg_results = results['background_removal_results']
                if bg_results and bg_results.get('processed'):
                    for item in bg_results['processed']:
                        self.add_result_file(item['path'], f"BG Removed: {item['description']}")
                
                self.add_result_file(results['final_vector'], "Final Vector")
                self.show_success("Complete processing pipeline finished!")
        
        # Switch to results tab
        self.tab_widget.setCurrentIndex(1)
    
    def handle_color_suggestions(self, suggestions):
        """Handle color suggestions by showing selection dialog"""
        dialog = ColorSelectionDialog(suggestions, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_colors = dialog.selected_colors
            tolerance = dialog.tolerance
            
            if selected_colors:
                self.log_message(f"🎯 Processing {len(selected_colors)} selected colors with tolerance {tolerance}")
                self.start_processing('process_selected_colors', 
                                   selected_colors=selected_colors, 
                                   tolerance=tolerance)
            else:
                self.log_message("❌ No colors selected for processing")
        else:
            self.log_message("❌ Color selection cancelled")

    def ai_background_removal(self):
        """AI-based background removal"""
        self.start_processing('ai_background_removal')
    
    def smart_background_removal(self):
        """Smart color detection background removal"""
        self.start_processing('smart_background_removal')
    
    def vectorize_image(self):
        """Vectorize image"""
        quality = self.quality_combo.currentText().lower()
        self.start_processing('vectorization', quality=quality)
    
    def colored_vectorization(self):
        """Colored vectorization"""
        num_colors = self.colors_spinbox.value()
        quality = self.quality_combo.currentText().lower()
        self.start_processing('colored_vectorization', num_colors=num_colors, quality=quality)
    
    def complete_processing(self):
        """Complete processing pipeline"""
        self.start_processing('complete_processing')
    
    def open_result_file(self, item):
        """Open result file with system default application"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            try:
                if platform.system() == "Darwin":  # macOS
                    os.system(f"open '{file_path}'")
                elif platform.system() == "Windows":  # Windows
                    os.startfile(file_path)
                else:  # Linux and others
                    os.system(f"xdg-open '{file_path}'")
            except Exception as e:
                self.show_error(f"Failed to open file: {str(e)}")

    def closeEvent(self, event):
        """Handle application closing"""
        # Save settings
        self.settings.setValue("dark_mode", self.is_dark_mode)
        
        # Clean up processing thread if running
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
        event.accept()    
    
    def handle_processing_error(self, error_message):
        """Handle processing error"""
        self.progress_bar.setVisible(False)
        self.update_button_states(True)
        self.show_error(f"Processing failed: {error_message}")
    
    def add_result_file(self, file_path, description=None):
        """Add result file to the list with timestamp"""
        if not description:
            description = Path(file_path).name
        
        # Get file modification time
        try:
            mod_time = os.path.getmtime(file_path)
            from datetime import datetime
            formatted_time = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = "Unknown"
        
        # Create item with timestamp data
        display_text = f"📄 {description}"
        item = QListWidgetItem(display_text)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        item.setData(Qt.ItemDataRole.UserRole + 1, mod_time)  # Store timestamp for sorting
        item.setData(Qt.ItemDataRole.UserRole + 2, description)  # Store description
        item.setToolTip(f"File: {file_path}\nModified: {formatted_time}")
        
        self.results_list.addItem(item)
        self.log_message(f"📄 Generated: {file_path}")
        
        # Auto-sort based on current selection
        self.sort_results_list(self.sort_combo.currentText())
    
    def sort_results_list(self, order):
        """Sort results list based on selected order"""
        items_data = []
        
        # Extract all items with their data
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            timestamp = item.data(Qt.ItemDataRole.UserRole + 1) or 0
            description = item.data(Qt.ItemDataRole.UserRole + 2) or ""
            items_data.append((item.text(), file_path, timestamp, description, item.toolTip()))
        
        # Sort based on selected order
        if order == "📅 Newest First":
            items_data.sort(key=lambda x: x[2], reverse=True)  # Sort by timestamp descending
        elif order == "📅 Oldest First":
            items_data.sort(key=lambda x: x[2])  # Sort by timestamp ascending
        elif order == "📝 A-Z":
            items_data.sort(key=lambda x: x[3].lower())  # Sort by description A-Z
        elif order == "📝 Z-A":
            items_data.sort(key=lambda x: x[3].lower(), reverse=True)  # Sort by description Z-A
        
        # Clear and repopulate list
        self.results_list.clear()
        for text, file_path, timestamp, description, tooltip in items_data:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            item.setData(Qt.ItemDataRole.UserRole + 1, timestamp)
            item.setData(Qt.ItemDataRole.UserRole + 2, description)
            item.setToolTip(tooltip)
            self.results_list.addItem(item)
    
    def delete_selected_files(self):
        """Delete selected files from the list and filesystem"""
        selected_items = self.results_list.selectedItems()
        if not selected_items:
            return
        
        file_paths = []
        items_to_remove = []
        
        for item in selected_items:
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and os.path.exists(file_path):
                file_paths.append(file_path)
                items_to_remove.append(item)
        
        if not file_paths:
            self.show_error("No valid files selected for deletion")
            return
        
        # Show confirmation dialog
        file_list = "\n".join([Path(fp).name for fp in file_paths])
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to permanently delete these {len(file_paths)} files?\n\n{file_list}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                    self.log_message(f"🗑️ Deleted: {Path(file_path).name}")
                    deleted_count += 1
                except Exception as e:
                    self.log_message(f"❌ Error deleting {Path(file_path).name}: {str(e)}")
            
            # Remove items from list
            for item in items_to_remove:
                row = self.results_list.row(item)
                if row >= 0:
                    self.results_list.takeItem(row)
            
            if deleted_count > 0:
                self.show_success(f"Successfully deleted {deleted_count} file(s)")
        
        # Update button state
        self.on_selection_changed()
    
    def clear_all_results(self):
        """Clear all results from the list without deleting files"""
        if self.results_list.count() == 0:
            return
        
        reply = QMessageBox.question(
            self,
            "Clear Results",
            "This will clear the results list but won't delete the actual files. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            count = self.results_list.count()
            self.results_list.clear()
            self.log_message(f"🧹 Cleared {count} results from list")
    
    def on_selection_changed(self):
        """Update delete button state based on selection"""
        selected_items = self.results_list.selectedItems()
        self.delete_selected_btn.setEnabled(bool(selected_items))
        
        # Update button text with count
        if selected_items:
            count = len(selected_items)
            self.delete_selected_btn.setText(f"🗑️ Delete Selected ({count})")
        else:
            self.delete_selected_btn.setText("🗑️ Delete Selected")
    
    def show_context_menu(self, pos):
        """Show context menu for results list"""
        item = self.results_list.itemAt(pos)
        if not item:
            return
        
        # Create context menu
        menu = QMenu(self)
        
        open_action = menu.addAction("📂 Open File")
        open_folder_action = menu.addAction("📁 Show in Folder")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete File")
        
        # Execute action
        action = menu.exec(self.results_list.mapToGlobal(pos))
        
        if action == open_action:
            self.open_result_file(item)
        elif action == open_folder_action:
            self.show_in_folder(item)
        elif action == delete_action:
            # Temporarily select the item and delete
            self.results_list.clearSelection()
            item.setSelected(True)
            self.delete_selected_files()
    
    def show_in_folder(self, item):
        """Show file in folder/finder"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            try:
                if platform.system() == "Darwin":  # macOS
                    os.system(f"open -R '{file_path}'")
                elif platform.system() == "Windows":  # Windows
                    os.system(f"explorer /select,\"{file_path}\"")
                else:  # Linux
                    folder_path = os.path.dirname(file_path)
                    os.system(f"xdg-open '{folder_path}'")
            except Exception as e:
                self.show_error(f"Failed to show file in folder: {str(e)}")

    # ...existing methods...
def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Image Editor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Image Editor")
    
    # Create and show main window
    window = ImageEditorGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()