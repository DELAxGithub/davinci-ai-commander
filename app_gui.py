import customtkinter as ctk
import os
import re
import subprocess
import sys
import threading
import google.generativeai as genai
import textwrap
from dvr import load_resolve  # Reuse the loader from dvr.py

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Keychain service/account identifiers
KEYCHAIN_SERVICE = "DaVinciAICommander"
KEYCHAIN_ACCOUNT = "GeminiAPIKey"

# Patterns blocked in AI-generated code
BLOCKED_PATTERNS = [
    r'\bimport\s+subprocess\b',
    r'\bfrom\s+subprocess\b',
    r'\bimport\s+shutil\b',
    r'\bfrom\s+shutil\b',
    r'\bos\.system\b',
    r'\bos\.popen\b',
    r'\bos\.remove\b',
    r'\bos\.unlink\b',
    r'\bos\.rmdir\b',
    r'\bos\.rename\b',
    r'\bshutil\.rmtree\b',
    r'\b__import__\b',
    r'\beval\s*\(',
    r'\bexec\s*\(',
    r'\bopen\s*\(.+["\']w',  # file write operations
]

GEMINI_MODEL = "gemini-2.5-flash"

SAMPLE_COMMANDS = [
    "Create bins case01 to case10",
    "List all clips in the current timeline",
    "Set all clip colors to blue in the timeline",
    "Add a marker at the current frame with note 'Review this'",
    "Show project framerate and resolution",
]


def keychain_load() -> str:
    """Load API key from macOS Keychain."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password",
             "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT, "-w"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def keychain_save(key: str) -> bool:
    """Save API key to macOS Keychain (add or update)."""
    try:
        subprocess.run(
            ["security", "add-generic-password",
             "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT,
             "-w", key, "-U"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        return True
    except Exception:
        return False


def validate_code(code: str) -> tuple[bool, str]:
    """Check AI-generated code for dangerous patterns. Returns (ok, reason)."""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, code):
            return False, f"Blocked: dangerous pattern detected ({pattern})"
    return True, ""


class DaVinciAgentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("DaVinci AI Commander")
        self.geometry("700x800")
        self.minsize(500, 400)

        # --- Internal State ---
        self.api_key = ""
        self.resolve = None
        self.project_manager = None
        self.media_pool = None
        self.command_history: list[str] = []
        self.history_index = -1

        # --- GUI Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Output Console (Text Box)
        self.console_frame = ctk.CTkFrame(self)
        self.console_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.console_textbox = ctk.CTkTextbox(self.console_frame, font=("Menlo", 12))
        self.console_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.console_textbox.configure(state="disabled")

        # 2. Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Command (e.g., 'Create bins case23 to case30')...")
        self.prompt_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        self.prompt_entry.bind("<Return>", self.start_processing_thread)
        self.prompt_entry.bind("<Up>", self.history_prev)
        self.prompt_entry.bind("<Down>", self.history_next)

        self.run_button = ctk.CTkButton(self.input_frame, text="Execute", command=self.start_processing_thread, width=100)
        self.run_button.pack(side="right", padx=(0, 10), pady=10)

        # 3. Footer / Settings
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.status_label = ctk.CTkLabel(self.settings_frame, text="Status: Starting...", text_color="gray")
        self.status_label.pack(side="left")

        self.api_key_button = ctk.CTkButton(self.settings_frame, text="Set API Key", command=self.open_api_key_dialog, height=24, width=80)
        self.api_key_button.pack(side="right")

        # --- Initial Tasks ---
        self.show_welcome()
        self.load_api_key()
        self.connect_davinci()

    def log(self, message):
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", message + "\n")
        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")

    def show_welcome(self):
        self.log("DaVinci AI Commander v1.0.0")
        self.log("=" * 40)
        self.log("")
        self.log("Example commands:")
        for cmd in SAMPLE_COMMANDS:
            self.log(f"  - {cmd}")
        self.log("")

    def load_api_key(self):
        """Load API key from Keychain, then fall back to environment."""
        key = keychain_load()
        if key:
            self.api_key = key
            self.log("API Key loaded from Keychain.")
            return
        key = os.getenv("GEMINI_API_KEY", "")
        if key:
            self.api_key = key
            self.log("API Key loaded from environment.")
            keychain_save(key)  # migrate to Keychain
            return
        self.log("No API Key found. Click 'Set API Key' to configure.")

    def open_api_key_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter Google Gemini API Key:", title="API Key")
        key = dialog.get_input()
        if key:
            self.api_key = key.strip()
            if keychain_save(self.api_key):
                self.log("API Key saved to Keychain.")
            else:
                os.environ["GEMINI_API_KEY"] = self.api_key
                self.log("API Key updated (Keychain save failed, using session only).")

    # --- Command History ---

    def history_prev(self, event=None):
        if not self.command_history:
            return "break"
        if self.history_index == -1:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.prompt_entry.delete(0, "end")
        self.prompt_entry.insert(0, self.command_history[self.history_index])
        return "break"

    def history_next(self, event=None):
        if not self.command_history:
            return "break"
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.prompt_entry.delete(0, "end")
            self.prompt_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = -1
            self.prompt_entry.delete(0, "end")
        return "break"

    # --- DaVinci Resolve Connection ---

    def connect_davinci(self):
        self.log("Connecting to DaVinci Resolve...")
        try:
            self.resolve = load_resolve()
            if self.resolve:
                self.project_manager = self.resolve.GetProjectManager()
                self.project = self.project_manager.GetCurrentProject()
                if self.project:
                    self.media_pool = self.project.GetMediaPool()
                    self.log(f"Connected to Project: {self.project.GetName()}")
                    self.status_label.configure(text="Status: Connected", text_color="green")
                else:
                    self.log("Connected to Resolve, but no project is open.")
                    self.log("  -> Open a project in Resolve, then restart this app.")
                    self.status_label.configure(text="Status: No Project", text_color="orange")
            else:
                self.log("Could not connect to DaVinci Resolve.")
                self.log("  -> Make sure DaVinci Resolve is running.")
                self.log("  -> Go to Resolve > Preferences > System > General")
                self.log("     and enable 'External scripting using' = Local.")
                self.status_label.configure(text="Status: Disconnected", text_color="red")
        except Exception as e:
            self.log(f"Connection Error: {e}")
            self.log("  -> Is DaVinci Resolve installed and running?")
            self.status_label.configure(text="Status: Error", text_color="red")

    def start_processing_thread(self, event=None):
        if not self.api_key:
            self.log("Error: No API Key configured. Click 'Set API Key'.")
            return

        user_input = self.prompt_entry.get()
        if not user_input.strip():
            return

        # Save to command history
        if not self.command_history or self.command_history[-1] != user_input:
            self.command_history.append(user_input)
        self.history_index = -1

        self.run_button.configure(state="disabled")
        self.prompt_entry.configure(state="disabled")
        self.status_label.configure(text="Status: Thinking...", text_color="yellow")

        threading.Thread(target=self.process_request, args=(user_input,), daemon=True).start()

    def process_request(self, user_input):
        try:
            self.log(f"\n> {user_input}")

            # 1. Generate Code using Gemini
            try:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(GEMINI_MODEL)
            except Exception as e:
                self.log(f"API configuration error: {e}")
                self.log("  -> Check your API key or internet connection.")
                return

            system_instruction = """
            You are a Python coding assistant for DaVinci Resolve.
            Your task is to translate the user's natural language request into a valid Python code block
            that uses the DaVinci Resolve Scripting API.

            CONTEXT VARIABLES AVAILABLE:
            - resolve (The Resolve object)
            - project (The generic Project object)
            - media_pool (The MediaPool object)
            - root_folder (The generic root folder object)

            RULES:
            1. You MUST wrap the code in ```python ... ``` markdown block.
            2. Do NOT import DaVinciResolveScript. Assume objects provided.
            3. Use simple, direct API calls.
            4. If creating bins, use media_pool.AddSubFolder(root_folder, "name").
            5. If deleting bins, iterate through `root_folder.GetSubFolderList()`. Do NOT use `FindSubFolder()`.
            6. If the user specifies a range (e.g., "case31-45"), parse the numbers and iterate.
            7. Do NOT use subprocess, os.system, shutil, eval, exec, or __import__.
            8. Do NOT open files for writing. Only read operations are allowed.

            NEGATIVE CONSTRAINTS (YOU CANNOT DO THESE):
            - You CANNOT edit video content (pixels), apply effects, or color grade clips directly.
            - You CANNOT "watch" or "analyze" the video content.
            - You CANNOT know if a video is "funny" or "good".
            - You CANNOT interact with OS UI elements (mouse clicks, key presses).
            - You CANNOT use `FindSubFolder()` (it does not exist). Use `GetSubFolderList()`.

            IF THE REQUEST VIOLATES CONSTRAINTS OR IS IMPOSSIBLE:
            Return exactly and ONLY this line of code:
            print("ERROR: I cannot fulfill this request because it is outside the capabilities of the DaVinci Resolve Scripting API.")

            Example Request: "Make the video funnier"
            Example Output:
            print("ERROR: I cannot fulfill this request because it is outside the capabilities of the DaVinci Resolve Scripting API.")
            """

            full_prompt = f"{system_instruction}\n\nUser Request: {user_input}\nCode:"

            try:
                response = model.generate_content(full_prompt)
                raw_text = response.text
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg or "401" in error_msg:
                    self.log("Error: Invalid API key. Please update via 'Set API Key'.")
                elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    self.log("Error: API rate limit reached. Please wait a moment.")
                elif "timeout" in error_msg.lower():
                    self.log("Error: API request timed out. Check your internet connection.")
                else:
                    self.log(f"API Error: {e}")
                return

            # Extract code block
            code_match = re.search(r"```python(.*?)```", raw_text, re.DOTALL)
            if code_match:
                generated_code = code_match.group(1).strip()
            else:
                code_match_generic = re.search(r"```(.*?)```", raw_text, re.DOTALL)
                if code_match_generic:
                    generated_code = code_match_generic.group(1).strip()
                else:
                    generated_code = raw_text.strip()

            self.log(f"Generated Code:\n{textwrap.indent(generated_code, '  ')}")

            # Validate generated code before execution
            is_safe, reason = validate_code(generated_code)
            if not is_safe:
                self.log(f"Safety check failed: {reason}")
                self.log("Code was NOT executed.")
                return

            # 2. Execute Code
            if not self.resolve:
                self.log("Error: Not connected to DaVinci Resolve. Cannot execute.")
                self.log("  -> Restart the app with Resolve running.")
                return

            project = self.project_manager.GetCurrentProject()
            if not project:
                self.log("Error: No current project in Resolve.")
                return
            media_pool = project.GetMediaPool()
            root_folder = media_pool.GetRootFolder()

            local_scope = {
                "resolve": self.resolve,
                "project": project,
                "media_pool": media_pool,
                "root_folder": root_folder,
                "print": lambda *args: self.log(" ".join(map(str, args))),
            }

            self.log("Executing...")
            exec(generated_code, {"__builtins__": {}}, local_scope)
            self.log("Done.")

        except Exception as e:
            self.log(f"Execution Error: {e}")
        finally:
            self.after(0, self._reset_ui)

    def _reset_ui(self):
        self.status_label.configure(text="Status: Ready", text_color="green" if self.resolve else "red")
        self.run_button.configure(state="normal")
        self.prompt_entry.configure(state="normal")
        self.prompt_entry.delete(0, "end")
        self.prompt_entry.focus()

if __name__ == "__main__":
    app = DaVinciAgentApp()
    app.mainloop()
