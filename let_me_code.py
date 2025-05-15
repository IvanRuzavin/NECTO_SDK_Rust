import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QPlainTextEdit, QTextEdit,
    QVBoxLayout, QWidget, QSplitter, QFileDialog, QMenuBar, QMessageBox
)
from PyQt6.QtGui import QPainter, QColor, QTextFormat, QMouseEvent, QFileSystemModel, QAction
from PyQt6.QtCore import Qt, QRect, QSize

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.breakpoint_lines = set()
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.highlight_current_line()

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.GlobalColor.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def mousePressEvent(self, event: QMouseEvent):
        margin_width = self.line_number_area_width()
        if event.position().x() < margin_width:
            cursor = self.cursorForPosition(event.position().toPoint())
            line = cursor.blockNumber()
            if line in self.breakpoint_lines:
                self.breakpoint_lines.remove(line)
            else:
                self.breakpoint_lines.add(line)
            self.update()
        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.paint_line_numbers()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space + 10

    def paint_line_numbers(self):
        painter = QPainter(self.viewport())
        font_metrics = self.fontMetrics()
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= self.viewport().height():
            if block.isVisible() and bottom >= 0:
                number = str(block_number + 1)
                margin = self.line_number_area_width()
                color = QColor("red") if block_number in self.breakpoint_lines else QColor("gray")
                painter.setPen(color)
                painter.drawText(0, top, margin - 4, font_metrics.height(), Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rust Project Viewer with Breakpoints")

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: File Tree
        self.model = QFileSystemModel()
        self.model.setReadOnly(True)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.open_file)
        self.splitter.addWidget(self.tree)

        # Right: Code Editor
        self.editor = CodeEditor()
        self.splitter.addWidget(self.editor)
        self.splitter.setStretchFactor(1, 1)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Menu
        self.create_menu()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Rust Project Folder", os.getcwd())
        if folder:
            self.model.setRootPath(folder)
            self.tree.setRootIndex(self.model.index(folder))

    def open_file(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path) and file_path.endswith(".rs"):
            with open(file_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.setWindowTitle(f"Editing: {os.path.basename(file_path)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())
