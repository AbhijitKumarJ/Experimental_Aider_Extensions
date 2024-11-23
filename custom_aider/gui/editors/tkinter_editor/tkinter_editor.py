"""Tkinter-based code editor with syntax highlighting and intellisense"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
from pathlib import Path
from .syntax_text import SyntaxText

class SimpleEditor:
    def __init__(self, initial_text=""):
        self.root = tk.Tk()
        self.root.title("Simple Editor")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Set up window size and position
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Create toolbar frame
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Add format selector
        ttk.Label(toolbar, text="Format:").pack(side=tk.LEFT, padx=(5, 0))
        self.format_var = tk.StringVar(value="plain")
        self.format_combo = ttk.Combobox(
            toolbar,
            textvariable=self.format_var,
            values=["plain", "markdown", "xml"], #, "python", "javascript", "html"
            state="readonly",
            width=15
        )
        self.format_combo.pack(side=tk.LEFT, padx=5)
        self.format_combo.bind('<<ComboboxSelected>>', self._on_format_changed)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create and configure text widget with syntax highlighting
        self.text_widget = SyntaxText(
            main_frame,
            wrap=tk.WORD,
            undo=True,
            font=('Courier', 12),
            padx=5,
            pady=5
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Create status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Create button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Add buttons
        save_btn = ttk.Button(button_frame, text="Save & Close", command=self.save_and_close)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add help text
        help_text = "Type @keyword for suggestions • Ctrl+S to save • Esc to cancel"
        help_label = ttk.Label(button_frame, text=help_text, foreground='gray')
        help_label.pack(side=tk.LEFT, padx=5)
        
        # Initialize result
        self.result = None
        
        # Insert initial text if provided
        if initial_text:
            self.text_widget.insert('1.0', initial_text)
            self._on_format_changed()  # Apply initial highlighting
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_and_close())
        self.root.bind('<Escape>', lambda e: self.cancel())
        
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Update status bar initially
        self._update_status()
        print("Editor initialized")  # Debug print
        
    def _on_format_changed(self, event=None):
        """Handle format selection changes"""
        format_name = self.format_var.get()
        print(f"Format changed to: {format_name}")  # Debug print
        self.text_widget.set_lexer(format_name)
        self._update_status()
        
    def _update_status(self):
        """Update the status bar with current information"""
        content = self.text_widget.get('1.0', 'end-1c')
        lines = len(content.splitlines())
        chars = len(content)
        words = len(content.split())
        format_name = self.format_var.get().upper()
        
        self.status_var.set(
            f"Format: {format_name} | Lines: {lines} | Words: {words} | "
            f"Characters: {chars}"
        )
        
    def save_and_close(self):
        """Save content and close window"""
        self.result = self.text_widget.get('1.0', 'end-1c')
        self.root.quit()
        
    def cancel(self):
        """Cancel editing and close window"""
        if messagebox.askokcancel("Cancel", "Are you sure you want to cancel editing?"):
            self.result = None
            self.root.quit()
    
    def run(self):
        """Run the editor window"""
        self.root.mainloop()
        self.root.destroy()
        return self.result

def main():
    """Run the editor as a standalone program"""
    # Get initial text from stdin if available
    if not sys.stdin.isatty():
        initial_text = sys.stdin.read()
    else:
        initial_text = ""
        
    # Create and run editor
    editor = SimpleEditor(initial_text)
    result = editor.run()
    
    # Output result to stdout if save was clicked
    if result is not None:
        print(result)
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())