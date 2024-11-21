import os

def consolidate_project(source_dir, output_file, ignore_list=None):
    """
    Consolidate text content of files within a folder into a single Markdown file,
    showing the folder structure at the beginning.
    
    :param source_dir: Path to the project directory
    :param output_file: Path to the output Markdown file
    :param ignore_list: List of file/folder names to ignore (optional)
    """
    if ignore_list is None:
        ignore_list = []
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Write project structure
        out_file.write("# Project Structure\n\n")
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in ignore_list]
            level = root.replace(source_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            out_file.write(f"{indent}- {os.path.basename(root)}/\n")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                if file not in ignore_list:
                    out_file.write(f"{sub_indent}- {file}\n")
        
        out_file.write("\n---\n\n")
        
        # Write file contents
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in ignore_list]
            for file in files:
                if file not in ignore_list:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, source_dir)
                    out_file.write(f"# {rel_path}\n\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_file:
                            content = in_file.read()
                            out_file.write(f"```\n{content}\n```\n\n")
                    except UnicodeDecodeError:
                        out_file.write("*[Binary file not shown]*\n\n")
                    except Exception as e:
                        out_file.write(f"*[Error reading file: {str(e)}]*\n\n")

# Example usage
if __name__ == "__main__":
    project_dir = "./"
    output_md = "aider_extension_consolidated.md"
    files_to_ignore = ["project-consolidator.py", ".git", ".gitignore", "venv", ".env", "__pycache__","aider_extension_consolidated.md"]
    
    consolidate_project(project_dir, output_md, files_to_ignore)
    print(f"Project consolidated to {output_md}")
