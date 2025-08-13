#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0 <transcription_file> [options]"
    echo ""
    echo -e "${BLUE}Options:${NC}"
    echo "  --voice <voice>         Select voice (default: bm_george)"
    echo "                          Available voices: bm_george, bm_daniel, bm_lewis,"
    echo "                                           bm_fable, am_adam, af_bella, am_santa"
    echo "  --speed <speed>         Audio speed (default: 1.0)"
    echo "  --output <output_path>  Output file path (default: output.wav)"
    echo "  -h, --help              For help information"
    echo ""
    echo -e "${BLUE}Example:${NC}"
    echo "  $0 transcript.txt"
    echo "  $0 transcript.txt --voice af_bella --speed 1.2 --output my_audio.wav"
}

check_uv() {
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}Error: uv not found. Installing uv first.${NC}"
        echo "Installing uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
}

check_input_file() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: File transcription is requirement.${NC}"
        usage
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        echo -e "${RED}Error: File '$1' not found.${NC}"
        exit 1
    fi
}

main() {
    if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        usage
        exit 0
    fi
    
    # Check uv
    check_uv

    TRANSCRIPTION_FILE="$1"
    shift
    
    # Check file input
    check_input_file "$TRANSCRIPTION_FILE"
    
    echo -e "${GREEN}Starting text-to-speech...${NC}"
    echo -e "${BLUE}File input: ${NC}$TRANSCRIPTION_FILE"
    
    echo -e "${YELLOW}Pending...${NC}"
    
    if uv run main.py "$TRANSCRIPTION_FILE" "$@"; then
        echo -e "${GREEN}Finish! Let check. ${NC}"

        if [ -f "output.wav" ]; then
            echo -e "${BLUE}File name: output.wav${NC}"
            echo -e "${BLUE}File size: $(ls -lh output.wav | awk '{print $5}')${NC}"
        fi
    else
        echo -e "${RED}Error.${NC}"
        exit 1
    fi
}

main "$@"
