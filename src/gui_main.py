#!/usr/bin/env python3
"""
Image Editor GUI - PyQt6 Interface with Dark/Light Mode Support
"""

import sys
import os
import subprocess
import platform
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QSlider,
    QSpinBox, QGroupBox, QGridLayout, QProgressBar, QTabWidget,
    QTextEdit, QScrollArea, QFrame, QSizePolicy, QCheckBox,
    QDialog, QDialogButtonBox, QProgressDialog, QColorDialog,
    QListWidget, QListWidgetItem, QComboBox, QSplitter, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings
from PyQt6.QtGui import QPixmap, QFont, QIcon, QPalette, QColor, QAction, QPainter

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
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 16px;
                margin-bottom: 8px;
                padding-top: 18px;
                background-color: #fafafa;
                color: #2c2c2c;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 4px 12px 4px 12px;
                color: #2c2c2c;
                font-weight: bold;
                font-size: 13px;
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            
            QGroupBox::indicator {
                width: 16px;
                height: 16px;
                margin-right: 6px;
            }
            
            QGroupBox::indicator:unchecked {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iIzY2NjY2NiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            
            QGroupBox::indicator:checked {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDZMOCAxMEw0IDYiIHN0cm9rZT0iIzMzMzMzMyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                min-height: 32px;
                margin: 2px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
                border: 1px solid #3d8b40;
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
                font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
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
                border: 2px solid #505050;
                border-radius: 8px;
                margin-top: 16px;
                margin-bottom: 8px;
                padding-top: 18px;
                background-color: #2a2a2a;
                color: #e0e0e0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 4px 12px 4px 12px;
                color: #e0e0e0;
                font-weight: bold;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #505050;
                border-radius: 4px;
            }
            
            QGroupBox::indicator {
                width: 16px;
                height: 16px;
                margin-right: 6px;
            }
            
            QGroupBox::indicator:unchecked {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iI2FhYWFhYSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            
            QGroupBox::indicator:checked {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDZMOCAxMEw0IDYiIHN0cm9rZT0iI2RkZGRkZCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            
            QPushButton {
                background-color: #0d7377;
                color: #ffffff;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                min-height: 32px;
                margin: 2px;
            }
            
            QPushButton:hover {
                background-color: #14a085;
                border: 1px solid #0a5d61;
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
                font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
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
        self._is_running = False
    
    def run(self):
        self._is_running = True
        try:
            if self.operation == 'ai_background_removal':
                self.progress_update.emit("🤖 AI background removal in progress...")
                result = self.processor.remove_background(self.image_path)
                self.result_ready.emit({'type': 'single_file', 'path': result})
                
            elif self.operation == 'smart_background_removal':
                self.progress_update.emit("🔍 Analyzing image for background colors...")
                # Use GUI-friendly version that doesn't prompt for CLI input
                suggestions = self.bg_remover.detect_background_colors_gui(self.image_path, num_suggestions=6)
                
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
                    if not self._is_running:  # Check if thread should stop
                        break
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
            if self._is_running:  # Only emit error if still running
                self.error_occurred.emit(str(e))
        finally:
            self._is_running = False
    
    def stop(self):
        """Safely stop the thread"""
        self._is_running = False


class PreviewThread(QThread):
    """Thread for generating quick previews without blocking the UI"""
    preview_ready = pyqtSignal(str, str)  # preview_path, operation_type
    error_occurred = pyqtSignal(str)
    
    def __init__(self, operation, image_path, **kwargs):
        super().__init__()
        self.operation = operation
        self.image_path = image_path
        self.kwargs = kwargs
        self.bg_remover = BackgroundRemover()
        
    def run(self):
        try:
            import tempfile
            from pathlib import Path
            
            # Create temporary preview file
            input_path = Path(self.image_path)
            temp_dir = Path(tempfile.gettempdir()) / "image_editor_previews"
            temp_dir.mkdir(exist_ok=True)
            
            if self.operation == 'background_removal_preview':
                target_color = self.kwargs.get('target_color')
                tolerance = self.kwargs.get('tolerance', 30)
                
                # Generate low-resolution preview for speed
                preview_path = temp_dir / f"bg_preview_{input_path.stem}.png"
                
                # Use the HQ method but on a smaller scale for speed
                self.bg_remover.remove_color_background_hq(
                    self.image_path, str(preview_path), target_color, tolerance
                )
                
                self.preview_ready.emit(str(preview_path), "background_removal")
                
            elif self.operation == 'vectorization_preview':
                quality = self.kwargs.get('quality', 'standard')
                
                # Create quick vectorization preview
                preview_path = temp_dir / f"vector_preview_{input_path.stem}.svg"
                
                from vectorizer import Vectorizer
                vectorizer = Vectorizer()
                
                # Use faster settings for preview
                if quality == 'ultra':
                    detail_level = 'high'  # Reduce from ultra for preview speed
                elif quality == 'high':
                    detail_level = 'medium'
                else:
                    detail_level = 'low'
                
                vectorizer.vectorize_hq(self.image_path, str(preview_path), detail_level)
                self.preview_ready.emit(str(preview_path), "vectorization")
                
        except Exception as e:
            self.error_occurred.emit(str(e))
        

class ImagePreviewWidget(QWidget):
    """Widget for displaying image previews with comparison capabilities"""
    
    def __init__(self):
        super().__init__()
        self.current_pixmap = None
        self.original_image_path = None
        self.preview_mode = "original"  # "original", "preview", "comparison"
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Preview controls
        controls_layout = QHBoxLayout()
        
        self.preview_mode_combo = QComboBox()
        self.preview_mode_combo.addItems(["📷 Original", "👁️ Preview", "🔄 Comparison"])
        self.preview_mode_combo.currentTextChanged.connect(self.change_preview_mode)
        controls_layout.addWidget(QLabel("View:"))
        controls_layout.addWidget(self.preview_mode_combo)
        
        controls_layout.addStretch()
        
        # Zoom controls
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(25, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        self.zoom_label = QLabel("100%")
        
        controls_layout.addWidget(QLabel("Zoom:"))
        controls_layout.addWidget(self.zoom_slider)
        controls_layout.addWidget(self.zoom_label)
        
        layout.addLayout(controls_layout)
        
        # Main preview area
        self.preview_container = QWidget()
        self.preview_layout = QHBoxLayout(self.preview_container)
        
        # Original image label
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setStyleSheet("""
            QLabel {
                border: 2px solid #808080;
                border-radius: 10px;
                min-height: 300px;
                font-size: 14px;
                font-weight: bold;
                padding: 20px;
                margin: 5px;
            }
        """)
        
        # Preview image label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #4CAF50;
                border-radius: 10px;
                min-height: 300px;
                font-size: 14px;
                font-weight: bold;
                padding: 20px;
                margin: 5px;
            }
        """)
        
        self.preview_layout.addWidget(self.original_label)
        self.preview_layout.addWidget(self.preview_label)
        
        # Initially hide preview label
        self.preview_label.setVisible(False)
        
        # Scroll area for large images
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_container)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        
        # Set initial state
        self.original_label.setText("📷\nDrop image here or click 'Load Image'")
    
    def change_preview_mode(self, mode):
        """Change preview display mode"""
        self.preview_mode = mode.lower().split()[1] if len(mode.split()) > 1 else "original"
        
        if self.preview_mode == "original":
            self.preview_label.setVisible(False)
            self.original_label.setVisible(True)
        elif self.preview_mode == "preview":
            self.preview_label.setVisible(True)
            self.original_label.setVisible(False)
        elif self.preview_mode == "comparison":
            self.preview_label.setVisible(True)
            self.original_label.setVisible(True)
    
    def update_zoom(self, value):
        """Update zoom level"""
        self.zoom_label.setText(f"{value}%")
        if self.current_pixmap:
            self.update_image_display()
    
    def load_image(self, image_path):
        """Load and display original image"""
        try:
            self.original_image_path = image_path
            
            # Clear previous pixmap to free memory
            if self.current_pixmap:
                self.current_pixmap = None
            
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                self.current_pixmap = pixmap
                self.update_image_display()
                return True
            else:
                self.original_label.setText("❌ Failed to load image")
                return False
        except Exception as e:
            self.original_label.setText(f"❌ Error loading image:\n{str(e)}")
            return False
    
    def update_image_display(self):
        """Update image display with current zoom"""
        if not self.current_pixmap:
            return
            
        zoom_factor = self.zoom_slider.value() / 100.0
        base_size = 400
        scaled_size = int(base_size * zoom_factor)
        
        # Scale original image
        scaled_pixmap = self.current_pixmap.scaled(
            scaled_size, scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.original_label.setPixmap(scaled_pixmap)
        self.original_label.setText("")
    
    def show_preview(self, preview_image_path, operation_type="processed"):
        """Show preview of processed image"""
        try:
            preview_pixmap = QPixmap(str(preview_image_path))
            if not preview_pixmap.isNull():
                zoom_factor = self.zoom_slider.value() / 100.0
                base_size = 400
                scaled_size = int(base_size * zoom_factor)
                
                scaled_preview = preview_pixmap.scaled(
                    scaled_size, scaled_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                self.preview_label.setPixmap(scaled_preview)
                self.preview_label.setText("")
                
                # Update preview mode to show comparison
                if self.preview_mode == "original":
                    self.preview_mode_combo.setCurrentText("🔄 Comparison")
                    self.change_preview_mode("🔄 Comparison")
                
                return True
            else:
                self.preview_label.setText(f"❌ Failed to load {operation_type} preview")
                return False
        except Exception as e:
            self.preview_label.setText(f"❌ Error loading preview:\n{str(e)}")
            return False
    
    def clear_preview(self):
        """Clear preview image"""
        self.preview_label.clear()
        self.preview_label.setText("👁️ Preview will appear here")
        self.preview_mode_combo.setCurrentText("📷 Original")
        self.change_preview_mode("📷 Original")


class ImageEditorGUI(QMainWindow):
    """Main GUI application for Image Editor"""
    
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.processing_thread = None
        self.preview_thread = None
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self._delayed_preview_generation)
        self.pending_color_suggestions = None
        self.settings = QSettings()
        self.is_dark_mode = self.settings.value("dark_mode", False, type=bool)
        
        # Initialize processing modules
        self.bg_remover = BackgroundRemover()
        
        self.init_ui()
        self.apply_theme()
        
        # Restore window geometry if saved
        self.restore_window_state()
        
        # Connect resize event for responsive behavior
        self.original_resize_event = self.resizeEvent
        self.resizeEvent = self.handle_resize_event
        
    def init_ui(self):
        self.setWindowTitle("🎨 Image Editor - Background Removal & Vectorization")
        
        # Make GUI responsive to screen size
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        # Calculate responsive window size with better scaling
        base_width = max(screen_geometry.width() * 0.75, 1000)  # 75% of screen, min 1000px
        base_height = max(screen_geometry.height() * 0.8, 700)   # 80% of screen, min 700px
        
        # Clamp to reasonable limits based on screen size
        max_width = min(screen_geometry.width() - 100, 1600)    # Leave 100px margin
        max_height = min(screen_geometry.height() - 100, 1200)  # Leave 100px margin
        
        window_width = min(int(base_width), max_width)
        window_height = min(int(base_height), max_height)
        
        # Center window on screen
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Set responsive minimum size based on screen
        min_width = min(900, screen_geometry.width() - 200)
        min_height = min(650, screen_geometry.height() - 200)
        self.setMinimumSize(min_width, min_height)
        
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
        
        # Set responsive splitter proportions based on window size
        control_width = max(350, window_width * 0.25)  # 25% min, but at least 350px
        preview_width = window_width - control_width
        main_splitter.setSizes([int(control_width), int(preview_width)])
        
        # Set minimum sizes for splitter panes
        main_splitter.setChildrenCollapsible(False)
        main_splitter.widget(0).setMinimumWidth(320)  # Control panel minimum
        main_splitter.widget(1).setMinimumWidth(500)  # Preview panel minimum
        
        # Store splitter for resize events
        self.main_splitter = main_splitter
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready - Load an image to begin")
    
    def restore_window_state(self):
        """Restore saved window geometry and state"""
        # Restore window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore window state
        window_state = self.settings.value("windowState")
        if window_state:
            self.restoreState(window_state)
        
        # Restore splitter state
        if hasattr(self, 'main_splitter'):
            splitter_state = self.settings.value("splitter_state")
            if splitter_state:
                self.main_splitter.restoreState(splitter_state)
    
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
        """Create the left control panel with collapsible sections"""
        # Create scroll area for better handling of small screens
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)  # Reduced spacing for better organization
        
        # File operations group - always visible
        file_group = QGroupBox("📁 File Operations")
        file_group.setCheckable(False)  # Always expanded
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(6)
        
        self.load_btn = QPushButton("📂 Load Image")
        self.load_btn.clicked.connect(self.load_image)
        self.load_btn.setMinimumHeight(35)  # Better touch target
        file_layout.addWidget(self.load_btn)
        
        self.image_info_label = QLabel("No image loaded")
        self.image_info_label.setStyleSheet("font-style: italic; padding: 8px; background-color: rgba(128,128,128,0.1); border-radius: 4px;")
        self.image_info_label.setWordWrap(True)  # Handle long filenames
        file_layout.addWidget(self.image_info_label)
        
        layout.addWidget(file_group)
        
        # Preview controls group - collapsible
        preview_group = QGroupBox("👁️ Live Preview")
        preview_group.setCheckable(True)
        preview_group.setChecked(True)  # Expanded by default
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setSpacing(8)
        
        # Background removal preview controls
        bg_preview_layout = QVBoxLayout()
        
        # Color picker for preview
        color_picker_layout = QHBoxLayout()
        self.preview_color_btn = QPushButton("🎨 Pick Background Color")
        self.preview_color_btn.clicked.connect(self.pick_preview_color)
        self.preview_color_btn.setEnabled(False)
        color_picker_layout.addWidget(self.preview_color_btn)
        
        self.selected_color_label = QLabel("No color selected")
        self.selected_color_label.setStyleSheet("padding: 4px; border: 1px solid #ccc; border-radius: 3px;")
        color_picker_layout.addWidget(self.selected_color_label)
        bg_preview_layout.addLayout(color_picker_layout)
        
        # Live tolerance slider
        tolerance_preview_layout = QHBoxLayout()
        tolerance_preview_label = QLabel("Preview Tolerance:")
        tolerance_preview_label.setStyleSheet("font-weight: bold;")
        tolerance_preview_layout.addWidget(tolerance_preview_label)
        
        self.tolerance_preview_slider = QSlider(Qt.Orientation.Horizontal)
        self.tolerance_preview_slider.setRange(1, 100)
        self.tolerance_preview_slider.setValue(30)
        self.tolerance_preview_value_label = QLabel("30")
        self.tolerance_preview_value_label.setStyleSheet("font-weight: bold; min-width: 30px;")
        self.tolerance_preview_slider.valueChanged.connect(self.update_live_preview)
        tolerance_preview_layout.addWidget(self.tolerance_preview_slider)
        tolerance_preview_layout.addWidget(self.tolerance_preview_value_label)
        bg_preview_layout.addLayout(tolerance_preview_layout)
        
        # Preview generation button
        self.generate_preview_btn = QPushButton("👁️ Generate Preview")
        self.generate_preview_btn.clicked.connect(self.generate_background_preview)
        self.generate_preview_btn.setEnabled(False)
        bg_preview_layout.addWidget(self.generate_preview_btn)
        
        preview_layout.addLayout(bg_preview_layout)
        layout.addWidget(preview_group)
        
        # Background removal group - collapsible
        bg_group = QGroupBox("🎨 Background Removal")
        bg_group.setCheckable(True)
        bg_group.setChecked(True)  # Expanded by default
        bg_layout = QVBoxLayout(bg_group)
        bg_layout.setSpacing(6)
        
        self.ai_bg_btn = QPushButton("🤖 AI Background Removal")
        self.ai_bg_btn.clicked.connect(self.ai_background_removal)
        bg_layout.addWidget(self.ai_bg_btn)
        
        self.smart_bg_btn = QPushButton("🔍 Smart Color Detection")
        self.smart_bg_btn.clicked.connect(self.smart_background_removal)
        bg_layout.addWidget(self.smart_bg_btn)
        
        # Use preview settings for final processing
        self.use_preview_btn = QPushButton("✨ Use Preview Settings")
        self.use_preview_btn.clicked.connect(self.use_preview_settings)
        self.use_preview_btn.setEnabled(False)
        bg_layout.addWidget(self.use_preview_btn)
        
        layout.addWidget(bg_group)
        
        # Vectorization group with preview - collapsible
        vector_group = QGroupBox("📐 Vectorization")
        vector_group.setCheckable(True)
        vector_group.setChecked(False)  # Collapsed by default to save space
        vector_layout = QVBoxLayout(vector_group)
        vector_layout.setSpacing(6)
        
        # Quality selection with preview
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setStyleSheet("font-weight: bold;")
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Standard", "High", "Ultra"])
        self.quality_combo.setCurrentText("High")
        self.quality_combo.currentTextChanged.connect(self.update_vectorization_preview)
        quality_layout.addWidget(self.quality_combo)
        vector_layout.addLayout(quality_layout)
        
        # Vector preview button
        self.vector_preview_btn = QPushButton("👁️ Preview Vectorization")
        self.vector_preview_btn.clicked.connect(self.generate_vector_preview)
        self.vector_preview_btn.setEnabled(False)
        vector_layout.addWidget(self.vector_preview_btn)
        
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
        self.colors_spinbox.valueChanged.connect(self.update_vectorization_preview)
        colors_layout.addWidget(self.colors_spinbox)
        vector_layout.addLayout(colors_layout)
        
        self.colored_vector_btn = QPushButton("🎨 Colored Vectorization")
        self.colored_vector_btn.clicked.connect(self.colored_vectorization)
        vector_layout.addWidget(self.colored_vector_btn)
        
        layout.addWidget(vector_group)
        
        # Complete processing group - collapsible
        complete_group = QGroupBox("⚡ Complete Processing")
        complete_group.setCheckable(True)
        complete_group.setChecked(False)  # Collapsed by default
        complete_layout = QVBoxLayout(complete_group)
        complete_layout.setSpacing(6)
        
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
        
        # Set panel in scroll area
        scroll_area.setWidget(panel)
        return scroll_area
    
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

    def pick_preview_color(self):
        """Pick a color from the image for background removal preview"""
        if not self.current_image_path:
            self.show_error("Please load an image first")
            return
        
        from PyQt6.QtWidgets import QColorDialog
        from PyQt6.QtGui import QColor
        
        # Show color picker dialog
        color = QColorDialog.getColor(QColor(255, 255, 255), self, "Pick Background Color")
        
        if color.isValid():
            # Store the selected color
            self.selected_preview_color = (color.red(), color.green(), color.blue())
            
            # Update color display
            color_text = f"RGB({color.red()}, {color.green()}, {color.blue()})"
            self.selected_color_label.setText(color_text)
            self.selected_color_label.setStyleSheet(f"""
                padding: 4px; 
                border: 1px solid #ccc; 
                border-radius: 3px;
                background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                color: {'white' if (color.red() + color.green() + color.blue()) < 384 else 'black'};
                font-weight: bold;
            """)
            
            # Enable preview generation
            self.generate_preview_btn.setEnabled(True)
            self.use_preview_btn.setEnabled(True)
            
            # Enable live preview updates
            self.tolerance_preview_slider.valueChanged.disconnect()
            self.tolerance_preview_slider.valueChanged.connect(self.update_live_preview)
            
            self.log_message(f"🎨 Selected background color: {color_text}")
    
    def update_live_preview(self, value=None):
        """Update live preview when tolerance changes"""
        if value is not None:
            self.tolerance_preview_value_label.setText(str(value))
        
        # Use timer to debounce preview generation
        if hasattr(self, 'selected_preview_color') and self.selected_preview_color:
            self.preview_timer.stop()  # Stop any existing timer
            self.preview_timer.start(1000)  # Start 1-second delay
    
    def _delayed_preview_generation(self):
        """Generate preview after debounce delay"""
        if hasattr(self, 'selected_preview_color') and self.selected_preview_color:
            self.generate_background_preview()
    
    def generate_background_preview(self):
        """Generate background removal preview"""
        if not self.current_image_path or not hasattr(self, 'selected_preview_color'):
            return
        
        # Stop any existing preview thread
        if self.preview_thread and self.preview_thread.isRunning():
            self.preview_thread.terminate()
            self.preview_thread.wait()
        
        tolerance = self.tolerance_preview_slider.value()
        
        # Start preview generation thread
        self.preview_thread = PreviewThread(
            'background_removal_preview',
            self.current_image_path,
            target_color=self.selected_preview_color,
            tolerance=tolerance
        )
        self.preview_thread.preview_ready.connect(self.handle_preview_ready)
        self.preview_thread.error_occurred.connect(self.handle_preview_error)
        self.preview_thread.start()
        
        self.log_message(f"👁️ Generating background removal preview (tolerance: {tolerance})")
    
    def generate_vector_preview(self):
        """Generate vectorization preview"""
        if not self.current_image_path:
            return
        
        quality = self.quality_combo.currentText().lower()
        
        # Start preview generation thread
        self.preview_thread = PreviewThread(
            'vectorization_preview',
            self.current_image_path,
            quality=quality
        )
        self.preview_thread.preview_ready.connect(self.handle_preview_ready)
        self.preview_thread.error_occurred.connect(self.handle_preview_error)
        self.preview_thread.start()
        
        self.log_message(f"👁️ Generating vectorization preview (quality: {quality})")
    
    def handle_preview_ready(self, preview_path, operation_type):
        """Handle preview generation completion"""
        if self.original_preview.show_preview(preview_path, operation_type):
            self.log_message(f"✅ {operation_type.title()} preview ready")
            
            # Switch to original tab to show preview
            self.tab_widget.setCurrentIndex(0)
        else:
            self.log_message(f"❌ Failed to display {operation_type} preview")
    
    def handle_preview_error(self, error_message):
        """Handle preview generation error"""
        self.log_message(f"❌ Preview error: {error_message}")
    
    def update_vectorization_preview(self):
        """Update vectorization preview when parameters change"""
        # Auto-generate preview when quality or colors change
        if self.current_image_path:
            QTimer.singleShot(1000, self.generate_vector_preview)  # Debounce for 1 second
    
    def use_preview_settings(self):
        """Use current preview settings for final background removal"""
        if not hasattr(self, 'selected_preview_color') or not self.selected_preview_color:
            self.show_error("Please select a background color first")
            return
        
        tolerance = self.tolerance_preview_slider.value()
        
        # Process with current preview settings
        self.log_message(f"✨ Using preview settings: RGB{self.selected_preview_color}, tolerance: {tolerance}")
        
        # Create final high-quality result
        try:
            from pathlib import Path
            input_path = Path(self.current_image_path)
            output_path = input_path.parent / f"{input_path.stem}_bg_removed_preview_settings.png"
            
            result = self.bg_remover.remove_color_background_hq(
                self.current_image_path, 
                str(output_path), 
                self.selected_preview_color, 
                tolerance
            )
            
            self.add_result_file(result, "Preview Settings Result")
            self.show_success(f"Background removed using preview settings!\nSaved: {output_path.name}")
            
        except Exception as e:
            self.show_error(f"Failed to process with preview settings: {str(e)}")
    
    def update_button_states(self, enabled):
        """Enable/disable processing buttons based on image availability"""
        buttons = [
            self.ai_bg_btn, self.smart_bg_btn, self.vectorize_btn,
            self.colored_vector_btn, self.complete_btn
        ]
        for button in buttons:
            button.setEnabled(enabled)
        
        # Also update preview-related buttons
        preview_buttons = [
            self.preview_color_btn, self.vector_preview_btn
        ]
        for button in preview_buttons:
            button.setEnabled(enabled)
        
        # Keep preview generation and use buttons in their current state
        # They should only be enabled when a color is selected

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
                
                # Clear previous preview
                self.original_preview.clear_preview()
                
                # Reset preview settings
                if hasattr(self, 'selected_preview_color'):
                    delattr(self, 'selected_preview_color')
                self.selected_color_label.setText("No color selected")
                self.selected_color_label.setStyleSheet("padding: 4px; border: 1px solid #ccc; border-radius: 3px;")
                self.generate_preview_btn.setEnabled(False)
                self.use_preview_btn.setEnabled(False)
                
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
        """Handle processing results from the worker thread"""
        try:
            if result['type'] == 'single_file':
                self.status_label.setText(f"✅ Processing completed!")
                self.show_result_preview(result['path'])
                
            elif result['type'] == 'color_suggestions':
                # Show color selection dialog
                self.show_color_selection_dialog(result['suggestions'])
                
            elif result['type'] == 'multiple_files':
                results = result['results']
                self.status_label.setText(f"✅ Processed {len(results['processed'])} images!")
                
                # Show all results
                for processed in results['processed']:
                    self.show_result_preview(processed['path'])
                    
            elif result['type'] == 'complete_pipeline':
                results = result['results']
                self.status_label.setText("✅ Complete processing pipeline finished!")
                
                # Show all results
                for key, path in results.items():
                    if path and os.path.exists(path):
                        self.show_result_preview(path)
                        
        except Exception as e:
            self.status_label.setText(f"❌ Error handling result: {str(e)}")

    def show_color_selection_dialog(self, suggestions):
        """Show dialog for color selection"""
        from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                   QCheckBox, QLabel, QPushButton, QSpinBox)
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap, QPainter, QColor
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Background Colors to Remove")
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Select the background colors you want to remove:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Color checkboxes
        color_checkboxes = []
        
        for i, (color_rgb, percentage, description) in enumerate(suggestions):
            color_layout = QHBoxLayout()
            
            # Color preview square
            color_label = QLabel()
            color_pixmap = QPixmap(30, 30)
            color_pixmap.fill(QColor(*color_rgb))
            color_label.setPixmap(color_pixmap)
            color_layout.addWidget(color_label)
            
            # Checkbox with description
            checkbox = QCheckBox(f"RGB{color_rgb} - {description} ({percentage:.1f}% of edges)")
            checkbox.setChecked(i == 0)  # Check first option by default
            color_checkboxes.append((checkbox, color_rgb, description))
            color_layout.addWidget(checkbox)
            
            layout.addLayout(color_layout)
        
        # Tolerance setting
        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(QLabel("Color Tolerance:"))
        tolerance_spinbox = QSpinBox()
        tolerance_spinbox.setRange(1, 100)
        tolerance_spinbox.setValue(30)
        tolerance_spinbox.setSuffix(" (higher = remove more similar colors)")
        tolerance_layout.addWidget(tolerance_spinbox)
        tolerance_layout.addStretch()
        layout.addLayout(tolerance_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(lambda: [cb[0].setChecked(True) for cb in color_checkboxes])
        
        select_none_btn = QPushButton("Select None") 
        select_none_btn.clicked.connect(lambda: [cb[0].setChecked(False) for cb in color_checkboxes])
        
        process_btn = QPushButton("🔄 Process Selected Colors")
        process_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 8px; }")
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(select_none_btn)
        button_layout.addStretch()
        button_layout.addWidget(process_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Connect buttons with proper scope
        def select_all():
            for checkbox, _, _ in color_checkboxes:
                checkbox.setChecked(True)
        
        def select_none():
            for checkbox, _, _ in color_checkboxes:
                checkbox.setChecked(False)
        
        def process_selected():
            selected_colors = []
            for checkbox, color_rgb, description in color_checkboxes:
                if checkbox.isChecked():
                    selected_colors.append((color_rgb, description))
            
            if not selected_colors:
                QMessageBox.warning(dialog, "No Selection", "Please select at least one color to process.")
                return
            
            dialog.accept()
            self.process_selected_colors(selected_colors, tolerance_spinbox.value())
        
        select_all_btn.clicked.connect(select_all)
        select_none_btn.clicked.connect(select_none)
        process_btn.clicked.connect(process_selected)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def process_selected_colors(self, selected_colors, tolerance):
        """Process the selected colors for background removal"""
        if not hasattr(self, 'current_image_path') or not self.current_image_path:
            self.show_error("No image loaded")
            return
        
        # Start processing thread
        self.start_processing('process_selected_colors', selected_colors=selected_colors, tolerance=tolerance)

    def handle_processing_result(self, result):
        """Handle processing completion"""
        try:
            # Re-enable buttons
            self.update_button_states(True)
            self.progress_bar.setVisible(False)
            
            if result['type'] == 'single_file':
                path = result['path']
                self.add_result_file(path, "Processed Image")
                self.show_success(f"✅ Processing completed!\nSaved: {Path(path).name}")
                
            elif result['type'] == 'multiple_files':
                results = result['results']
                for item in results['processed']:
                    self.add_result_file(item['path'], f"{item['description']} Removal")
                
                message = f"✅ Processing completed!\n\nProcessed {len(results['processed'])} color variants:"
                for item in results['processed']:
                    message += f"\n• {item['description']}: {Path(item['path']).name}"
                self.show_success(message)
                
            elif result['type'] == 'complete_pipeline':
                results = result['results']
                for key, path in results.items():
                    if path and os.path.exists(path):
                        self.add_result_file(path, key.replace('_', ' ').title())
                
                message = f"✅ Complete pipeline finished!\n\nGenerated files:"
                for key, path in results.items():
                    if path:
                        message += f"\n• {key.replace('_', ' ').title()}: {Path(path).name}"
                self.show_success(message)
                
            elif result['type'] == 'color_suggestions':
                # Handle color suggestions from smart background removal
                self.show_color_suggestions(result['suggestions'])
                
            # Switch to results tab
            self.tab_widget.setCurrentIndex(1)
            
        except Exception as e:
            self.show_error(f"Error handling result: {str(e)}")

    def handle_processing_error(self, error_message):
        """Handle processing error"""
        self.update_button_states(True)
        self.progress_bar.setVisible(False)
        self.show_error(f"Processing failed: {error_message}")

    def ai_background_removal(self):
        """Start AI background removal"""
        self.start_processing('ai_background_removal')

    def smart_background_removal(self):
        """Start smart background removal with color detection"""
        self.start_processing('smart_background_removal')

    def vectorize_image(self):
        """Start image vectorization"""
        quality = self.quality_combo.currentText().lower()
        self.start_processing('vectorization', quality=quality)

    def colored_vectorization(self):
        """Start colored vectorization"""
        num_colors = self.colors_spinbox.value()
        quality = self.quality_combo.currentText().lower()
        self.start_processing('colored_vectorization', num_colors=num_colors, quality=quality)

    def complete_processing(self):
        """Start complete processing pipeline"""
        self.start_processing('complete_processing')

    def add_result_file(self, file_path, description="Result"):
        """Add result file to the results list"""
        if not os.path.exists(file_path):
            return
        
        file_path_obj = Path(file_path)
        
        # Create list item
        item_text = f"📁 {file_path_obj.name}\n   📍 {description}\n   📅 {self.get_file_time(file_path)}"
        
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, str(file_path))  # Store full path
        
        # Add to list
        self.results_list.addItem(item)
        
        # Update delete button state
        self.update_delete_button_state()
        
        self.log_message(f"📁 Added result: {file_path_obj.name}")

    def get_file_time(self, file_path):
        """Get file creation/modification time"""
        try:
            import os
            from datetime import datetime
            mtime = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Unknown time"

    def sort_results_list(self, sort_type):
        """Sort results list based on selection"""
        items = []
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            items.append((item.text(), file_path))
        
        if sort_type == "📅 Newest First":
            items.sort(key=lambda x: os.path.getmtime(x[1]) if os.path.exists(x[1]) else 0, reverse=True)
        elif sort_type == "📅 Oldest First":
            items.sort(key=lambda x: os.path.getmtime(x[1]) if os.path.exists(x[1]) else 0)
        elif sort_type == "📝 A-Z":
            items.sort(key=lambda x: Path(x[1]).name.lower())
        elif sort_type == "📝 Z-A":
            items.sort(key=lambda x: Path(x[1]).name.lower(), reverse=True)
        
        # Clear and repopulate list
        self.results_list.clear()
        for text, file_path in items:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.results_list.addItem(item)

    def on_selection_changed(self):
        """Handle selection changes in results list"""
        self.update_delete_button_state()

    def update_delete_button_state(self):
        """Update delete button enabled state"""
        has_selection = len(self.results_list.selectedItems()) > 0
        self.delete_selected_btn.setEnabled(has_selection)

    def delete_selected_files(self):
        """Delete selected files"""
        selected_items = self.results_list.selectedItems()
        if not selected_items:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion",
            f"Are you sure you want to delete {len(selected_items)} selected file(s)?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            for item in selected_items:
                file_path = item.data(Qt.ItemDataRole.UserRole)
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                        self.log_message(f"🗑️ Deleted: {Path(file_path).name}")
                    
                    # Remove from list
                    row = self.results_list.row(item)
                    self.results_list.takeItem(row)
                    
                except Exception as e:
                    self.log_message(f"❌ Failed to delete {Path(file_path).name}: {str(e)}")
            
            if deleted_count > 0:
                self.statusBar().showMessage(f"Deleted {deleted_count} file(s)")
            
            self.update_delete_button_state()

    def clear_all_results(self):
        """Clear all results"""
        if self.results_list.count() == 0:
            return
        
        reply = QMessageBox.question(
            self,
            "Clear All Results",
            "Are you sure you want to clear all results from the list?\nFiles will not be deleted from disk.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.results_list.clear()
            self.log_message("🧹 Cleared all results from list")
            self.update_delete_button_state()

    def open_result_file(self, item):
        """Open result file with default application"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        
        if not os.path.exists(file_path):
            self.show_error(f"File not found: {Path(file_path).name}")
            return
        
        try:
            if platform.system() == "Darwin":  # macOS
                os.system(f'open "{file_path}"')
            elif platform.system() == "Windows":
                os.startfile(file_path)
            else:  # Linux
                os.system(f'xdg-open "{file_path}"')
            
            self.log_message(f"📂 Opened: {Path(file_path).name}")
        except Exception as e:
            self.show_error(f"Failed to open file: {str(e)}")

    def show_context_menu(self, position):
        """Show context menu for results list"""
        item = self.results_list.itemAt(position)
        if not item:
            return
        
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        open_action = QAction("📂 Open File", self)
        open_action.triggered.connect(lambda: self.open_result_file(item))
        menu.addAction(open_action)
        
        reveal_action = QAction("📍 Show in Folder", self)
        reveal_action.triggered.connect(lambda: self.reveal_in_folder(item))
        menu.addAction(reveal_action)
        
        menu.addSeparator()
        
        delete_action = QAction("🗑️ Delete File", self)
        delete_action.triggered.connect(lambda: self.delete_single_file(item))
        menu.addAction(delete_action)
        
        menu.exec(self.results_list.mapToGlobal(position))

    def reveal_in_folder(self, item):
        """Reveal file in folder"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        
        if not os.path.exists(file_path):
            self.show_error(f"File not found: {Path(file_path).name}")
            return
        
        try:
            if platform.system() == "Darwin":  # macOS
                os.system(f'open -R "{file_path}"')
            elif platform.system() == "Windows":
                os.system(f'explorer /select,"{file_path}"')
            else:  # Linux
                folder_path = Path(file_path).parent
                os.system(f'xdg-open "{folder_path}"')
            
            self.log_message(f"📍 Revealed: {Path(file_path).name}")
        except Exception as e:
            self.show_error(f"Failed to reveal file: {str(e)}")

    def delete_single_file(self, item):
        """Delete a single file"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        file_name = Path(file_path).name
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{file_name}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.log_message(f"🗑️ Deleted: {file_name}")
                
                # Remove from list
                row = self.results_list.row(item)
                self.results_list.takeItem(row)
                
                self.statusBar().showMessage(f"Deleted {file_name}")
                self.update_delete_button_state()
                
            except Exception as e:
                self.show_error(f"Failed to delete {file_name}: {str(e)}")

    def handle_resize_event(self, event):
        """Handle window resize for responsive behavior"""
        # Call original resize event
        if self.original_resize_event:
            self.original_resize_event(event)
        
        # Adjust splitter proportions for small windows
        if hasattr(self, 'main_splitter'):
            window_width = self.width()
            
            if window_width < 1000:  # Compact mode
                control_width = min(300, window_width * 0.35)
            else:  # Standard mode
                control_width = min(400, window_width * 0.3)
            
            preview_width = window_width - control_width
            self.main_splitter.setSizes([int(control_width), int(preview_width)])

    def closeEvent(self, event):
        """Handle application close"""
        # Save window state
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        if hasattr(self, 'main_splitter'):
            self.settings.setValue("splitter_state", self.main_splitter.saveState())
        
        # Stop any running threads
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread.wait(3000)  # Wait up to 3 seconds
        
        if self.preview_thread and self.preview_thread.isRunning():
            self.preview_thread.terminate()
            self.preview_thread.wait(1000)  # Wait up to 1 second
        
        event.accept()


def main():
    """Main application entry point"""
    # Enable high DPI support
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Image Editor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ImageEditor")
    
    # Set application icon if available
    try:
        app.setWindowIcon(QIcon("icon.png"))
    except:
        pass
    
    # Create and show main window
    window = ImageEditorGUI()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()