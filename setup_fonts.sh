#!/bin/bash
# setup_fonts.sh
# Install Devanagari fonts for subtitle rendering

echo "Setting up Devanagari fonts..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "Installing Noto Sans Devanagari font..."
        sudo apt-get update
        sudo apt-get install -y fonts-noto fonts-noto-core fonts-noto-cjk fonts-noto-ui-core
        sudo apt-get install -y fonts-dejavu fonts-dejavu-core
        echo "✅ Fonts installed successfully"
    
    # Fedora/RHEL
    elif command -v dnf &> /dev/null; then
        echo "Installing Noto Sans Devanagari font..."
        sudo dnf install -y google-noto-sans-devanagari-fonts dejavu-sans-fonts
        echo "✅ Fonts installed successfully"
    
    # Arch Linux
    elif command -v pacman &> /dev/null; then
        echo "Installing Noto Sans Devanagari font..."
        sudo pacman -S --noconfirm noto-fonts ttf-dejavu
        echo "✅ Fonts installed successfully"
    else
        echo "⚠️ Unknown package manager. Please install fonts manually:"
        echo "   - Noto Sans Devanagari"
        echo "   - DejaVu Sans"
    fi
    
    # Update font cache
    fc-cache -fv

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    
    if command -v brew &> /dev/null; then
        echo "Installing Noto Sans Devanagari font via Homebrew..."
        brew tap homebrew/cask-fonts
        brew install --cask font-noto-sans-devanagari
        echo "✅ Font installed successfully"
    else
        echo "⚠️ Homebrew not found. Please install manually:"
        echo "   1. Download Noto Sans Devanagari from Google Fonts"
        echo "   2. Install by double-clicking the .ttf files"
    fi

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Detected Windows system"
    echo "Please install Noto Sans Devanagari font manually:"
    echo "   1. Visit: https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari"
    echo "   2. Click 'Download family'"
    echo "   3. Extract and install all .ttf files"
    echo "   4. Restart your terminal/IDE"
else
    echo "⚠️ Unknown operating system"
    echo "Please install Noto Sans Devanagari font manually"
fi

echo ""
echo "Verification: Checking for Devanagari font files..."

# Check for font files
FONT_LOCATIONS=(
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    "/Library/Fonts/Noto Sans Devanagari.ttf"
    "C:/Windows/Fonts/NotoSansDevanagari-Regular.ttf"
)

FOUND=false
for font_path in "${FONT_LOCATIONS[@]}"; do
    if [ -f "$font_path" ]; then
        echo "✅ Found: $font_path"
        FOUND=true
    fi
done

if [ "$FOUND" = false ]; then
    echo "⚠️ No Devanagari fonts found in standard locations"
    echo "Please check font installation"
else
    echo ""
    echo "✅ Setup complete! Devanagari fonts are ready."
fi

echo ""
echo "You can now run your application:"
echo "  streamlit run app.py"