#!/usr/bin/env python3
import sys
import os
import time

def load_resolve():
    try:
        import DaVinciResolveScript as dvr_script
        resolve = dvr_script.scriptapp("Resolve")
        if resolve:
            return resolve
    except ImportError:
        pass

    import platform
    if platform.system() == "Darwin":
        expected_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        if os.path.exists(expected_path):
            if expected_path not in sys.path:
                sys.path.append(expected_path)
            
            lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
            if "RESOLVE_SCRIPT_LIB" not in os.environ and os.path.exists(lib_path):
                os.environ["RESOLVE_SCRIPT_LIB"] = lib_path
                
            try:
                import DaVinciResolveScript as dvr_script
                resolve = dvr_script.scriptapp("Resolve")
                if resolve:
                    return resolve
            except ImportError:
                print("Found module path but failed to import DaVinciResolveScript.")

    return None

def color_code_timeline(target_timeline_name=None):
    resolve = load_resolve()
    if not resolve:
        print("Could not connect to DaVinci Resolve.")
        return

    # Ensure we are in Edit page context
    resolve.OpenPage("edit")
    time.sleep(1.0)

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    
    if not project:
        print("No project is currently open.")
        return

    # 1. Prioritize Current Timeline (Default behavior)
    current_timeline = project.GetCurrentTimeline()
    target_timeline = None

    if target_timeline_name is None:
        if current_timeline:
            target_timeline = current_timeline
            print(f"Targeting active timeline: {target_timeline.GetName()}")
        else:
            print("No active timeline found.")
            return
    elif current_timeline and current_timeline.GetName() == target_timeline_name:
        print(f"Using active timeline: {target_timeline_name}")
        target_timeline = current_timeline
    else:
        # 2. Search by name
        timeline_count = project.GetTimelineCount()
        for i in range(1, timeline_count + 1):
            timeline = project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() == target_timeline_name:
                target_timeline = timeline
                print(f"Found timeline by index: {i}")
                break
    
    if not target_timeline:
        print(f"Timeline '{target_timeline_name}' not found.")
        if current_timeline:
            print(f"(Current active timeline is: '{current_timeline.GetName()}')")
        return

    # Detect items
    track_type = "audio"
    track_count = target_timeline.GetTrackCount(track_type)
    
    print(f"Scanning {track_count} audio tracks...")

    # Sort items by Start Frame first
    all_items = []
    # Search all audio tracks for content
    for t_idx in range(1, track_count + 1):
        try:
            track_items = target_timeline.GetItemListInTrack(track_type, t_idx)
            if track_items:
                print(f"Found {len(track_items)} clips in Audio Track {t_idx}.")
                all_items.extend(track_items)
        except Exception as e:
            print(f"Error reading track {t_idx}: {e}")

    if not all_items:
        print("No audio clips found in any track.")
        return

    # Sort all items by start time
    all_items.sort(key=lambda x: x.GetStart())

    

    # Group with tolerance (e.g., 20 frames to catch 13-frame offsets)
    TOLERANCE_FRAMES = 20
    chunks = [] # List of lists: [[item1, item2], [item3, item4]]
    
    current_chunk = []
    chunk_start_time = -1

    for item in all_items:
        start = item.GetStart()
        
        if not current_chunk:
            current_chunk.append(item)
            chunk_start_time = start
        else:
            # If within tolerance of the current chunk's start
            if abs(start - chunk_start_time) <= TOLERANCE_FRAMES:
                current_chunk.append(item)
            else:
                chunks.append(current_chunk)
                current_chunk = [item]
                chunk_start_time = start
    
    if current_chunk:
        chunks.append(current_chunk)

    print(f"Grouped {len(all_items)} clips into {len(chunks)} vertical chunks (Tolerance: {TOLERANCE_FRAMES} frames).")

    # Valid DaVinci Resolve Colors (Safe List)
    colors = [
        "Orange", "Teal", "Yellow", "Purple", 
        "Pink", "Green", "Blue", "Tan", "Chocolate", "Olive"
    ]
    
    count = 0
    for i, chunk_items in enumerate(chunks):
        color = colors[i % len(colors)]
        
        for item in chunk_items:
            # Retry logic for robustness
            success = False
            for attempt in range(3):
                if item.SetClipColor(color):
                    success = True
                    count += 1
                    break
                time.sleep(0.1) # Brief pause before retry
            
            if not success:
                 print(f"Failed to color item {item.GetName()} (Color: {color}) after 3 attempts.")

    print(f"Done! Painted {count} clips across {len(chunks)} vertical chunks.")

if __name__ == "__main__":
    color_code_timeline()
