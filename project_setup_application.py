import os, subprocess
import sys
import json
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QFileDialog, QScrollArea, QFormLayout, QMessageBox, QCompleter,
    QTextEdit,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class CommandRunner(QThread):
    """Runs terminal commands and sends real-time output to the GUI."""
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        process = subprocess.Popen(
            self.command,
            shell=True,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            self.output.emit(line)
        process.wait()
        self.finished.emit()


class ProjectWindow(QWidget):
    def __init__(self, mcu_name):
        super().__init__()
        self.setWindowTitle("Rust Project Builder")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()
        label = QLabel("System setup saved successfully!\nNow you can build or flash the project.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        project_label = QLabel("Project:")
        project_list = os.listdir(os.path.join(os.getcwd(), 'test'))
        self.project_combo = QComboBox()
        self.project_combo.setEditable(False)
        self.project_combo.addItems(project_list)

        choose_project_button = QPushButton("Choose Project")
        build_button = QPushButton("Build Project")
        flash_button = QPushButton("Flash MCU")
        erase_button = QPushButton("Erase MCU")
        close_button = QPushButton("Close")

        choose_project_button.clicked.connect(self.configure_main_project)
        build_button.clicked.connect(self.build_project)
        flash_button.clicked.connect(lambda: self.flash_project(mcu_name))
        erase_button.clicked.connect(lambda: self.erase_mcu(mcu_name))
        close_button.clicked.connect(self.close)

        # Terminal-like output area
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("""
            background-color: #111;
            color: #0f0;
            font-family: Consolas, monospace;
            font-size: 12px;
        """)

        layout.addWidget(label)
        layout.addWidget(project_label)
        layout.addWidget(self.project_combo)
        layout.addWidget(choose_project_button)
        layout.addWidget(build_button)
        layout.addWidget(flash_button)
        layout.addWidget(erase_button)
        layout.addWidget(close_button)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output_box)

        self.setLayout(layout)
        self.worker = None  # Will store QThread for subprocess

    def log(self, text):
        self.output_box.append(text)
        self.output_box.ensureCursorVisible()

    def run_command(self, command, cwd=None):
        if self.worker and self.worker.isRunning():
            self.log("Another command is already running.")
            return
        self.output_box.clear()
        self.log(f"$ {command}\n")

        self.worker = CommandRunner(command, cwd)
        self.worker.output.connect(self.log)
        self.worker.finished.connect(lambda: self.log("\nCommand finished.\n"))
        self.worker.start()

    def configure_main_project(self):
        selected_project = self.project_combo.currentText()
        with open(os.path.join(os.getcwd(), 'test', selected_project, 'main.rs'), 'r') as source_project:
            project_content = source_project.read()
        with open(os.path.join(os.getcwd(), 'src', 'main.rs'), 'w') as dest_project:
            dest_project.write(project_content)
        self.log(f"Project {selected_project} configured.\n")

    def build_project(self):
        self.run_command("cargo build")

    def flash_project(self, mcu_name):
        self.run_command(f"cargo flash --chip {mcu_name} --connect-under-reset")

    def erase_mcu(self, mcu_name):
        self.run_command(f"probe-rs erase --chip {mcu_name}")


class MCUConfigurator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embedded Rust System Parameters")
        self.setMinimumSize(800, 600)

        self.current_data = None
        self.field_widgets = {}

        self.database = sqlite3.connect("project_setup\database\database_mikro_sdk_rust.db")
        self.db_cursor = self.database.cursor()

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        # MCU selection layout
        mcu_layout = QHBoxLayout()
        mcu_label = QLabel("MCU:")
        # Get MCU list
        self.db_cursor.execute("SELECT NAME FROM MCU")
        mcu_list = [row[0] for row in self.db_cursor.fetchall()]
        self.mcu_combo = QComboBox()
        self.mcu_combo.setEditable(True)
        self.mcu_combo.addItems(mcu_list)

        # Enable filtering while typing
        completer = QCompleter(mcu_list, self.mcu_combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.mcu_combo.setCompleter(completer)

        # Optional: Hook up a callback
        self.mcu_combo.currentTextChanged.connect(self.load_mcu_config)

        mcu_layout.addWidget(mcu_label)
        mcu_layout.addWidget(self.mcu_combo)
        layout.addLayout(mcu_layout)

        self.setLayout(layout)

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

    def load_mcu_config(self, mcu_name):
        self.field_widgets.clear()
        selected_mcu = self.mcu_combo.currentText()
        self.db_cursor.execute(f"SELECT FAMILY.VENDOR FROM MCU JOIN FAMILY ON MCU.FAMILY = FAMILY.NAME WHERE MCU.NAME = '{selected_mcu}'")
        query_result = self.db_cursor.fetchall()
        if not query_result:
            return
        query_data = query_result[0]
        vendor = query_data[0]

        # Clear previous content
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        filepath = f"project_setup/core_packages/mcu_definitions/{vendor}/{selected_mcu}.json"
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
                field_key = field["key"]
                label = field.get("label", field_key)
                init_value = field.get("init", None)
                mask = field["mask"]

                if field.get("hidden", False):
                    self.field_widgets.setdefault(combined_key, []).append((mask, init_value))
                    continue

                combo = QComboBox()
                selected_index = -1

                if "settings" in field:
                    for i, setting in enumerate(field["settings"]):
                        combo.addItem(setting["label"], setting["value"])
                        if init_value.lower() == setting["value"].lower():
                            selected_index = i

                elif "settings_array" in field:
                    settings = field["settings_array"]
                    min_val = int(settings["min_value"])
                    max_val = int(settings["max_value"])
                    inverted = settings.get("inverted", False)
                    values = list(range(min_val, max_val + 1))
                    if inverted:
                        values = list(reversed(values))

                    init_value_array = "0x" + init_value.lstrip('0')

                    for i, val in enumerate(values):
                        mask_hex = int(f"0x{field["mask"]}", 16)
                        val_bin = bin(mask_hex)
                        val_hex = hex(int(f"0x{hex(val)[2:].zfill(8).upper()}", 16) << (len(val_bin) - len(val_bin.rstrip('0'))))
                        combo.addItem(f"{field_key} = {val}", val_hex)
                        if init_value_array == val_hex:
                            selected_index = i

                if selected_index != -1:
                    combo.setCurrentIndex(selected_index)

                self.form_layout.addRow(QLabel(label), combo)
                self.field_widgets.setdefault(combined_key, []).append((mask, combo))

    def save_parameters(self):
        selected_mcu = self.mcu_combo.currentText()
        self.db_cursor.execute(f"SELECT FAMILY.* FROM MCU JOIN FAMILY ON MCU.FAMILY = FAMILY.NAME WHERE MCU.NAME = '{selected_mcu}'")
        query_result = self.db_cursor.fetchall()[0]
        family_path = query_result[1]
        vendor = query_result[2]
        target = query_result[3]
        gpio = query_result[4]
        adc = query_result[5]
        i2c = query_result[6]
        spi = query_result[7]
        tim = query_result[8]
        uart = query_result[9]

        query_result_path_index = 3
        current_data = None
        family_template = None
        hal_ll_template = None
        implementation = None

        with open(f"project_setup/core_packages/mcu_definitions/{vendor}/{selected_mcu}.json", "r") as f:
            current_data = json.load(f)
        with open(f"family_definitions/{vendor}/{family_path}/Cargo_family_template.toml", "r") as f:
            family_template = f.read()
        with open("hal_ll/hal_ll_Cargo_template.toml", "r") as f:
            hal_ll_template = f.read()

        for language_impl in current_data.get("language_list", []):
            if language_impl.get("language") == "RUST":
                current_data = language_impl


        for module in current_data.get("module_list", []):
            module_name = module.get("module_name")
            sub_module_list = ""
            for sub_module in module.get("sub_modules", []):
                sub_module_name = sub_module.get("sub_module_name")
                pin_mapping = ""
                for pin_feature in sub_module.get("pin_map_features"):
                    pin_mapping += "\""
                    pin_mapping += pin_feature
                    pin_mapping += "\","
                pin_mapping = pin_mapping.rstrip(',')
                if pin_mapping != "":
                    sub_module_list += "\""
                    sub_module_list += sub_module_name
                    sub_module_list += "\","
                family_template = family_template.replace(f"{{{sub_module_name}_features}}", pin_mapping)
            sub_module_list = sub_module_list.rstrip(',')
            hal_ll_template = hal_ll_template.replace(f"{{{module_name}}}", sub_module_list)
            query_result_path_index += 1

        hal_ll_template = hal_ll_template.replace(f"{{family}}", family_path)


        #loading modules implementation
        with open(f"hal_ll/gpio/gpio_port/{gpio}/gpio_port.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/gpio_port.rs", "w") as f:
            f.write(implementation)

        with open(f"hal_ll/adc/{adc}/adc.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/adc.rs", "w") as f:
            f.write(implementation)

        with open(f"hal_ll/i2c/{i2c}/i2c_master.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/i2c_master.rs", "w") as f:
            f.write(implementation)

        with open(f"hal_ll/spi/{spi}/spi_master.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/spi_master.rs", "w") as f:
            f.write(implementation)

        with open(f"hal_ll/tim/{tim}/tim.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/tim.rs", "w") as f:
            f.write(implementation)

        with open(f"hal_ll/uart/{uart}/uart.rs", "r") as f:
            implementation = f.read()
        with open("hal_ll/src/uart.rs", "w") as f:
            f.write(implementation)




        with open(f"family_definitions/{vendor}/{family_path}/Cargo.toml", "w") as f:
            f.write(family_template)
        with open("hal_ll/Cargo.toml", "w") as f:
            f.write(hal_ll_template)

        with open(f"project_setup/core_packages/memory/{vendor}/{selected_mcu}/memory.x", "r") as f:
            memory_x_contents = f.read()
        with open("memory.x", "w") as f:
            f.write(memory_x_contents)

        with open(f"project_setup/core_packages/mcu_headers/{vendor}/{selected_mcu}/lib.rs", "r") as f:
            mcu_header_contents = f.read()
        with open("core/mcu_header/src/lib.rs", "w") as f:
            f.write(mcu_header_contents)

        with open(f"project_setup/core_packages/startup/{vendor}/{selected_mcu.lower()}.s", "r") as f:
            startup_contents = f.read()
        with open("core/system_reset/src/startup_assembly.s", "w") as f:
            f.write(startup_contents)

        with open(f".cargo/template_config.toml", "r") as f:
            config_contents = f.read()
        config_contents = config_contents.replace(f"{{compiling_target}}", target)
        with open(".cargo/config.toml", "w") as f:
            f.write(config_contents)

        core_header_output = []
        clock = self.clock_input.text()
        selected_mcu = self.mcu_combo.currentText()
        try:
            clock_int = int(clock)
        except ValueError:
            QMessageBox.critical(self, "Error", "Clock must be a valid integer")
            return

        for reg_key, fields in self.field_widgets.items():
            reg_name, addr = reg_key.split("|")
            reg_value = 0
            for mask, widget_or_value in fields:
                if isinstance(widget_or_value, QComboBox):
                    value_hex = widget_or_value.currentData()
                    if value_hex is None:
                        continue
                else:
                    # Hidden field with static init value
                    value_hex = widget_or_value

                value_int = int(value_hex, 16)
                reg_value |= value_int

            core_header_output.append(f"pub const ADDRESS_{reg_name}\t: u32 = 0x{addr};")
            core_header_output.append(f"pub const VALUE_{reg_name}\t: u32 = 0x{reg_value:08X};")

        core_header_output.append(f"pub const FOSC_KHZ_VALUE : u32 = {clock_int * 1000};")
        with open("core/system/src/core_header.rs", "w") as f:
            f.write("\n".join(core_header_output))

        self.db_cursor.execute(f"SELECT SYSTEM_LIB FROM MCU WHERE NAME = '{selected_mcu}'")
        query_result = self.db_cursor.fetchall()[0]
        system_lib = query_result[0]

        with open(f"core/system/system_implementations/{vendor}/{system_lib}.rs", "r") as f:
            system_contents = f.read()
        with open("core/system/src/lib.rs", "w") as f:
            f.write(system_contents)

        subprocess.run(f'rustup target add {target}')

        # After saving everything successfully
        QMessageBox.information(self, "Success", "System parameters saved successfully!")

        # Open the project window
        self.project_window = ProjectWindow(selected_mcu)
        self.project_window.show()

        # Close the current setup window
        self.close()



# Run Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MCUConfigurator()
    win.show()
    sys.exit(app.exec())