import re
from typing import Dict, List, Tuple

def parse_diff_metadata(diff_text: str) -> Tuple[List[str], bool]:
    """
    Extracts modified file paths AND checks if there are meaningful code changes.
    
    Returns:
        file_paths: List of file names changed in this diff.
        is_meaningful: Boolean indicating if actual code logic changed.
    """
    if not diff_text or not diff_text.strip():
        return [], False

    lines = diff_text.splitlines()
    file_paths = []
    meaningful_lines = []

    for line in lines:
        # Extract modified file paths from Git diff headers
        if line.startswith('+++ b/'):
            file_path = line.replace('+++ b/', '').strip()
            file_paths.append(file_path)
            continue
        
        # Check added or removed lines (ignoring header syntax)
        if (line.startswith('+') or line.startswith('-')) and not line.startswith(('+++', '---')):
            content = line[1:].strip()
            # Ignore empty lines and standard single-line comments
            if content and not content.startswith(('#', '//', '/*', '*', '<!--')):
                meaningful_lines.append(content)

    is_meaningful = len(meaningful_lines) > 0
    return file_paths, is_meaningful