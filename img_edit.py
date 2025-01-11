import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QComboBox, QListWidget, QLabel, QFileDialog, QMessageBox,QSlider
)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        #Widgets
        self.select_folder = QPushButton('Select Folder')
        self.file_list = QListWidget()
        
        self.btn_left = QPushButton('Left')
        self.btn_right = QPushButton('Right')
        self.mirror = QPushButton('Mirror')
        self.sharp = QPushButton('Sharp')
        self.gray = QPushButton('Gray')
        self.saturation = QPushButton('Saturation')
        self.contrast = QPushButton('Contrast')
        self.blur = QPushButton('Blur')
        self.save_button = QPushButton('Save')
        
        
        self.filter_box = QComboBox()
        self.filter_box.addItems([
            'Original', 'Left', 'Right', 'Mirror',
            'Sharp', 'Gray', 'Saturation', 'Contrast', 'Blur'
        ])
        
        self.picture_box = QLabel('Image will appear here.')
        
        #Editor Variables
        self.working_directory = ''
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = 'edits/'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Photo Editor')
        self.resize(900, 700)
        self.master_layout = QHBoxLayout()
        self.line_1 = QVBoxLayout()
        self.line_2 = QVBoxLayout()
        
        # Add widgets to line_1
        self.line_1.addWidget(self.select_folder)
        self.line_1.addWidget(self.file_list)
        self.line_1.addWidget(self.filter_box)
        self.line_1.addWidget(self.btn_left)
        self.line_1.addWidget(self.btn_right)
        self.line_1.addWidget(self.mirror)
        self.line_1.addWidget(self.sharp)
        self.line_1.addWidget(self.gray)
        self.line_1.addWidget(self.saturation)
        self.line_1.addWidget(self.contrast)
        self.line_1.addWidget(self.blur)
        
        self.line_1.addWidget(self.save_button)
        
        # Add widgets to line_2
        self.line_2.addWidget(self.picture_box)
        
        # Add lines to master_layout
        self.master_layout.addLayout(self.line_1, 20)
        self.master_layout.addLayout(self.line_2, 80)
        self.setLayout(self.master_layout)
        
        # Connect signals
        self.select_folder.clicked.connect(self.getWorkDirectory)
        self.file_list.currentRowChanged.connect(self.display_image)
        self.gray.clicked.connect(lambda: self.transformImage('Gray')) 
        self.btn_left.clicked.connect(lambda: self.transformImage('Left'))
        self.btn_right.clicked.connect(lambda: self.transformImage('Right'))
        self.sharp.clicked.connect(lambda: self.transformImage('Sharp'))
        self.blur.clicked.connect(lambda: self.transformImage('Blur'))
        self.saturation.clicked.connect(lambda: self.transformImage('Color'))
        self.contrast.clicked.connect(lambda: self.transformImage('Contrast'))
        self.mirror.clicked.connect(lambda: self.transformImage('Mirror'))
        self.filter_box.currentIndexChanged.connect(self.handle_filter)
        self.save_button.clicked.connect(self.save_image_file)
        
        
    def filter(self, files, extensions):
        """Filter files by the given extensions."""
        results = []
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    results.append(file)
        return results

    def getWorkDirectory(self):
        """Open a folder selection dialog and list image files in the folder."""
        self.working_directory = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        # Check if the user selected a folder
        if not self.working_directory:
            return
        
        extensions = ['.jpg', '.jpeg', '.png', '.svg']
        try:
            filenames = self.filter(os.listdir(self.working_directory), extensions)
            self.file_list.clear()
            for filename in filenames:
                self.file_list.addItem(filename)
        except Exception as e:
            self.file_list.addItem(f"Error reading folder: {e}")
    
    def load_image(self,filename):
        self.filename = filename
        fullname = os.path.join(self.working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()
        
    def save_image(self):
        path = os.path.join(self.working_directory, self.save_folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path,self.filename)
        self.image.save(fullname)
        
    def show_image(self,path):
        self.picture_box.hide()
        image = QPixmap(path)
        w,h = self.picture_box.width(), self.picture_box.height()
        image = image.scaled(w,h, Qt.KeepAspectRatio)
        self.picture_box.setPixmap(image)
        self.picture_box.show()
    
    def display_image(self):
        if self.file_list.currentRow() >= 0:
            filename = self.file_list.currentItem().text()
            self.load_image(filename)
            self.show_image(os.path.join(self.working_directory, editor.filename))
            
    def transformImage(self, transformation):
        transformations = {
            'Gray': lambda image: image.convert('L'),
            'Color': lambda image: ImageEnhance.Color(image).enhance(1.2),
            'Contrast': lambda image: ImageEnhance.Contrast(image).enhance(1.2),
            'Sharp': lambda image: image.filter(ImageFilter.SHARPEN),
            'Blur': lambda image: image.filter(ImageFilter.BLUR),
            'Mirror': lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
            'Left': lambda image: image.transpose(Image.ROTATE_90),
            'Right': lambda image: image.transpose(Image.ROTATE_270),
        }
        transform_function = transformations.get(transformation)
        if transform_function:
            self.image = transform_function(self.image)
            self.save_image()
            image_path = os.path.join(self.working_directory, self.save_folder, self.filename)
            self.show_image(image_path)
    
    
    
    def apply_filter(self, filter_name):
        if filter_name == 'Original':
            self.image = self.original.copy()
            
        else:
            mapping = {
                'Gray':lambda image: image.convert('L'),
                'Color':lambda image: ImageEnhance.Color(image).enhance(1.2),
                'Contrast':lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                'Sharp':lambda image: image.filter(ImageFilter.SHARPEN),
                'Blur':lambda image: image.filter(ImageFilter.BLUR),
                'Mirror':lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                'Left':lambda image: image.transpose(Image.ROTATE_90),
                'Right':lambda image: image.transpose(Image.ROTATE_270)
                
            }
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(self.working_directory, self.save_folder, self.filename)
                self.show_image(image_path)
            pass
        
        self.save_image()
        image_path = os.path.join(self.working_directory, self.save_folder, self.filename)
        self.show_image(image_path)
        
    def handle_filter(self):
        if self.file_list.currentRow() >= 0:
            filter_name = self.filter_box.currentText()
            self.apply_filter(filter_name)
    
    def save_image_file(self):
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        if filename:
            try:
                self.image.save(filename)
                QMessageBox.information(self, "Saved", f"Image saved to: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {e}")
       
        
    def save_message(self):
        msg = QMessageBox()
        msg.setWindowTitle('Saved!')
        msg.setText('Image has been saved!')
        msg.exec_()
        
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
