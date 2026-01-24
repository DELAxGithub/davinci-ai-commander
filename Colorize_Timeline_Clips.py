#!/usr/bin/env python3
import sys
import os

def load_resolve():
    """
    Attempts to load the DaVinciResolveScript module.
    """
    # Try importing directly (if running from inside Resolve Console)
    try:
        import DaVinciResolveScript as dvr_script
        resolve = dvr_script.scriptapp("Resolve")
        if resolve:
            return resolve
    except ImportError:
        pass

    # Fallback: Check standard macOS paths for external execution
    import platform
    if platform.system() == "Darwin":
        expected_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        if os.path.exists(expected_path):
            if expected_path not in sys.path:
                sys.path.append(expected_path)
            
            # Also set the LIB path env var which is often needed by the module internally
            lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
            if "RESOLVE_SCRIPT_LIB" not in os.environ and os.path.exists(lib_path):
                os.environ["RESOLVE_SCRIPT_LIB"] = lib_path
                
            try:
                import DaVinciResolveScript as dvr_script
                resolve = dvr_script.scriptapp("Resolve")
                if resolve:
                    return resolve
            except ImportError:
                pass

    return None

def colorize_timeline_clips(resolve):
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    
    if not project:
        print("Error: No project is currently open.")
        return

    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("Error: No timeline is currently open.")
        return

    # High contrast color cycle
    valid_colors = [
        "Orange", "Teal", "Purple", "Yellow", "Blue", "Pink", "Green", "Navy", "Tan", "Chocolate"
    ]

    print(f"Applying colors to timeline: {timeline.GetName()}")

    for track_type in ["video", "audio"]:
        track_count = timeline.GetTrackCount(track_type)
        print(f"Checking {track_count} {track_type} tracks...")
        
        for track_index in range(1, track_count + 1):
            clips = timeline.GetItemListInTrack(track_type, track_index)
            
            if not clips:
                continue

            for i, clip in enumerate(clips):
                color_name = valid_colors[i % len(valid_colors)]
                clip.SetClipColor(color_name)
    
    print("Derived from DaVinci AI Commander.")

def main():
    resolve = load_resolve()
    if not resolve:
        print("Could not connect to DaVinci Resolve.")
        return
        
    colorize_timeline_clips(resolve)

if __name__ == "__main__":
    main()
