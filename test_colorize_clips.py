
import sys
import dvr

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
    # Avoiding adjacent colors on the color wheel
    color_cycle = [
        "Orange",
        "Teal",
        "Purple",
        "Yellow",
        "Blue",
        "Pink",
        "Green",
        "Red", # Sometimes just called Red? In Resolve usually "Orange" is the default first warm color, but let's stick to standard names
        "Tan",
        "Navy"
    ]
    
    # Resolve officially supports these strings (usually case-sensitive in some versions, title case is safest):
    # Orange, Apricot, Yellow, Lime, Olive, Green, Teal, Navy, Blue, Purple, Violet, Pink, Tan, Beige, Brown, Chocolate
    # "Red" is usually mapped to "Orange" or doesn't exist as a dedicated standard clip color label in some versions, 
    # but let's stick to the ones visible in your screenshot.
    
    valid_colors = [
        "Orange", "Teal", "Purple", "Yellow", "Blue", "Pink", "Green", "Navy", "Tan", "Chocolate"
    ]

    print(f"Applying colors to timeline: {timeline.GetName()}")

    
    for track_type in ["video", "audio"]:
        track_count = timeline.GetTrackCount(track_type)
        print(f"Found {track_count} {track_type} tracks.")
        
        for track_index in range(1, track_count + 1):
            print(f"Processing {track_type.capitalize()} Track {track_index}...")
            clips = timeline.GetItemListInTrack(track_type, track_index)
            
            if not clips:
                print(f"  No clips found in {track_type} track {track_index}.")
                continue

            for i, clip in enumerate(clips):
                # Pick color based on index to ensure neighbors are different
                # We use a global counter or local? Local per track is fine for neighbors.
                color_name = valid_colors[i % len(valid_colors)]
                
                # SetClipColor is the standard API method
                success = clip.SetClipColor(color_name)
                
                if success:
                     print(f"  Clip '{clip.GetName()}' -> {color_name}")
                else:
                     print(f"  Failed to set color for '{clip.GetName()}'")

def main():
    resolve = dvr.load_resolve()
    if not resolve:
        print("Could not connect to DaVinci Resolve.")
        sys.exit(1)
        
    colorize_timeline_clips(resolve)

if __name__ == "__main__":
    main()
