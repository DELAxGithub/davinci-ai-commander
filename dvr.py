#!/usr/bin/env python3
import sys
import os
import argparse

def load_resolve():
    """
    Attempts to load the DaVinciResolveScript module.
    It checks if it's already available (e.g. running from console),
    or tries to import it if the environment is set up.
    """
    # Try importing directly
    try:
        import DaVinciResolveScript as dvr_script
        resolve = dvr_script.scriptapp("Resolve")
        if resolve:
            return resolve
    except ImportError:
        pass

    # Fallback: Check standard macOS paths
    # This allow the app to run without a wrapper script
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
                print("Found module path but failed to import DaVinciResolveScript.")

    print("Could not load 'DaVinciResolveScript' module.")
    print("Please ensure DaVinci Resolve is installed and running.")
    return None

def create_bins(prefix, start, end, resolve=None):
    if not resolve:
        resolve = load_resolve()
        if not resolve:
            return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    
    if not project:
        print("Error: No project is currently open.")
        return

    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    if start > end:
        print(f"Error: Start ({start}) is greater than End ({end}).")
        return

    print(f"Creating bins '{prefix}{start}' to '{prefix}{end}'...")
    
    created_count = 0
    for i in range(start, end + 1):
        bin_name = f"{prefix}{i}"
        try:
            # CreateFolder directly under root
            new_folder = media_pool.AddSubFolder(root_folder, bin_name)
            if new_folder:
                print(f"Created: {bin_name}")
                created_count += 1
            else:
                print(f"Failed to create (or maybe exists): {bin_name}")
        except Exception as e:
            print(f"Error creating {bin_name}: {e}")

    print(f"Done. Created {created_count} bins.")

def main():
    parser = argparse.ArgumentParser(description="DaVinci Resolve Utility CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: create-bins
    parser_create = subparsers.add_parser("create-bins", help="Bulk create bins in the Master folder")
    parser_create.add_argument("--prefix", type=str, required=True, help="Prefix for the bin name (e.g. 'case')")
    parser_create.add_argument("--start", type=int, required=True, help="Start number")
    parser_create.add_argument("--end", type=int, required=True, help="End number")

    args = parser.parse_args()

    resolve = load_resolve()
    if not resolve:
        sys.exit(1)

    if args.command == "create-bins":
        create_bins(args.prefix, args.start, args.end, resolve)

if __name__ == "__main__":
    main()
