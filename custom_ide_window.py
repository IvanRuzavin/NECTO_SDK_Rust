import os, subprocess
import time, signal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit
)

from PyQt6.QtGui import QTextCursor

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer

class CommandRunner(QThread):
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


# -----------------------
# QThread worker for GDB
# -----------------------
class DebugWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, cfg_target, arm_target):
        super().__init__()
        self.cfg_target = cfg_target
        self.arm_target = arm_target
        self.openocd = None
        self.gdb = None
        self.running = True

    def run(self):
        try:
            self.output_signal.emit("[INFO] Starting OpenOCD...\n")
            self.openocd = subprocess.Popen(
                [
                    r"runner\\xpack-openocd-0.12.0-7\\bin\\openocd.exe",
                    "-f", rf"runner\\xpack-openocd-0.12.0-7\\bin\\{self.cfg_target}"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            time.sleep(2)  # Give OpenOCD time to start

            self.output_signal.emit("[INFO] Starting GDB...\n")
            self.gdb = subprocess.Popen(
                [
                    r"runner\\xpack-arm-none-eabi-gcc-14.2.1-1.1\\bin\\arm-none-eabi-gdb.exe",
                    rf"./target/{self.arm_target}/debug/mikrosdk"
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="cp1252"
            )

            # Connect and break main
            self.send_gdb_command("target extended-remote localhost:3333")
            self.send_gdb_command("monitor reset halt")
            self.send_gdb_command("load")
            self.send_gdb_command("break main")
            self.send_gdb_command("continue")

            # Continuously read GDB output
            for line in self.gdb.stdout:
                if not self.running:
                    break
                self.output_signal.emit(line)

        except Exception as e:
            self.output_signal.emit(f"[ERROR] {e}\n")

    def send_gdb_command(self, cmd):
        """Send a command to GDB through stdin."""
        if not self.gdb:
            return
        try:
            if cmd != signal.SIGINT:
                self.gdb.stdin.write(cmd + "\n")
                self.gdb.stdin.flush()
                self.output_signal.emit(f"(send) {cmd}\n")
            else:
                self.gdb.stdin.write
                self.gdb.stdin.flush()
                self.output_signal.emit(f"(send) PAUSE DEBUG\n")
        except Exception as e:
            self.output_signal.emit(f"[ERROR] Failed to send: {e}\n")

    def step(self):
        self.send_gdb_command("next")

    def step_into(self):
        self.send_gdb_command("step")

    def step_out(self):
        self.send_gdb_command("finish")

    def restart(self):
        self.send_gdb_command("run")

    def run_program(self):
        self.send_gdb_command("continue")

    def stop(self):
        self.output_signal.emit("[INFO] Stopping debugger...\n")
        self.running = False
        if self.gdb:
            try:
                self.gdb.stdin.write("quit\n")
                self.gdb.stdin.flush()
                self.gdb.terminate()
            except Exception:
                pass
        if self.openocd:
            self.openocd.terminate()
        self.quit()


# -------------------------
# Main PyQt Project Window
# -------------------------
class ProjectWindow(QWidget):
    def __init__(self, mcu_name, cfg_target, arm_target):
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
        debug_button = QPushButton("Debug MCU")
        step_button = QPushButton("Step")
        step_into_button = QPushButton("Step Into")
        step_out_button = QPushButton("Step Out")
        restart_button = QPushButton("Restart")
        run_button = QPushButton("Run")
        stop_debug_button = QPushButton("Stop Debugging")
        flash_button = QPushButton("Flash MCU")
        erase_button = QPushButton("Erase MCU")
        close_button = QPushButton("Close")

        choose_project_button.clicked.connect(self.configure_main_project)
        build_button.clicked.connect(self.build_project)
        debug_button.clicked.connect(lambda: self.debug_project(cfg_target, arm_target))
        step_button.clicked.connect(self.step_debug)
        step_into_button.clicked.connect(self.step_into_debug)
        step_out_button.clicked.connect(self.step_out_debug)
        restart_button.clicked.connect(self.restart_debug)
        run_button.clicked.connect(self.run_debug)
        stop_debug_button.clicked.connect(self.stop_debugging)
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
        layout.addWidget(debug_button)
        layout.addWidget(step_button)
        layout.addWidget(step_into_button)
        layout.addWidget(step_out_button)
        layout.addWidget(restart_button)
        layout.addWidget(run_button)
        layout.addWidget(stop_debug_button)
        layout.addWidget(flash_button)
        layout.addWidget(erase_button)
        layout.addWidget(close_button)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output_box)

        self.setLayout(layout)
        self.debug_worker = None  # QThread for debugger
        self.command_worker = None  # QThread for commander

    # -------------------
    # Debug control logic
    # -------------------
    def debug_project(self, cfg_target, arm_target):
        if self.debug_worker:
            self.output_box.append("[WARN] Debugger already running.\n")
            return
        self.debug_worker = DebugWorker(cfg_target, arm_target)
        self.debug_worker.output_signal.connect(self.append_output)
        self.debug_worker.start()
        self.output_box.append("[INFO] Debug session started.\n")

    def step_debug(self):
        if self.debug_worker:
            self.debug_worker.step()

    def step_into_debug(self):
        if self.debug_worker:
            self.debug_worker.step_into()

    def step_out_debug(self):
        if self.debug_worker:
            self.debug_worker.step_out()

    def restart_debug(self):
        if self.debug_worker:
            self.debug_worker.restart()

    def run_debug(self):
        if self.debug_worker:
            self.debug_worker.run_program()

    def stop_debugging(self):
        if self.debug_worker:
            self.debug_worker.stop()
            self.debug_worker = None
            self.output_box.append("[INFO] Debug session stopped.\n")

    def log(self, text):
        self.output_box.moveCursor(QTextCursor.MoveOperation.End)
        self.output_box.insertPlainText(text)
        self.output_box.ensureCursorVisible()

    def run_command(self, command, cwd=None):
        if self.command_worker and self.command_worker.isRunning():
            self.log("Another command is already running.")
            return
        self.output_box.clear()
        self.log(f"$ {command}\n")

        self.command_worker = CommandRunner(command, cwd)
        self.command_worker.output.connect(self.log)
        self.command_worker.finished.connect(lambda: self.log("\nCommand finished.\n"))
        self.command_worker.start()

    def configure_main_project(self):
        selected_project = self.project_combo.currentText()
        with open(os.path.join(os.getcwd(), 'test', selected_project, 'main.rs'), 'r') as source_project:
            project_content = source_project.read()
        with open(os.path.join(os.getcwd(), 'src', 'main.rs'), 'w') as dest_project:
            dest_project.write(project_content)
        self.log(f"Project {selected_project} configured.\n")

    def build_project(self):
        self.run_command("cargo build")

    def append_output(self, text):
        self.output_box.moveCursor(QTextCursor.MoveOperation.End)
        self.output_box.insertPlainText(text)
        self.output_box.ensureCursorVisible()

    def flash_project(self, mcu_name):
        self.run_command(f"cargo flash --chip {mcu_name} --connect-under-reset")

    def erase_mcu(self, mcu_name):
        self.run_command(f"probe-rs erase --chip {mcu_name}")