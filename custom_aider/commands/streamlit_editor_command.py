from ..commands_registry import CommandsRegistry
import streamlit
import subprocess
import sys
import os
import tempfile
import threading
import time
import signal
from pathlib import Path

STREAMLIT_EDITOR_CODE = '''
import streamlit as st
import os
import json

st.set_page_config(
    page_title="Aider Streamlit Editor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load initial content if provided
content_file = os.environ.get('AIDER_EDITOR_CONTENT')
initial_content = ""
if content_file and os.path.exists(content_file):
    with open(content_file, 'r') as f:
        initial_content = f.read()

# Set up the title
st.title("Aider Streamlit Editor")

# Add editor instructions
st.markdown("""
### Instructions:
1. Edit the text in the area below
2. Use the 'Save Changes' button to save and close
3. Or use 'Cancel' to discard changes
""")

# Create text editor with initial content
text_content = st.text_area("Edit your content:", 
                           value=initial_content,
                           height=400)

# Create columns for buttons
col1, col2 = st.columns([1,6])

# Add save button that writes to file and exits
if col1.button("Save Changes"):
    output_file = os.environ.get('AIDER_EDITOR_OUTPUT')
    if output_file:
        with open(output_file, 'w') as f:
            f.write(text_content)
    st.success("Changes saved!")
    # Write success flag
    with open(output_file + '.success', 'w') as f:
        f.write('1')
    # Exit after brief delay
    time.sleep(0.5)
    os._exit(0)

# Add cancel button
if col2.button("Cancel"):
    st.error("Cancelled!")
    time.sleep(0.5)
    os._exit(1)
'''

def create_temp_streamlit_app():
    """Create temporary Streamlit app file"""
    fd, path = tempfile.mkstemp(suffix='.py')
    with os.fdopen(fd, 'w') as f:
        f.write(STREAMLIT_EDITOR_CODE)
    return path

def cmd_streamlit_editor(self, initial_content=""):
    """Launch Streamlit editor and return edited content.
    Usage: Run the command or pipe to it to edit content.
    
    Launches a Streamlit-based rich text editor in the browser.
    Waits for you to save or cancel, then returns the edited text.
    """
    # Create temp files
    app_path = create_temp_streamlit_app()
    content_file = tempfile.mktemp()
    output_file = tempfile.mktemp()
    
    try:
        # Write initial content
        with open(content_file, 'w') as f:
            f.write(initial_content)
            
        # Set up environment
        env = os.environ.copy()
        env['AIDER_EDITOR_CONTENT'] = content_file
        env['AIDER_EDITOR_OUTPUT'] = output_file
        
        # Build Streamlit command
        cmd = [
            sys.executable,
            "-m", "streamlit",
            "run",
            app_path,
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--theme.base=light",
            "--"  # Stop streamlit arg parsing
        ]

        # Start Streamlit
        self.io.tool_output("Launching Streamlit editor...")
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid if os.name != 'nt' else None
        )

        # Monitor for output file
        success_file = output_file + '.success'
        start_time = time.time()
        timeout = 300  # 5 minutes
        
        while time.time() - start_time < timeout:
            # Check if process has ended
            if process.poll() is not None:
                if process.returncode != 0:
                    self.io.tool_error("Editor process ended unexpectedly")
                    return None
                break
                
            # Check for success file
            if os.path.exists(success_file):
                break
                
            time.sleep(0.5)
            
        # Cleanup Streamlit process
        try:
            if os.name != 'nt':
                os.killpg(process.pid, signal.SIGTERM)
            else:
                process.terminate()
        except:
            pass
            
        # Check for output
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                return f.read()
                
        return None
        
    finally:
        # Cleanup temp files
        for f in [app_path, content_file, output_file, success_file]:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                pass

# Register the command
CommandsRegistry.register("streamlit_editor", cmd_streamlit_editor)
