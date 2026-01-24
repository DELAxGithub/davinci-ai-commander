
import sys
import dvr

def get_subfolder_by_name(folder, name):
    sub_folders = folder.GetSubFolderList()
    for sub in sub_folders:
        if sub.GetName() == name:
            return sub
    return None

def main():
    resolve = dvr.load_resolve()
    if not resolve:
        print("Error: Could not connect to DaVinci Resolve.")
        sys.exit(1)

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    
    if not project:
        print("Error: No project open.")
        sys.exit(1)
        
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    print(f"Project: {project.GetName()}")
    print("Moving .mp3 files to 'nare1' folders...")

    total_moved = 0

    for i in range(16, 31):
        case_name = f"case{i}"
        
        # 1. Get the parent 'caseX' folder
        case_folder = get_subfolder_by_name(root_folder, case_name)
        if not case_folder:
            print(f"Skipping {case_name} (Folder not found)")
            continue
            
        # 2. Get the target 'nare1' folder inside it
        nare_folder = get_subfolder_by_name(case_folder, "nare1")
        if not nare_folder:
            print(f"Skipping {case_name} (nare1 folder not found)")
            continue

        # 3. Find mp3 clips in the 'caseX' folder
        clips = case_folder.GetClipList()
        mp3_clips_to_move = []
        
        for clip in clips:
            # GetClipProperty usually returns properties like "File Name", "File Path", etc.
            # Depending on version "File Name" is reliable.
            file_name = clip.GetClipProperty("File Name")
            
            # Check for mp3 extension (case insensitive)
            if file_name and file_name.lower().endswith(".mp3"):
                mp3_clips_to_move.append(clip)
        
        # 4. Move valid clips
        if mp3_clips_to_move:
            if media_pool.MoveClips(mp3_clips_to_move, nare_folder):
                count = len(mp3_clips_to_move)
                print(f"  {case_name}: Moved {count} mp3(s) -> nare1")
                total_moved += count
            else:
                print(f"  {case_name}: Failed to move {len(mp3_clips_to_move)} clips.")
        else:
            # Optional: print if empty to confirm check happened
            # print(f"  {case_name}: No mp3 files found.")
            pass

    print("-" * 30)
    print(f"Total MP3 clips moved: {total_moved}")

if __name__ == "__main__":
    main()
