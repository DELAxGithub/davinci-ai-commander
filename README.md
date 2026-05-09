# DaVinci AI Commander

**Control DaVinci Resolve with natural language. Type what you want, and AI writes the code.**

<img src="https://img.shields.io/badge/DaVinci_Resolve-19+-blue.svg" alt="DaVinci Resolve 19+"> <img src="https://img.shields.io/badge/Platform-macOS_11+-lightgrey.svg" alt="macOS 11+"> <img src="https://img.shields.io/badge/AI-Gemini_2.5_Flash-orange.svg" alt="Gemini 2.5 Flash">

DaVinci AI Commander automates the tedious parts of post-production — bin organization, batch rendering, marker management, metadata editing — through plain English (or Japanese) commands.

> "Create bins case01 to case30" → Done in 2 seconds.  
> "Set all clip colors to blue in the timeline" → Done.  
> "Render all timelines with the YouTube preset" → Queued.

## Features

- **Natural Language Control** — Powered by Google Gemini 2.5 Flash. Translates your intent into DaVinci Resolve Scripting API calls.
- **Safe by Design** — Only touches structural operations (bins, timelines, markers, metadata). Cannot modify video content, apply effects, or color grade.
- **Code Validation** — AI-generated code is checked for dangerous patterns before execution.
- **Secure API Key Storage** — Your Gemini API key is stored in macOS Keychain, not in plain text.
- **Command History** — Navigate past commands with ↑↓ arrow keys.
- **Standalone .app** — No Python setup required for end users. Just download, launch, and connect.

## Requirements

- macOS 11 (Big Sur) or later
- DaVinci Resolve 19+ (Free or Studio)
- Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

## Getting Started

1. **Open DaVinci Resolve** with a project loaded.
2. **Enable scripting**: Resolve → Preferences → System → General → "External scripting using" → **Local**.
3. **Launch DaVinci AI Commander**.
4. **Set your API key** (first launch only — click "Set API Key" button).
5. **Type a command** and press Enter.

## What It Can Do

| Category | Examples |
|----------|---------|
| **Bin Management** | Create, delete, rename bins in bulk |
| **Timeline** | Create timelines, append clips, read timeline info |
| **Markers** | Add, list, remove markers with notes |
| **Metadata** | Read/write clip metadata, project settings |
| **Rendering** | Queue renders, apply presets, batch export |
| **Clip Properties** | Change clip colors, flags |

## What It Cannot Do

- Edit video content (cut, trim, split)
- Apply effects or color grading
- Analyze video/audio content
- Interact with the Resolve UI directly

See [use_cases.md](use_cases.md) for the full list, and [pro_reference.md](pro_reference.md) for professional automation workflows.

## Development

### Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./launch_app.sh
```

### Build

```bash
./build_app.sh
```

For signed distribution:

```bash
CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)" ./build_app.sh
```

For signed + notarized:

```bash
CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)" \
APPLE_ID="your@email.com" \
APPLE_TEAM_ID="YOURTEAMID" \
APP_PASSWORD="xxxx-xxxx-xxxx-xxxx" \
./build_app.sh
```

## License

[MIT License](LICENSE) — © 2026 DELAX Studio

---

*DaVinci AI Commander is not affiliated with or endorsed by Blackmagic Design.*
