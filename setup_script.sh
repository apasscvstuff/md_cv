#!/bin/bash
# CV Markdown System Setup Script
# Run this in your project directory

echo "Setting up CV Markdown System..."

# Create main directory structure
mkdir -p content
mkdir -p assets/icons
mkdir -p styles
mkdir -p scripts
mkdir -p output/{firmware,ai,consulting,executive,general}

# Create content files (YAML)
touch content/arthur-personal.yaml
touch content/arthur-skills.yaml
touch content/arthur-experience.yaml
touch content/arthur-projects.yaml
touch content/arthur-education.yaml

# Create style files
touch styles/cv-base.css
touch styles/cv-print.css
touch styles/cv-versions.css

# Create script files
touch scripts/build-cv.py
touch scripts/test-cv-system.py
chmod +x scripts/build-cv.py
chmod +x scripts/test-cv-system.py

# Create placeholder for assets
touch assets/profile.jpeg.placeholder
touch assets/icons/phone.png.placeholder
touch assets/icons/email.png.placeholder
touch assets/icons/github.png.placeholder
touch assets/icons/linkedin.png.placeholder

echo "✅ Directory structure created successfully!"
echo "📁 Project structure:"
echo "arthur-cv-markdown/"
echo "├── content/"
echo "│   ├── arthur-personal.yaml"
echo "│   ├── arthur-skills.yaml"
echo "│   ├── arthur-experience.yaml"
echo "│   ├── arthur-projects.yaml"
echo "│   └── arthur-education.yaml"
echo "├── assets/"
echo "│   ├── profile.jpeg"
echo "│   └── icons/"
echo "│       ├── phone.png"
echo "│       ├── email.png"
echo "│       ├── github.png"
echo "│       └── linkedin.png"
echo "├── styles/"
echo "│   ├── cv-base.css"
echo "│   ├── cv-print.css"
echo "│   └── cv-versions.css"
echo "├── scripts/"
echo "│   ├── build-cv.py"
echo "│   └── test-cv-system.py"
echo "└── output/"
echo "    ├── firmware/"
echo "    ├── ai/"
echo "    ├── consulting/"
echo "    ├── executive/"
echo "    └── general/"

echo ""
echo "Next steps:"
echo "1. Add your professional photo to assets/profile.jpeg"
echo "2. Download/create contact icons for assets/icons/"
echo "3. Populate YAML files with your existing CV content"
echo "4. Test the system: python scripts/test-cv-system.py"
echo "5. Build all versions: python scripts/build-cv.py all"