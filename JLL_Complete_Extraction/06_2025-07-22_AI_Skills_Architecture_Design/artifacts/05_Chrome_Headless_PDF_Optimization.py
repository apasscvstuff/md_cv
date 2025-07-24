CLAUDE ARTIFACT: Chrome Headless PDF Optimization
============================================================
From Conversation: AI Skills Architecture Design
Found at path: root.chat_messages[1].content[23]
Artifact ID: chrome_pdf_optimization
Type: application/vnd.ant.code
Language: python
Created: 2025-07-23T13:04:56.525290Z
Updated: 2025-07-23T13:05:31.256630Z
============================================================

ARTIFACT CONTENT:
----------------------------------------
def _try_chrome_headless_pdf_enhanced(
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
            if chrome_cmd.startswith("/") and not Path(chrome_cmd).exists():
                continue

            # 🎯 ENHANCED CHROME SETTINGS - Professional PDF quality
            cmd = [
                chrome_cmd,
                "--headless=new",                    # Latest headless mode
                "--disable-gpu",                     # Prevent GPU conflicts
                "--disable-dev-shm-usage",          # Memory optimization
                "--no-sandbox",                      # Bypass security for headless
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                
                # 📄 PDF GENERATION SETTINGS - Optimized for professional output
                f"--print-to-pdf={pdf_path}",
                "--print-to-pdf-no-header",          # Clean output
                "--no-pdf-header-footer",            # No browser artifacts
                "--no-margins",                      # Use CSS margins instead
                
                # 🎨 RENDERING QUALITY - High-fidelity output
                "--force-color-profile=srgb",        # Consistent color reproduction
                "--disable-background-media-suspend", # Ensure media processing
                "--disable-features=TranslateUI",     # Remove translation bars
                "--disable-ipc-flooding-protection",  # Better resource handling
                
                # 🖨️ PRINT-SPECIFIC OPTIMIZATIONS
                "--disable-extensions",              # Clean rendering environment
                "--disable-plugins",                 # Prevent plugin interference
                "--disable-images",                  # Handle images via CSS
                "--virtual-time-budget=10000",      # Extended load time for fonts
                "--run-all-compositor-stages-before-draw", # Complete rendering
                
                # 📐 LAYOUT & SIZING - Professional formatting
                "--window-size=1280,1696",          # A4 proportion (1:1.41)
                "--hide-scrollbars",                # Clean visual output
                "--disable-background-networking",   # Faster rendering
                
                # 🔧 FONT & ASSET HANDLING - Critical for professional appearance
                "--font-render-hinting=none",       # Crisp font rendering
                "--enable-font-antialiasing",       # Smooth text
                "--disable-remote-fonts",           # Use local fonts only
                "--allow-file-access-from-files",   # Local asset access
                
                f"file://{html_path.absolute()}",
            ]

            # 🎯 EXECUTION WITH TIMEOUT - Professional reliability
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,  # Increased timeout for font loading
                cwd=html_path.parent  # Ensure proper working directory
            )
            
            if result.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 10000:
                print(f"✅ Enhanced PDF generated: {pdf_path}")
                print(f"📊 File size: {pdf_path.stat().st_size // 1024}KB")
                return True
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                print(f"❌ Chrome failed with {chrome_cmd}: {error_msg}")

        except subprocess.TimeoutExpired:
            print(f"⏰ Chrome timeout with {chrome_cmd} - PDF generation took too long")
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"💥 Chrome error with {chrome_cmd}: {e}")
            continue

    print("❌ Chrome headless not available or failed")
    return False


def _create_print_optimized_html(self, html_path: Path, target_version: str) -> Path:
    """Create PDF-optimized HTML with enhanced print styles"""
    
    # Read existing HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 🎯 PDF-SPECIFIC ENHANCEMENTS
    pdf_enhancements = """
    <style>
    /* 🖨️ PDF-SPECIFIC OPTIMIZATIONS */
    @media print {
        body {
            /* Enhanced font rendering for PDF */
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
            
            /* Ensure colors print correctly */
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            color-adjust: exact;
        }
        
        /* Force high-quality image rendering */
        img {
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
        }
        
        /* Ensure consistent spacing */
        * {
            box-sizing: border-box;
        }
        
        /* Enhanced page setup */
        @page {
            size: A4 portrait;
            margin: 15mm;
            
            /* Professional page counter */
            @bottom-right {
                content: counter(page) " / " counter(pages);
                font-family: 'Roboto', sans-serif;
                font-size: 8pt;
                color: #666;
            }
        }
        
        /* Prevent awkward breaks */
        .cv-experience-item,
        .cv-project-item,
        .cv-education-item {
            page-break-inside: avoid;
            break-inside: avoid;
        }
        
        h1, h2, h3 {
            page-break-after: avoid;
            break-after: avoid;
        }
    }
    </style>
    """
    
    # Insert PDF enhancements before closing </head>
    enhanced_html = html_content.replace('</head>', f'{pdf_enhancements}</head>')
    
    # Create PDF-optimized version
    pdf_html_path = html_path.parent / f"arthur-{target_version}-pdf.html"
    with open(pdf_html_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    return pdf_html_path


# 🎯 INTEGRATION HELPER - Add this to your CVBuilder class
def build_pdf_enhanced(self, target_version: str, template: str = "professional") -> None:
    """Enhanced PDF generation with optimized Chrome settings"""
    print(f"🎯 Building enhanced PDF for {target_version} version...")

    # Ensure HTML exists
    html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
    if not html_path.exists():
        self.build_html(target_version, template)

    # Create PDF-optimized HTML
    pdf_html_path = self._create_print_optimized_html(html_path, target_version)
    pdf_path = self.output_dir / target_version / f"arthur-{target_version}.pdf"

    # Try enhanced Chrome generation first
    if self._try_chrome_headless_pdf_enhanced(pdf_html_path, pdf_path, target_version):
        # Cleanup temporary PDF-optimized HTML
        pdf_html_path.unlink(missing_ok=True)
        print(f"✅ Enhanced PDF generation complete: {pdf_path}")
        return True
    
    # Fallback to existing methods
    return self._try_weasyprint_pdf(html_path, pdf_path, target_version)