import customtkinter as ctk
import os
import sys
import threading
import google.generativeai as genai
import textwrap
from dvr import load_resolve  # Reuse the loader from dvr.py

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DaVinciAgentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("DaVinci AI Commander")
        self.geometry("600x700")
        
        # --- Internal State ---
        self.api_key = ""
        self.resolve = None
        self.project_manager = None
        self.media_pool = None
        
        # --- GUI Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Output Console (Text Box)
        self.console_frame = ctk.CTkFrame(self)
        self.console_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        self.console_textbox = ctk.CTkTextbox(self.console_frame, font=("Menlo", 12))
        self.console_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.console_textbox.insert("0.0", "Initialize DaVinci Connection...\n")
        self.console_textbox.configure(state="disabled")

        # 2. Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Command (e.g., 'Create bins case23 to case30')...")
        self.prompt_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        self.prompt_entry.bind("<Return>", self.start_processing_thread)

        self.run_button = ctk.CTkButton(self.input_frame, text="Execute", command=self.start_processing_thread, width=100)
        self.run_button.pack(side="right", padx=(0, 10), pady=10)

        # 3. Footer / Settings
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.status_label = ctk.CTkLabel(self.settings_frame, text="Status: Ready", text_color="gray")
        self.status_label.pack(side="left")
        
        self.api_key_button = ctk.CTkButton(self.settings_frame, text="Set API Key", command=self.open_api_key_dialog, height=24, width=80)
        self.api_key_button.pack(side="right")

        # --- Initial Tasks ---
        self.check_env()
        self.connect_davinci()

    def log(self, message):
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", message + "\n")
        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")

    def check_env(self):
        # Allow user to set GEMINI_API_KEY env var beforehand
        key = os.getenv("GEMINI_API_KEY")
        if key:
            self.api_key = key
            self.log(f"API Key loaded from environment.")

    def open_api_key_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter Google Gemini API Key:", title="API Key")
        key = dialog.get_input()
        if key:
            self.api_key = key.strip()
            os.environ["GEMINI_API_KEY"] = self.api_key # Update env for session
            self.log("API Key updated.")

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
                    self.status_label.configure(text="Status: No Project", text_color="orange")
            else:
                self.log("Could not find DaVinci Resolve API.")
                self.log("Make sure environment variables are set or DaVinci is open.")
                self.status_label.configure(text="Status: Disconnected", text_color="red")
        except Exception as e:
            self.log(f"Connection Error: {e}")

    def start_processing_thread(self, event=None):
        if not self.api_key:
            self.log("Error: Please set API Key first.")
            return
        
        user_input = self.prompt_entry.get()
        if not user_input.strip():
            return
        
        self.run_button.configure(state="disabled")
        self.prompt_entry.configure(state="disabled")
        self.status_label.configure(text="Status: Thinking...")
        
        threading.Thread(target=self.process_request, args=(user_input,), daemon=True).start()

    def process_request(self, user_input):
        try:
            self.log(f"\n> {user_input}")
            
            # 1. Generate Code using Gemini
            genai.configure(api_key=self.api_key)
            # User requested "latest", so we use the alias
            model = genai.GenerativeModel('gemini-flash-latest')
            
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
            
            response = model.generate_content(full_prompt)
            raw_text = response.text
            
            # Robust extraction of code block
            import re
            code_match = re.search(r"```python(.*?)```", raw_text, re.DOTALL)
            if code_match:
                generated_code = code_match.group(1).strip()
            else:
                 # Fallback: try generic code block or just use the text
                code_match_generic = re.search(r"```(.*?)```", raw_text, re.DOTALL)
                if code_match_generic:
                    generated_code = code_match_generic.group(1).strip()
                else:
                    generated_code = raw_text.strip()
            
            # Remove any potential trailing non-code garbage if no markdown found (simple heuristics)
            # But the regex above handles the markdown case well.
            
            self.log(f"Generated Code:\n{textwrap.indent(generated_code, '  ')}")
            
            # 2. Execute Code
            if not self.resolve:
               self.log("Error: Not connected to DaVinci Resolve. Cannot execute.")
               return

            # Refresh context objects to be safe
            project = self.project_manager.GetCurrentProject()
            if not project:
                 self.log("Error: No current project.")
                 return
            media_pool = project.GetMediaPool()
            root_folder = media_pool.GetRootFolder()
            
            local_scope = {
                "resolve": self.resolve,
                "project": project,
                "media_pool": media_pool,
                "root_folder": root_folder,
                "print": lambda *args: self.log(" ".join(map(str, args))) # Override print to log to UI
            }
            
            self.log("Executing...")
            exec(generated_code, {}, local_scope)
            self.log("Execution finished.")

        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            # UI updates must happen on main thread usually, but CTk is lenient or we use after.
            # For simplicity in prototype, we'll try direct update (CTk usually handles this)
            # or use after() if strict.
            self.status_label.configure(text="Status: Ready")
            self.run_button.configure(state="normal")
            self.prompt_entry.configure(state="normal")
            self.prompt_entry.delete(0, "end")

if __name__ == "__main__":
    app = DaVinciAgentApp()
    app.mainloop()
