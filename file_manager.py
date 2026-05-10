import os
import shutil
import logging
import argparse
from datetime import datetime

def setup_logging():
    """Configures the logging system to output to both console and a file."""
    log_filename = f"file_ops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return log_filename


EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv', '.md'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'Video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.h', '.java', '.json', '.yaml'],
}

def organize_files(directory):
    """
    Sorts files into subfolders based on their extensions.
    Categorizes unknown extensions into an 'Others' folder.
    """
    if not os.path.isdir(directory):
        logging.error(f"Directory not found: {directory}")
        return

    logging.info(f"Organizing files in: {directory}")
    
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        for filename in files:
            filepath = os.path.join(directory, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            target_folder = "Others"
            for folder, extensions in EXTENSION_MAP.items():
                if file_ext in extensions:
                    target_folder = folder
                    break
            
            dest_dir = os.path.join(directory, target_folder)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                logging.info(f"Created folder: {target_folder}")
            
            shutil.move(filepath, os.path.join(dest_dir, filename))
            logging.info(f"Moved: {filename} -> {target_folder}/")
            
    except Exception as e:
        logging.error(f"Error during organization: {e}")

def bulk_rename(directory, prefix="", suffix=""):
    """
    Renames all files in the specified directory by adding a prefix and/or suffix.
    """
    if not os.path.isdir(directory):
        logging.error(f"Directory not found: {directory}")
        return

    logging.info(f"Bulk renaming files in: {directory}")
    
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                name, ext = os.path.splitext(filename)
                new_name = f"{prefix}{name}{suffix}{ext}"
                new_path = os.path.join(directory, new_name)
                
                os.rename(filepath, new_path)
                logging.info(f"Renamed: {filename} -> {new_name}")
    except Exception as e:
        logging.error(f"Error during bulk rename: {e}")

def cleanup_empty_dirs(directory):
    """
    Recursively removes empty directories within the target path.
    """
    if not os.path.isdir(directory):
        logging.error(f"Directory not found: {directory}")
        return

    logging.info(f"Cleaning up empty directories in: {directory}")
    
    try:
        # Walk bottom-up to ensure empty parent directories are also caught
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in dirs:
                dir_path = os.path.join(root, name)
                if not os.listdir(dir_path):  # Directory is empty
                    os.rmdir(dir_path)
                    logging.info(f"Removed empty directory: {dir_path}")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="File Manager Automation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python file_manager.py ./my_folder --organize
  python file_manager.py ./my_folder --rename "v1_" --suffix "_draft"
  python file_manager.py ./my_folder --cleanup
        """
    )
    parser.add_argument("path", help="Target directory path")
    parser.add_argument("-o", "--organize", action="store_true", help="Organize files into folders by type")
    parser.add_argument("-r", "--rename", help="Add prefix for bulk renaming", default=None)
    parser.add_argument("-s", "--suffix", help="Add suffix for bulk renaming", default="")
    parser.add_argument("-c", "--cleanup", action="store_true", help="Remove empty subdirectories")

    args = parser.parse_args()
    
    log_file = setup_logging()
    logging.info("Starting file automation tasks...")

    target_path = os.path.abspath(args.path)

    if not os.path.exists(target_path):
        logging.error(f"Path does not exist: {target_path}")
        return

    try:
        if args.organize:
            organize_files(target_path)
        
        if args.rename is not None:
            bulk_rename(target_path, prefix=args.rename, suffix=args.suffix)
            
        if args.cleanup:
            cleanup_empty_dirs(target_path)
            
        if not (args.organize or args.rename is not None or args.cleanup):
            logging.warning("No action specified. Use --help to see available options.")
            
    except Exception as e:
        logging.critical(f"Critical script failure: {e}", exc_info=True)
    
    logging.info(f"Tasks completed. Check {log_file} for full details.")

if __name__ == "__main__":
    main()
