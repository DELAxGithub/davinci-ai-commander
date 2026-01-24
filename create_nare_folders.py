
import sys
import dvr

def get_subfolder_by_name(folder, name):
    """
    Finds a subfolder with a specific name inside a given folder.
    Returns the folder object if found, otherwise None.
    """
    sub_folders = folder.GetSubFolderList()
    for sub in sub_folders:
        if sub.GetName() == name:
            return sub
    return None

def main():
    # 1. Connect to DaVinci Resolve
    resolve = dvr.load_resolve()
    if not resolve:
        print("Error: Could not connect to DaVinci Resolve. Please ensure it is running.")
        sys.exit(1)

    # 2. Get Current Project Information
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()

    if not project:
        print("Error: No project is currently open.")
        sys.exit(1)

    print(f"Current Project: {project.GetName()}")

    # 3. Process folders case16 - case30
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    print("Starting folder structure update...")
    
    created_count = 0
    skipped_count = 0

    for i in range(16, 31): # 16 to 30 inclusive
        case_folder_name = f"case{i}"
        target_subfolder_name = "nare1"

        # Find or Create 'caseX' folder
        # The user asked to create 'nare1' INSIDE these folders. 
        # It's safest to ensure the parent exists first.
        case_folder = get_subfolder_by_name(root_folder, case_folder_name)
        
        if not case_folder:
            print(f"  Parent '{case_folder_name}' not found. Creating it...")
            case_folder = media_pool.AddSubFolder(root_folder, case_folder_name)
        
        if case_folder:
            # Check if 'nare1' already exists inside
            nare_folder = get_subfolder_by_name(case_folder, target_subfolder_name)
            
            if nare_folder:
                # print(f"  '{target_subfolder_name}' already exists in '{case_folder_name}'.")
                skipped_count += 1
            else:
                new_folder = media_pool.AddSubFolder(case_folder, target_subfolder_name)
                if new_folder:
                    print(f"  Created '{target_subfolder_name}' in '{case_folder_name}'")
                    created_count += 1
                else:
                    print(f"  Failed to create '{target_subfolder_name}' in '{case_folder_name}'")
        else:
            print(f"  Critical Error: Could not access or create '{case_folder_name}'")

    print("-" * 30)
    print(f"Finished.")
    print(f"Total folders created: {created_count}")
    print(f"Existing folders skipped: {skipped_count}")

if __name__ == "__main__":
    main()
