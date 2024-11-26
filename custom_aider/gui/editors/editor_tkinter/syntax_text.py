"""Base syntax highlighting text widget with intellisense"""
import tkinter as tk
from tkinter import ttk
from pygments import lex
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.lexers.markup import MarkdownLexer, XmlLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.html import HtmlLexer
import re
import json
from pathlib import Path

class SyntaxText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create tags dictionary and suggestion window
        self.tags = {}
        self.suggestion_window = None
        self.suggestion_var = None
        self.suggestion_list = None
        
        # Load keywords file if exists
        self.keywords = self._load_keywords()
        
        # Create tags with specific colors
        self._create_tags()
        
        # Bind events for live updating
        self.bind('<KeyRelease>', self._on_key_release)
        self.bind('<KeyPress>', self._on_key_press)
        self.bind('<<Paste>>', self._on_paste)
        self.bind('<<Cut>>', self._on_text_change)
        
        # Special key bindings for suggestions
        self.bind('<Up>', self._navigate_suggestions)
        self.bind('<Down>', self._navigate_suggestions)
        self.bind('<Return>', self._insert_suggestion)
        self.bind('<Tab>', self._insert_suggestion)
        self.bind('<Escape>', self._hide_suggestions)
        
        # Initialize with TextLexer
        self._lexer = TextLexer()
        print("SyntaxText initialized")  # Debug print
        
    def _load_keywords(self):
        """Load keywords from .extn_aider.keywords.json"""
        try:
            keywords_file = Path.cwd() /  '.extn_aider' / '.extn_aider.keywords.json'
            if keywords_file.exists():
                with open(keywords_file) as f:
                    return json.load(f)
            print("No keywords file found")  # Debug print
            return {}
        except Exception as e:
            print(f"Error loading keywords: {e}")  # Debug print
            return {}

    def _create_tags(self):
        """Create basic tags for different code elements"""
        # Keywords - blue
        self.tag_configure("keyword", foreground="#0000FF")
        self.tags["keyword"] = "keyword"
        
        # Strings - green
        self.tag_configure("string", foreground="#008000")
        self.tags["string"] = "string"
        
        # Comments - gray
        self.tag_configure("comment", foreground="#808080")
        self.tags["comment"] = "comment"
        
        # Functions - purple
        self.tag_configure("function", foreground="#800080")
        self.tags["function"] = "function"
        
        # HTML tags - dark red
        self.tag_configure("tag", foreground="#800000")
        self.tags["tag"] = "tag"
        
        print("Tags created:", self.tags)  # Debug print
        
    def set_lexer(self, lexer_name):
        """Set the lexer based on the format"""
        try:
            self._lexer = {
                'plain': TextLexer(),
                'python': PythonLexer(),
                'javascript': JavascriptLexer(),
                'html': HtmlLexer(),
                'xml': XmlLexer(),
                'markdown': MarkdownLexer()
            }[lexer_name]
            print(f"Lexer set to: {lexer_name}")  # Debug print
            self.highlight_text()
        except Exception as e:
            print(f"Error setting lexer: {e}")  # Debug print
            self._lexer = TextLexer()

    def _get_word_before_cursor(self):
        """Get the word being typed before the cursor"""
        try:
            cursor_pos = self.index("insert")
            line_start = self.index(f"{cursor_pos} linestart")
            line = self.get(line_start, cursor_pos)
            
            # Find last word with @ pattern
            match = re.search(r'@[\w-]*$', line)
            if match:
                return match.group()
        except Exception as e:
            print(f"Error getting word: {e}")
        return None

    def _show_suggestions(self, word):
        """Show suggestion window with matching keywords"""
        if not word or not word.startswith('@'):
            return self._hide_suggestions()
            
        # Get matching keywords
        prefix = word[1:]  # Remove @ symbol
        matches = []
        for key, value in self.keywords.items():
            if key.startswith(prefix):
                matches.append((f"@{key}", value))
                
        if not matches:
            return self._hide_suggestions()
            
        # Create or update suggestion window
        if not self.suggestion_window:
            # Create suggestion window
            self.suggestion_window = tk.Toplevel()
            self.suggestion_window.withdraw()  # Hide initially
            self.suggestion_window.overrideredirect(True)  # No window decorations
            
            # Create listbox for suggestions
            self.suggestion_var = tk.StringVar()
            self.suggestion_list = tk.Listbox(
                self.suggestion_window,
                listvariable=self.suggestion_var,
                selectmode=tk.SINGLE,
                height=5,
                font=self.cget('font')
            )
            self.suggestion_list.pack(fill=tk.BOTH, expand=True)
            
        # Update suggestions
        suggestions = [f"{key} - {value}" for key, value in matches]
        self.suggestion_var.set(suggestions)
        
        # Position window near cursor
        x, y, _, h = self.bbox("insert")
        x += self.winfo_rootx()
        y += self.winfo_rooty() + h
        
        self.suggestion_window.geometry(f"+{x}+{y}")
        self.suggestion_window.deiconify()
        
        # Select first item
        self.suggestion_list.selection_clear(0, tk.END)
        self.suggestion_list.selection_set(0)

    def _hide_suggestions(self, event=None):
        """Hide the suggestion window"""
        if self.suggestion_window:
            self.suggestion_window.withdraw()
        return "break"

    def _navigate_suggestions(self, event):
        """Handle up/down navigation in suggestions"""
        if not self.suggestion_window or not self.suggestion_window.winfo_viewable():
            return
            
        current = self.suggestion_list.curselection()
        if not current:
            return "break"
            
        if event.keysym == 'Up' and current[0] > 0:
            self.suggestion_list.selection_clear(current)
            self.suggestion_list.selection_set(current[0] - 1)
        elif event.keysym == 'Down' and current[0] < self.suggestion_list.size() - 1:
            self.suggestion_list.selection_clear(current)
            self.suggestion_list.selection_set(current[0] + 1)
            
        return "break"

    def _insert_suggestion(self, event=None):
        """Insert the selected suggestion"""
        if not self.suggestion_window or not self.suggestion_window.winfo_viewable():
            return
            
        selection = self.suggestion_list.curselection()
        if not selection:
            return "break"
            
        # Get selected suggestion text (just the key part)
        full_text = self.suggestion_list.get(selection[0])
        suggestion = full_text.split(' - ')[1].strip()
        
        # Get the word being replaced
        cursor_pos = self.index("insert")
        line_start = self.index(f"{cursor_pos} linestart")
        line = self.get(line_start, cursor_pos)
        match = re.search(r'@[\w-]*$', line)
        
        if match:
            # Replace the partial word with the suggestion
            start = f"{cursor_pos} - {len(match.group())}c"
            end = cursor_pos
            self.delete(start, end)
            self.insert(cursor_pos, suggestion[0:])  # Remove @ from insertion
            
        self._hide_suggestions()
        return "break"

    def _on_key_press(self, event):
        """Handle key press events"""
        if event.char.isspace():
            self._hide_suggestions()
            
    def _on_key_release(self, event):
        """Handle key release events"""
        if event.char and event.char.isprintable():
            word = self._get_word_before_cursor()
            if word:
                self._show_suggestions(word)
            
        if not hasattr(self, '_highlight_pending'):
            self._highlight_pending = False
            
        if not self._highlight_pending:
            self._highlight_pending = True
            self.after(100, self._on_text_change)
            
    def _on_paste(self, event=None):
        """Handle paste events"""
        self.after(1, self._on_text_change)
        
    def _on_text_change(self, event=None):
        """Handle any text change"""
        if hasattr(self, '_highlight_pending'):
            self._highlight_pending = False
        self.highlight_text()
        
    def _map_token_to_tag(self, token_type):
        """Map a pygments token type to our tag names"""
        token_str = str(token_type).lower()
        if 'keyword' in token_str:
            return 'keyword'
        elif 'string' in token_str:
            return 'string'
        elif 'comment' in token_str:
            return 'comment'
        elif 'function' in token_str or 'name.function' in token_str:
            return 'function'
        elif 'name.tag' in token_str:
            return 'tag'
        return None

    def _remove_all_tags(self):
        """Remove all syntax highlighting tags"""
        for tag in self.tags.values():
            self.tag_remove(tag, "1.0", "end")

    def highlight_text(self):
        """Apply syntax highlighting to the text"""
        print("Highlighting text...")  # Debug print
        
        # Get the current text
        text = self.get("1.0", "end-1c")
        
        # Remove existing tags
        self._remove_all_tags()
        
        try:
            # Get token position mappings
            token_positions = []
            pos = 0
            
            # Tokenize the text
            for token, value in lex(text, self._lexer):
                start_pos = pos
                end_pos = pos + len(value)
                tag = self._map_token_to_tag(token)
                if tag:
                    token_positions.append((f"1.0+{start_pos}c", f"1.0+{end_pos}c", tag))
                pos = end_pos
            
            # Apply the tags
            for start, end, tag in token_positions:
                self.tag_add(tag, start, end)
                print(f"Applied tag {tag} from {start} to {end}")  # Debug print
                
            print(f"Applied {len(token_positions)} tag positions")  # Debug print
            
        except Exception as e:
            print(f"Error during highlighting: {e}")  # Debug print