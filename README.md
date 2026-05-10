# Python File Manager Automation Script

A robust Python script to automate directory management tasks such as organizing files by type, bulk renaming, and cleaning up empty folders.

## Features
- **File Organization**: Automatically sorts files into categorized folders (`Images`, `Documents`, `Code`, etc.) based on their extensions.
- **Bulk Renaming**: Add custom prefixes and suffixes to all files in a directory.
- **Directory Cleanup**: Recursively identifies and removes empty subdirectories.
- **Detailed Logging**: Every operation is logged with timestamps and status (INFO/ERROR) to both the console and a `.log` file.
- **Robust Error Handling**: Uses try-except blocks to handle permission issues, missing paths, and unexpected IO errors.

## Requirements
- Python 3.x
- No external dependencies required (uses `os`, `shutil`, `logging`, and `argparse`).

## Usage

### Organize Files
Sorts files in the target directory into type-based folders.
```bash
python file_manager.py ./target_folder --organize
```

### Bulk Rename
Adds a prefix and/or suffix to all files in the directory.
```bash
python file_manager.py ./target_folder --rename "project_A_" --suffix "_v1"
```

### Cleanup Empty Directories
Removes all empty folders and subfolders.
```bash
python file_manager.py ./target_folder --cleanup
```

### Combine Operations
You can run multiple operations at once:
```bash
python file_manager.py ./target_folder -o -c
```

## Sample Input/Output

### Before Organization:
```text
test_folder/
├── photo1.jpg
├── photo2.png
├── doc1.pdf
├── script.py
├── empty_dir/
└── nested_empty/
    └── deep_empty/
```

### After Running `python file_manager.py ./test_folder -o -c`:
```text
test_folder/
├── Images/
│   ├── photo1.jpg
│   └── photo2.png
├── Documents/
│   └── doc1.pdf
├── Code/
│   └── script.py
└── Others/
    └── unknown.xyz
```

### Sample Log Output:
```text
2026-05-10 15:49:57,260 - INFO - Organizing files in: D:\Python automation script\test_folder
2026-05-10 15:49:57,261 - INFO - Created folder: Documents
2026-05-10 15:49:57,261 - INFO - Moved: data.csv -> Documents/
2026-05-10 15:49:57,264 - INFO - Removed empty directory: D:\test_folder\nested_empty\deep_empty
```
