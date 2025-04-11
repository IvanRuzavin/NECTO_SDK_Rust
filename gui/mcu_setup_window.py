import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QFileDialog, QScrollArea, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class MCUConfigurator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embedded Rust System Parameters")
        self.setMinimumSize(800, 600)

        self.def_path = os.path.join(os.path.dirname(__file__), "core_packages", "def")
        self.current_data = None
        self.field_widgets = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # MCU selection layout
        mcu_layout = QHBoxLayout()
        mcu_label = QLabel("MCU:")
        self.mcu_combo = QComboBox()
        self.mcu_combo.addItems([f[:-5] for f in os.listdir(self.def_path) if f.endswith(".json")])
        self.mcu_combo.currentTextChanged.connect(self.load_mcu_config)

        mcu_layout.addWidget(mcu_label)
        mcu_layout.addWidget(self.mcu_combo)
        layout.addLayout(mcu_layout)

        # Clock input
        clock_layout = QHBoxLayout()
        clock_label = QLabel("Clock (MHz):")
        self.clock_input = QLineEdit()
        clock_layout.addWidget(clock_label)
        clock_layout.addWidget(self.clock_input)
        layout.addLayout(clock_layout)

        # Scrollable field section
        self.scroll_area = QScrollArea()
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.form_widget)
        layout.addWidget(self.scroll_area)

        # Save button
        self.save_button = QPushButton("Save System Parameters")
        self.save_button.clicked.connect(self.save_parameters)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Load first MCU
        self.load_mcu_config(self.mcu_combo.currentText())

    def load_mcu_config(self, mcu_name):
        self.field_widgets.clear()
        
        # Clear previous content
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        filepath = os.path.join(self.def_path, f"{mcu_name}.json")
        if not os.path.exists(filepath):
            return

        with open(filepath, "r") as f:
            self.current_data = json.load(f)

        # Set clock value
        self.clock_input.setText(str(self.current_data.get("clock", 0)))

        # Populate visible fields
        for register in self.current_data.get("config_registers", []):
            reg_key = register["key"]
            address = register["address"]
            combined_key = f"{reg_key}|{address}"

            for field in register["fields"]:
                if field.get("hidden", False):
                    continue

                label = field.get("label", field["key"])
                field_key = field["key"]
                combo = QComboBox()

                if "settings" in field:
                    for setting in field["settings"]:
                        combo.addItem(setting["label"], setting["value"])
                elif "settings_array" in field:
                    settings = field["settings_array"]
                    min_val = int(settings["min_value"])
                    max_val = int(settings["max_value"])
                    inverted = settings.get("inverted", False)
                    values = range(min_val, max_val + 1)
                    if inverted:
                        values = reversed(values)
                    for i in values:
                        val_hex = hex(i)[2:].zfill(8).upper()
                        combo.addItem(f"{field_key} = {i}", val_hex)

                self.form_layout.addRow(QLabel(label), combo)
                self.field_widgets.setdefault(combined_key, []).append((field["mask"], combo))


    def save_parameters(self):
        output = []
        clock = self.clock_input.text()
        try:
            clock_int = int(clock)
        except ValueError:
            QMessageBox.critical(self, "Error", "Clock must be a valid integer")
            return

        for reg_key, fields in self.field_widgets.items():
            reg_name, addr = reg_key.split("|")
            reg_value = 0
            for mask, widget in fields:
                value_hex = widget.currentData()
                if value_hex is None:
                    continue
                value_int = int(value_hex, 16)
                reg_value |= value_int

            output.append(f"pub const ADDRESS_{reg_name}\t: u32 = 0x{addr};")
            output.append(f"pub const VALUE_{reg_name}\t: u32 = 0x{reg_value:08X};")

        output.append(f"pub const FOSC_KHZ_VALUE : u32 = {clock_int * 1000};")

        os.makedirs("core_header", exist_ok=True)
        with open("core_header/lib.rs", "w") as f:
            f.write("\n".join(output))

        QMessageBox.information(self, "Saved", "System parameters saved to core_header/lib.rs")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MCUConfigurator()
    win.show()
    sys.exit(app.exec())
