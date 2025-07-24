CLAUDE ARTIFACT: CORRECTED Chrome PDF Method - Drop-in Replacement
============================================================
From Conversation: AI Skills Architecture Design
Found at path: root.chat_messages[7].content[24]
Artifact ID: corrected_chrome_method
Type: application/vnd.ant.code
Language: python
Created: 2025-07-23T13:39:03.099710Z
Updated: 2025-07-23T13:39:24.629360Z
============================================================

ARTIFACT CONTENT:
----------------------------------------
# CORRECTED Chrome PDF Method - Replace in build_system.py
# This method maintains compatibility with your existing system while enhancing PDF quality

def _try_chrome_headless_pdf(
    self, html_path: Path, pdf_path: Path, target_version: str
) -> bool:
    """Enhanced Chrome headless PDF generation with optimized settings for professional quality"""
    
    chrome_commands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome",
        "chromium",
        "google-chrome-stable",
        "/opt/homebrew/bin/chromium",
        "/usr/local/bin/google-chrome",
    ]

    for chrome_cmd in chrome_commands:
        try:
            # Check if the command exists
            if chrome_cmd.startswith("/"):
                if not Path(chrome_cmd).exists():
                    continue

            # Enhanced Chrome settings for professional PDF quality
            cmd = [
                chrome_cmd,
                "--headless=new",                    # Latest headless mode
                "--disable-gpu",                     # Prevent GPU conflicts
                "--disable-dev-shm-usage",          # Memory optimization
                "--no-sandbox",                      # Bypass security for headless
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                
                # PDF generation settings - optimized for professional output
                f"--print-to-pdf={pdf_path}",
                "--print-to-pdf-no-header",          # Clean output
                "--no-pdf-header-footer",            # No browser artifacts
                "--no-margins",                      # Use CSS margins instead
                
                # Rendering quality - high-fidelity output
                "--force-color-profile=srgb",        # Consistent color reproduction
                "--disable-background-media-suspend", # Ensure media processing
                "--disable-features=TranslateUI,VizDisplayCompositor", # Remove UI elements
                "--disable-ipc-flooding-protection",  # Better resource handling
                
                # Print-specific optimizations
                "--disable-extensions",              # Clean rendering environment
                "--disable-plugins",                 # Prevent plugin interference
                "--virtual-time-budget=10000",      # Extended load time for fonts
                "--run-all-compositor-stages-before-draw", # Complete rendering
                
                # Layout & sizing - professional formatting
                "--window-size=1280,1696",          # A4 proportion (1:1.41)
                "--hide-scrollbars",                # Clean visual output
                "--disable-background-networking",   # Faster rendering
                
                # Font & asset handling - critical for professional appearance
                "--font-render-hinting=none",       # Crisp font rendering
                "--enable-font-antialiasing",       # Smooth text
                "--disable-remote-fonts",           # Use local fonts only
                "--allow-file-access-from-files",   # Local asset access
                "--disable-web-security",           # Allow local font loading
                
                # Performance optimizations
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-features=Translate",
                
                f"file://{html_path.absolute()}",
            ]

            # Execute with extended timeout for font loading
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=45,  # Extended timeout for complex CVs
                cwd=html_path.parent  # Ensure proper working directory
            )
            
            if result.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 5000:
                print(f"✅ Enhanced PDF generated with Chrome: {pdf_path}")
                print(f"📊 File size: {pdf_path.stat().st_size // 1024}KB")
                return True
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                print(f"❌ Chrome failed with {chrome_cmd}: {error_msg}")

        except subprocess.TimeoutExpired:
            print(f"⏰ Chrome timeout with {chrome_cmd} - extending processing time")
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"💥 Chrome error with {chrome_cmd}: {e}")
            continue

    print("❌ Chrome headless not available or failed")
    return False