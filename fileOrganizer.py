from pathlib import Path


#Define the file extensions for organization
TARGET_EXTENSIONS = {'.pptx', '.png', '.c', '.uxf', '.flutter', '.exe', '.msi', '.iso', '.zip', '.jpg', '.mp4', '.doc', '.drawio', '.mpp', '.ipynb', '.py', '.cpp'}

MASTER_ARCHIVE = Path.home() / "Documents" / "OrganizedFileTypes"

#Dynamically locates user folders
SAFE_ZONES = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
]

def get_unique_path(target_path):
    """Checks if a file exists and appends an incrementing number if it does."""
    if not target_path.exists():
        return target_path

    counter = 1
    base_name = target_path.stem
    extension = target_path.suffix
    directory = target_path.parent

    while True:
        new_name = f"{base_name}({counter}){extension}"
        new_path = directory / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def organize_safe_zones():

    MASTER_ARCHIVE.mkdir(parents=True, exist_ok=True)
    print(f"Master Archive Location: {MASTER_ARCHIVE}")
    
    for zone in SAFE_ZONES:
        if not zone.exists():
            print(f"Skipping: {zone} (not found)")
            continue

        print(f"Scanning: {zone}...")

        #iterdir() lists only immediate files in the folder, not system folders
        for item in zone.iterdir():

            if not item.is_file() or item == MASTER_ARCHIVE:
                continue
                
            #Only process files with extensions listed in TARGET_EXTENSIONS
            if item.suffix.lower() in TARGET_EXTENSIONS:

                #Creates a destination folder named after the file extension
                dest_dir = MASTER_ARCHIVE / item.suffix[1:].upper()
                
                #Here we make the subdirectories, with a check to make sure if it exists it doesn't
                #crash the program
                dest_dir.mkdir(exist_ok=True)

                #Defines the final target path
                original_target = dest_dir / item.name
                final_path = get_unique_path(original_target)

                #Move files safely using try/except block in case of failures
                try:
                    item.rename(final_path)
                    if final_path.name != item.name:
                        print(f"Renamed and Moved {item.name} -> {final_path.name}")
                    else:
                        print(f"Moved: {item.name} -> {dest_dir.name}/")
                except Exception as e:
                    print(f"Could not move {item.name}: {e}")

if __name__ == "__main__":
    organize_safe_zones()
