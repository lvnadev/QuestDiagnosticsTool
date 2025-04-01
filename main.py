import time
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
import subprocess
import re
import os
import json
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from io import BytesIO
import requests
import threading



class QuestDiagnosticsTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Diagnostics Tool")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        root.iconbitmap("assets/rainbowoculus.ico")
        root.configure(bg="#1e1e1e")
        
        
        quest_2_image = PhotoImage(file="assets/OculusQuest2.png")
        unknown_image = PhotoImage(file="assets/images.png")
        quest_1_image = PhotoImage(file="assets/OculusQuest1.png")
        quest_3_image = PhotoImage(file="assets/MetaQuest3.png")
        quest_3s_image = PhotoImage(file="assets/MetaQuest3S.png")

        self.bg_color = "#D3D3D3"
        self.header_color = "#2a2a2a"
        self.accent_color = "#5d6bc2"
        self.exploit_color = "#d93025"
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.current_dir, "assets/keyboard.py")
        self.placeholder_images = {
        "Quest 3S": quest_3s_image,
        "Quest 3": quest_3_image,
        "Quest 2": quest_2_image,
        "Quest 1": quest_1_image,
        "Unknown": unknown_image,
    }
        
        self.device_info = {}
        self.current_device = None
        self.current_button_page = "basic"
        
        def load_placeholder_images(self):
            try:
                self.placeholder_images["Quest 1"] = ImageTk.PhotoImage(Image.open("assets/images.png"))
                self.placeholder_images["Quest 2"] = ImageTk.PhotoImage(Image.open("OculusQuest2.png"))
                self.placeholder_images["Quest 3"] = ImageTk.PhotoImage(Image.open("assets/images.png"))
                self.placeholder_images["Quest 3S"] = ImageTk.PhotoImage(Image.open("assets/images.png"))
                self.placeholder_images["Unknown"] = ImageTk.PhotoImage(Image.open("assets/images.png"))
            except Exception as e:
                print(f"Error loading images: {e}")
                self.placeholder_images["Unknown"] = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color='grey'))
                print("Placeholder Images Loaded: ", self.placeholder_images)

        if "Unknown" not in self.placeholder_images:
                self.placeholder_images["Unknown"] = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color='grey'))

        

        
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.header_frame = tk.Frame(self.main_frame, bg=self.header_color)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = tk.Label(self.header_frame, text="Quest Diagnostics Tool", font=("Arial", 16, "bold"), bg=self.header_color, fg="white")
        header_label.pack(pady=10)
        
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.left_frame = tk.Frame(self.content_frame, bg=self.bg_color, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        self.left_frame.pack_propagate(False)
        
        self.image_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.device_image_label = tk.Label(self.image_frame, bg=self.bg_color)
        self.device_image_label.pack(pady=10)
        
        self.device_name_label = tk.Label(self.image_frame, text="No device connected", font=("Arial", 14, "bold"), bg=self.bg_color)
        self.device_name_label.pack(pady=5)
        
        self.system_info_frame = tk.LabelFrame(self.left_frame, text="System Info", bg=self.bg_color, font=("Arial", 12))
        self.system_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.system_info_text = tk.Text(self.system_info_frame, height=10, width=30, bg=self.bg_color, relief=tk.FLAT, state=tk.DISABLED)
        self.system_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.additional_info_frame = tk.LabelFrame(self.right_frame, text="Additional Information", bg=self.bg_color, font=("Arial", 12))
        self.additional_info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.additional_info_text = tk.Text(self.additional_info_frame, height=10, bg=self.bg_color, relief=tk.FLAT, state=tk.DISABLED)
        self.additional_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.button_nav_frame = tk.Frame(self.right_frame, bg=self.bg_color)
        self.button_nav_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.basic_tools_btn = tk.Button(self.button_nav_frame, text="Basic Tools", 
                                        command=self.show_basic_tools,
                                        bg=self.accent_color, fg="white", 
                                        font=("Arial", 10), width=15)
        self.basic_tools_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.exploits_btn = tk.Button(self.button_nav_frame, text="Exploits", 
                                     command=self.show_exploits,
                                     bg=self.exploit_color, fg="white", 
                                     font=("Arial", 10), width=15)
        self.exploits_btn.pack(side=tk.LEFT)
        
        self.basic_tools_frame = tk.LabelFrame(self.right_frame, text="Basic Tools", bg=self.bg_color, font=("Arial", 12))
        self.basic_tools_frame.pack(fill=tk.BOTH, expand=True)
        
        self.exploits_frame = tk.LabelFrame(self.right_frame, text="Exploits", bg=self.bg_color, font=("Arial", 12))
        
        self.basic_button_frame = tk.Frame(self.basic_tools_frame, bg=self.bg_color)
        self.basic_button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        basic_buttons = [
            ("Refresh ADB", self.refresh_device),
            ("Restart Device", lambda: self.run_adb_command("reboot")),
            ("Shutdown", lambda: self.run_adb_command("shell reboot -p")),
            ("Sideload APK", self.sideload_apk),
            ("Clear Cache", lambda: self.run_adb_command("shell pm clear com.oculus.vrshell")),
            ("Enter Recovery", lambda: self.run_adb_command("reboot recovery")),
            ("List Installed Apps", self.list_installed_apps),
            ("Battery Status", self.get_battery_status)
        ]
        
        row, col = 0, 0
        for button_text, command in basic_buttons:
            btn = tk.Button(self.basic_button_frame, text=button_text, command=command, 
                           bg=self.accent_color, fg="white", 
                           font=("Arial", 10), width=18, height=2)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        for i in range(4):
            self.basic_button_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.basic_button_frame.grid_columnconfigure(i, weight=1)
        
        self.exploits_button_frame = tk.Frame(self.exploits_frame, bg=self.bg_color)
        self.exploits_button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        exploit_buttons = [
            ("Factory Reset", self.factory_reset),
            ("Auth Exploit (W) (v72)", self.authexploit),
            ("Disable Guardian", self.disable_guardian),
            ("Enable Guardian", self.enable_guardian),
            ("Enable Developer Options", lambda: self.run_adb_command("shell setprop debug.oculus.enableDeveloperOptions 1")),
            ("Open ADB Keyboard", self.showadbkeyboard),
            
        ]
        
        row, col = 0, 0
        for button_text, command in exploit_buttons:
            btn = tk.Button(self.exploits_button_frame, text=button_text, command=command, 
                           bg=self.exploit_color, fg="white", 
                           font=("Arial", 10), width=18, height=2)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        for i in range(4):
            self.exploits_button_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.exploits_button_frame.grid_columnconfigure(i, weight=1)
            
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.check_adb_available()
        
        self.refresh_device()
    def enableguardian(self):
        self.run_adb_command("adb shell settings put global guardian_enabled 1")

    def show_basic_tools(self):
        """Switch to basic tools page"""
        if self.current_button_page != "basic":
            self.exploits_frame.pack_forget()
            self.basic_tools_frame.pack(fill=tk.BOTH, expand=True)
            self.current_button_page = "basic"
            self.basic_tools_btn.config(relief=tk.SUNKEN)
            self.exploits_btn.config(relief=tk.RAISED)

    def showadbkeyboard(self):
        try:
            subprocess.run(['python', self.file_path], check=True)
        except subprocess.CalledProcessError:
            print(f"An error occurred while running keyboard.py.")
        except FileNotFoundError:
            print(f"The file does not exist in the directory.")


    
    def show_exploits(self):
        """Switch to exploits page"""
        if self.current_button_page != "exploits":
            self.basic_tools_frame.pack_forget()
            self.exploits_frame.pack(fill=tk.BOTH, expand=True)
            self.current_button_page = "exploits"
            self.exploits_btn.config(relief=tk.SUNKEN)
            self.basic_tools_btn.config(relief=tk.RAISED)
            
            messagebox.showwarning("Warning", 
                "Exploit features may void your warranty or damage your device.\n"
                "Use at your own risk.")
    
    def create_placeholder_image(self, model_name, color):
        """Create a placeholder image for the Quest models"""
        img = Image.new('RGB', (200, 150), color)
        return ImageTk.PhotoImage(img)
    
    def check_adb_available(self):
        """Check if ADB is available on the system"""
        try:
            subprocess.run(["adb", "version"], check=True, capture_output=True, text=True)
            self.set_status("ADB is installed and ready")
        except (subprocess.SubprocessError, FileNotFoundError):
            messagebox.showerror("ADB Not Found", "Android Debug Bridge (ADB) is not found in your system PATH.\n\n"
                               "Please install ADB and make sure it's in your system PATH.")
            self.set_status("ADB not found - please install ADB")
    
    def set_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run_adb_command(self, command, get_output=False):
        """Run an ADB command and optionally return the output"""
        self.set_status(f"Running: adb {command}")
        try:
            if get_output:
                result = subprocess.run(["adb", *command.split()], check=True, capture_output=True, text=True)
                self.set_status("Command completed successfully")
                return result.stdout
            else:
                subprocess.run(["adb", *command.split()], check=True)
                self.set_status("Command completed successfully")
                return True
        except subprocess.SubprocessError as e:
            error_msg = str(e)
            self.set_status(f"Error: {error_msg}")
            messagebox.showerror("ADB Error", f"Error running ADB command:\n{error_msg}")
            return None if get_output else False
    
    def refresh_device(self):
        """Refresh connected device information"""
        self.set_status("Scanning for connected Quest devices...")
        threading.Thread(target=self._refresh_device_thread, daemon=True).start()
    
    def _refresh_device_thread(self):
        """Background thread for device refresh"""
        devices_output = self.run_adb_command("devices", get_output=True)
        if not devices_output:
            self.update_ui_no_device()
            return
        
        devices = re.findall(r'^(\S+)\s+device$', devices_output, re.MULTILINE)
        if not devices:
            self.update_ui_no_device()
            return
        
        self.current_device = devices[0]

        self.device_info = {}
        try:
            model = self.run_adb_command("shell getprop ro.product.model", get_output=True).strip()
            self.device_info["model"] = model
            if "Quest" in model:
                self.device_info["quest_version"] = model
            else:
                hardware = self.run_adb_command("shell getprop ro.hardware", get_output=True).strip()
                if "monterey" in hardware.lower():
                    self.device_info["quest_version"] = "Quest 1"
                elif "hollywood" in hardware.lower():
                    self.device_info["quest_version"] = "Quest 2"
                elif "eureka" in hardware.lower():
                    self.device_info["quest_version"] = "Quest 3"
                elif "eureka-s" in hardware.lower():
                    self.device_info["quest_version"] = "Quest 3S"
                else:
                    self.device_info["quest_version"] = "Unknown"
                
            self.device_info["serial"] = self.run_adb_command("shell getprop ro.serialno", get_output=True).strip()
            
            self.device_info["firmware"] = self.run_adb_command("shell getprop ro.build.version.release", get_output=True).strip()
            
            self.device_info["build"] = self.run_adb_command("shell getprop ro.build.display.id", get_output=True).strip()
            
            storage_output = self.run_adb_command("shell df -h /sdcard", get_output=True)

            storage_match = re.search(r'/dev/fuse\s+(\S+)\s+(\S+)\s+(\S+)', storage_output)

            if storage_match:
                self.device_info["storage_total"] = storage_match.group(1)
                self.device_info["storage_used"] = storage_match.group(2)
                self.device_info["storage_free"] = storage_match.group(3)

            self.device_info["device_name"] = self.run_adb_command("shell getprop ro.product.name", get_output=True).strip()
            self.device_info["cpu_info"] = self.run_adb_command("shell getprop ro.product.cpu.abi", get_output=True).strip()
            
            battery_output = self.run_adb_command("shell dumpsys battery", get_output=True)
            battery_match = re.search(r'level: (\d+)', battery_output)
            if battery_match:
                self.device_info["battery"] = f"{battery_match.group(1)}%"

            charging_match = re.search(r'AC powered: (\w+)', battery_output)
            if charging_match and charging_match.group(1).lower() == "true":
                self.device_info["charging"] = "Yes"
            else:
                self.device_info["charging"] = "No"

            self.root.after(0, self.update_ui_with_device)
            
        except Exception as e:
            self.set_status(f"Error collecting device information: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to collect device information:\n{str(e)}"))
    
    def update_ui_no_device(self):
        """Update UI when no device is connected"""
        self.root.after(0, lambda: self.device_name_label.config(text="No device connected"))
        self.root.after(0, lambda: self.device_image_label.config(image=self.placeholder_images["Unknown"]))

        self.root.after(0, lambda: self.update_text_widget(self.system_info_text, "No device connected"))

        self.root.after(0, lambda: self.update_text_widget(self.additional_info_text, "Connect a Quest device to see additional information"))
        
        self.root.after(0, lambda: self.set_status("No Quest device detected"))

    def sideload_apk(self):
            try:
                apk_path = filedialog.askopenfilename(
                    title="Select APK to Sideload",
                    filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
                )
                
                if not apk_path:
                    print("No APK file selected. Cancelling operation.")
                    return
                
                print(f"Starting sideload process for {apk_path}...")
                print(f"Installing APK from {apk_path}...")

                subprocess.run(["adb", "install", apk_path], check=True)

                print("Sideload completed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error during sideload: {e}")

            except Exception as e:
                print(f"Unexpected error: {e}")


    def update_ui_with_device(self):
        """Update UI with device information."""
        quest_version = self.device_info.get("quest_version", "Unknown").strip()
        print(f"Detected Quest version: {quest_version}")
    
        if quest_version == "Unknown":
            self.after(5000, self.update_ui_with_device)
            return
    
        self.device_name_label.config(text=quest_version)

        print(f"Available keys in placeholder_images: {self.placeholder_images.keys()}")

        image = self.placeholder_images.get(quest_version, self.placeholder_images["Unknown"])

        print(f"Selected image for {quest_version}: {image}")
    
        self.device_image_label.config(image=image)
        self.device_image_label.image = image
        system_info = (
            f"Serial: {self.device_info.get('serial', 'N/A')}\n"
            f"Firmware: {self.device_info.get('firmware', 'N/A')}\n"
            f"Build: {self.device_info.get('build', 'N/A')}\n"
            f"Model: {self.device_info.get('model', 'N/A')}\n"
            f"Battery: {self.device_info.get('battery', 'N/A')}\n"
            f"Charging: {self.device_info.get('charging', 'N/A')}\n"
            
        )
        self.update_text_widget(self.system_info_text, system_info)

        additional_info = (
            f"Device Name: {self.device_info.get('device_name', 'N/A')}\n"
            f"CPU Architecture: {self.device_info.get('cpu_info', 'N/A')}\n\n"
            f"Storage Information:\n"
            f"  Total: {self.device_info.get('storage_total', 'N/A')}\n"
            f"  Used: {self.device_info.get('storage_used', 'N/A')}\n"
            f"  Free: {self.device_info.get('storage_free', 'N/A')}\n\n"
            f"ADB Device ID: {self.current_device}"
        )
        self.update_text_widget(self.additional_info_text, additional_info)

        self.set_status(f"Connected to {quest_version} device")
        
    def get_memory_info(self):
        try:
            result = subprocess.run(["adb", "shell", "cat", "/proc/meminfo"], capture_output=True, text=True)
            output = result.stdout
            lines = output.splitlines()
            mem_total = int(lines[0].split()[1]) / (1024 * 1024) 
            mem_free = int(lines[1].split()[1]) / (1024 * 1024)
            mem_available = int(lines[2].split()[1]) / (1024 * 1024)
            return mem_total, mem_free, mem_available
        except Exception as e:
            print(f"Error: {e}")
            return None

    
    def update_text_widget(self, widget, text):
        """Update a text widget with new content"""
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    def disconnect_controllers(self):
        """Disconnect all Bluetooth controllers"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        result = messagebox.askyesno("Disconnect Controllers", 
                                   "This will disconnect all paired controllers.\nContinue?")
        if result:
            self.run_adb_command("shell am broadcast -a android.bluetooth.adapter.action.REQUEST_DISABLE")
            self.set_status("Controller disconnect request sent")
    
    def list_installed_apps(self):
        """List installed apps on the device"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        self.set_status("Fetching installed apps...")
        apps_output = self.run_adb_command("shell pm list packages -3", get_output=True)
        
        if apps_output:
            packages = re.findall(r'package:(.*)', apps_output)
            formatted_apps = "\n".join(packages)
            app_window = tk.Toplevel(self.root)
            app_window.title("Installed Apps")
            app_window.geometry("500x400")
            frame = tk.Frame(app_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            label = tk.Label(frame, text=f"Installed Apps on {self.device_info.get('quest_version', 'Device')}", font=("Arial", 12, "bold"))
            label.pack(pady=(0, 10))
            
            text_area = tk.Text(frame, wrap=tk.WORD)
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame, command=text_area.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_area.config(yscrollcommand=scrollbar.set)
            
            text_area.insert(tk.END, formatted_apps)
            text_area.config(state=tk.DISABLED)
            
            self.set_status("Installed apps retrieved successfully")
        else:
            self.set_status("Failed to retrieve installed apps")
    
    def get_battery_status(self):
        """Get detailed battery status"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        self.set_status("Fetching battery information...")
        battery_output = self.run_adb_command("shell dumpsys battery", get_output=True)
        
        if battery_output:
            battery_window = tk.Toplevel(self.root)
            battery_window.title("Battery Status")
            battery_window.geometry("400x300")
            frame = tk.Frame(battery_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            label = tk.Label(frame, text=f"Battery Status for {self.device_info.get('quest_version', 'Device')}", font=("Arial", 12, "bold"))
            label.pack(pady=(0, 10))
            
            text_area = tk.Text(frame, wrap=tk.WORD)
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame, command=text_area.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_area.config(yscrollcommand=scrollbar.set)
            
            text_area.insert(tk.END, battery_output)
            text_area.config(state=tk.DISABLED)
            
            self.set_status("Battery information retrieved successfully")
        else:
            self.set_status("Failed to retrieve battery information")

    def factory_reset(self):
        """Factory reset the device"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        result = messagebox.askyesno("Warning", 
                                   "This will FACTORY RESET your device and DELETE ALL DATA.\n\n"
                                   "This action cannot be undone!\n\n"
                                   "Are you absolutely sure you want to continue?",
                                   icon="warning")
        if result:
            confirm = messagebox.askyesno("Final Warning",
                                        "ALL DATA WILL BE LOST!\n\n"
                                        "Press YES to confirm factory reset.",
                                        icon="warning")
            if confirm:
                self.set_status("Performing factory reset...")
                self.run_adb_command("shell am broadcast -a android.intent.action.MASTER_CLEAR")
                messagebox.showinfo("Factory Reset", "Factory reset command sent to device.")
    
    def authexploit(self):
        """Automates opening, uninstalling, and sideloading an APK on Quest 2"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return

        apk_path = filedialog.askopenfilename(title="Select Modded APK", filetypes=[("APK files", "*.apk")])
        if not apk_path:
            messagebox.showwarning("No APK Selected", "You must select a modded APK file.")
            return

        package_name = simpledialog.askstring("Package Name", "Enter the package name of the app to replace:")
        if not package_name:
            messagebox.showwarning("No Package Name", "You must enter a package name.")
            return

        self.set_status("Waking up headset and disabling proximity sensor...")

        self.run_adb_command("shell input keyevent KEYCODE_WAKEUP")

        self.run_adb_command("shell setprop debug.oculus.disable_proximity true")

        self.set_status(f"Checking if {package_name} is installed...")

        package_list = subprocess.run(["adb", "shell", "pm", "list", "packages"], capture_output=True, text=True).stdout

        print("ADB Package List Output:", package_list)

        if not package_list or not isinstance(package_list, str) or "package:" not in package_list:
            messagebox.showerror("Error", "Failed to retrieve package list from device. Please check ADB connection.")
            self.run_adb_command("shell setprop debug.oculus.disable_proximity false")
            return
        installed_packages = [pkg.replace("package:", "").strip() for pkg in package_list.splitlines()]
        
        print("Processed Package List:", installed_packages)

        if package_name not in installed_packages:
            messagebox.showerror("Package Not Found", f"The package '{package_name}' is not installed on the device.")
            self.run_adb_command("shell setprop debug.oculus.disable_proximity false")
            return

        self.set_status(f"Opening {package_name} for 10 seconds...")
        self.run_adb_command(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")

        time.sleep(10)

        self.set_status(f"Closing {package_name}...")
        self.run_adb_command(f"shell am force-stop {package_name}")

        self.set_status(f"Uninstalling {package_name}...")
        if not self.run_adb_command(f"uninstall {package_name}"):
            messagebox.showerror("Uninstall Failed", f"Failed to uninstall {package_name}.")
            self.run_adb_command("shell setprop debug.oculus.disable_proximity false")
            return

        self.set_status(f"Sideloading modded APK...")
        if not self.run_adb_command(f"install \"{apk_path}\""):
            messagebox.showerror("Install Failed", "Failed to sideload the modded APK.")
            self.run_adb_command("shell setprop debug.oculus.disable_proximity false")
            return
        self.run_adb_command("shell setprop debug.oculus.disable_proximity false")

        messagebox.showinfo("Success", f"Modded APK installed successfully for {package_name}.")
        self.set_status("Operation complete")





    
    def disable_guardian(self):
        """Disable guardian system"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        result = messagebox.askyesno("Disable Guardian", 
                                   "Disabling the Guardian system may be unsafe and could lead to physical injury.\n\n"
                                   "Do you want to continue?",
                                   icon="warning")
        if result:
            self.set_status("Disabling Guardian system...")
            if self.run_adb_command("shell setprop debug.oculus.guardian_pause 1"):
                messagebox.showinfo("Guardian Disabled", "Guardian system has been temporarily disabled.\n\nBe careful when using the headset!")
                self.set_status("Guardian system disabled")
            else:
                self.set_status("Failed to disable Guardian system")

    def enable_guardian(self):
        """Enable Guardian system"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
        
        self.set_status("Enabling Guardian system...")
        if self.run_adb_command("shell setprop debug.oculus.guardian_pause 1"):
            messagebox.showinfo("Guardian Enabled", "Oh yeah.")
            self.set_status("Guardian system enabled")
        else:
            self.set_status("Failed to enable Guardian system")
    
    def authexploitnew(self):
        try:
            apk_path = input("Enter the path to the APK file: ").strip()
            package_name = input("Enter the package name to uninstall: ").strip()
            
            if not os.path.exists(apk_path):
                print(f"Error: APK file not found at {apk_path}")
                return
            
            if not package_name:
                print("Error: Package name cannot be empty")
                return
            
            print(f"Starting auth process for {package_name}...")
            
            subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_WAKEUP"], check=True)
            print("Headset awakened")
            
            subprocess.run(["adb", "shell", "am", "broadcast", "-a", "com.oculus.vrpowermanager.prox_close"], check=True)
            print("Proximity sensor disabled")
            
            try:
                print(f"Opening {package_name}...")
                subprocess.run(["adb", "shell", "monkey", "-p", package_name, "1"], check=True)
                
                time.sleep(10)
                
                print(f"Uninstalling {package_name}...")
                subprocess.run(["adb", "shell", "pm", "uninstall", package_name], check=True)
                
                print(f"Installing new APK from {apk_path}...")
                subprocess.run(["adb", "install", apk_path], check=True)
                
                print("Process completed successfully!")
                
            except subprocess.CalledProcessError as e:
                print(f"Error during process: {e}")
            finally:
                subprocess.run(["adb", "shell", "am", "broadcast", "-a", "com.oculus.vrpowermanager.automation_disable"], check=True)
                print("Proximity sensor re-enabled")
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            try:
                subprocess.run(["adb", "shell", "am", "broadcast", "-a", "com.oculus.vrpowermanager.automation_disable"], check=True)
                print("Proximity sensor re-enabled")
            except:
                print("Failed to re-enable proximity sensor")

    
    def remove_lock_pattern(self):
        """Remove lock pattern/PIN"""
        if not self.current_device:
            messagebox.showinfo("No Device", "No Quest device connected")
            return
            
        result = messagebox.askyesno("Remove Lock Pattern", 
                                   "This will attempt to remove the lock pattern/PIN from your device.\n\n"
                                   "This may require device reset if unsuccessful.\n\n"
                                   "Do you want to continue?",
                                   icon="warning")
        if result:
            self.set_status("Attempting to remove lock pattern/PIN...")
            commands = [
                "shell rm /data/system/gesture.key",
                "shell rm /data/system/password.key",
                "shell rm /data/system/locksettings.db",
                "shell rm /data/system/locksettings.db-wal",
                "shell rm /data/system/locksettings.db-shm"
            ]
            
            success = True
            for cmd in commands:
                if not self.run_adb_command(cmd):
                    success = False
            
            if success:
                messagebox.showinfo("Lock Removed", "Lock pattern/PIN removal commands sent.\n\nDevice may need to be restarted.")
                self.set_status("Lock removal commands completed")
            else:
                messagebox.showinfo("Lock Removal Failed", "Failed to remove lock pattern/PIN.\n\nDevice may need to be rooted for this operation.")
                self.set_status("Lock removal failed")

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = QuestDiagnosticsTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()

