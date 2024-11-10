import re
from pathlib import Path # used to delete old files in folder

# Take out any invalid characters for a filename
def sanitize_filename(filename: str) -> str:
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[\/:*?"<>|]', '_', filename)
    # Optionally strip leading/trailing spaces and dots
    sanitized = sanitized.strip().strip('.')
    return sanitized


# --- Function to delete files inside directory (without deleting directory itself) ---
def emptyFolder(directoryPath):
    [f.unlink() for f in Path(directoryPath).glob("*") if f.is_file()] 