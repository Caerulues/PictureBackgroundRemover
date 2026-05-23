from pathlib import Path

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QMessageBox
)

from i18n import t
from image_processor import remove_solid_background
from qt_image_utils import make_preview


class BackgroundRemoverWindow(QWidget):
    PREVIEW_MAX_WIDTH = 650
    PREVIEW_MAX_HEIGHT = 520
    CONTROL_PANEL_WIDTH = 220
    WINDOW_MARGIN = 16
    LAYOUT_SPACING = 16

    def __init__(self):
        super().__init__()

        self.setWindowTitle(t("window_title"))

        self.file_path: Path | None = None
        self.original_image: Image.Image | None = None
        self.processed_image: Image.Image | None = None

        self.tolerance_slider = QSlider(Qt.Orientation.Horizontal)
        self.tolerance_slider.setRange(0, 120)
        self.tolerance_slider.setValue(35)

        self.softness_slider = QSlider(Qt.Orientation.Horizontal)
        self.softness_slider.setRange(0, 50)
        self.softness_slider.setValue(10)

        self.preview_label = QLabel(t("preview_placeholder"))
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet(
            "background-color: #222222;"
            "color: #aaaaaa;"
            "font-size: 16px;"
        )

        self.preview_label.setMinimumSize(
            self.PREVIEW_MAX_WIDTH,
            self.PREVIEW_MAX_HEIGHT
        )

        self.build_ui()
        self.connect_signals()
        self.apply_minimum_window_size()

    def build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            self.WINDOW_MARGIN,
            self.WINDOW_MARGIN,
            self.WINDOW_MARGIN,
            self.WINDOW_MARGIN
        )
        main_layout.setSpacing(self.LAYOUT_SPACING)

        control_layout = QVBoxLayout()
        control_layout.setSpacing(14)

        self.control_panel = QWidget()
        self.control_panel.setFixedWidth(self.CONTROL_PANEL_WIDTH)
        self.control_panel.setLayout(control_layout)

        open_button = QPushButton(t("select_image"))
        open_button.clicked.connect(self.open_image)

        save_button = QPushButton(t("export_png"))
        save_button.clicked.connect(self.save_image)

        tolerance_label = QLabel(t("tolerance"))
        softness_label = QLabel(t("edge_softness"))

        tip = QLabel(t("tip"))
        tip.setStyleSheet("color: #555555;")
        tip.setWordWrap(True)

        control_layout.addWidget(open_button)
        control_layout.addWidget(tolerance_label)
        control_layout.addWidget(self.tolerance_slider)
        control_layout.addWidget(softness_label)
        control_layout.addWidget(self.softness_slider)
        control_layout.addWidget(save_button)
        control_layout.addWidget(tip)
        control_layout.addStretch()

        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.preview_label)

    def apply_minimum_window_size(self):
        min_width = (
            self.CONTROL_PANEL_WIDTH +
            self.PREVIEW_MAX_WIDTH +
            self.WINDOW_MARGIN * 2 +
            self.LAYOUT_SPACING
        )

        min_height = (
            self.PREVIEW_MAX_HEIGHT +
            self.WINDOW_MARGIN * 2
        )

        self.setMinimumSize(min_width, min_height)
        self.resize(min_width, min_height)

    def connect_signals(self):
        self.tolerance_slider.valueChanged.connect(self.process_image)
        self.softness_slider.valueChanged.connect(self.process_image)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            t("select_image_dialog_title"),
            "",
            (
                f"{t('image_files')} (*.png *.jpg *.jpeg *.webp *.bmp);;"
                f"{t('all_files')} (*.*)"
            )
        )

        if not file_path:
            return

        self.file_path = Path(file_path)
        self.original_image = Image.open(file_path).convert("RGBA")
        self.process_image()

    def process_image(self):
        if self.original_image is None:
            return

        self.processed_image = remove_solid_background(
            image=self.original_image,
            tolerance=self.tolerance_slider.value(),
            edge_softness=self.softness_slider.value()
        )

        self.update_preview()

    def update_preview(self):
        if self.processed_image is None:
            return

        pixmap = make_preview(
            self.processed_image,
            max_size=(self.PREVIEW_MAX_WIDTH, self.PREVIEW_MAX_HEIGHT)
        )

        self.preview_label.setPixmap(pixmap)

    def save_image(self):
        if self.processed_image is None:
            QMessageBox.warning(
                self,
                t("warning"),
                t("select_image_first")
            )
            return

        default_name = t("default_export_name")

        if self.file_path:
            default_name = self.file_path.stem + t("transparent_suffix")

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            t("save_image_dialog_title"),
            default_name,
            f"{t('png_image')} (*.png)"
        )

        if not save_path:
            return

        if not save_path.lower().endswith(".png"):
            save_path += ".png"

        self.processed_image.save(save_path)

        QMessageBox.information(
            self,
            t("done"),
            f"{t('saved_to')}\n{save_path}"
        )