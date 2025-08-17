import os
import shutil

def remove_files(FOLDER_PATH):
    if os.path.exists(FOLDER_PATH):
        for filename in os.listdir(FOLDER_PATH):
            file_path = os.path.join(FOLDER_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)  # remove file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # remove folder inside
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print("✅ All files removed successfully!")
    else:
        print(f"Folder '{FOLDER_PATH}' does not exist.")
