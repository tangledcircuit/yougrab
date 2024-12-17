# You.com Chat Exporter

A Python script to convert You.com chat conversations into clean markdown files.

## Features

- Extracts complete chat conversations
- Maintains formatting for:
  - Code blocks with language detection
  - Headers
  - Lists
  - Regular text
- Preserves conversation flow between user and AI
- Supports custom AI agent name
- Adds proper markdown code block syntax

## Requirements

- Python 3.6+
- BeautifulSoup4
- re (standard library)

## Installation

```bash
pip install beautifulsoup4
```

## Usage

Basic usage:
```bash
python extract.py -i your_conversation.html -o conversation.md
```

With custom agent name:
```bash
python extract.py -i your_conversation.html -o output.md -n "Dot1Q"
```

## How It Works

1. **HTML Parsing**: Uses BeautifulSoup4 to parse the You.com chat HTML
2. **Content Extraction**: Identifies question/answer pairs using data-testid attributes
3. **Format Conversion**: 
   - Converts HTML headers to markdown headers
   - Maintains code blocks with language detection
   - Preserves list formatting
   - Adds proper markdown syntax for chat participants
4. **Code Block Handling**: Automatically adds `//` to the first line of code blocks if missing

## Arguments

- `-i, --input`: Input HTML file path (required)
- `-o, --output`: Output markdown file path (required)
- `-n, --name`: Custom agent name (default: "Born")

## Example Output

```markdown
**TangledCircuit**: How do I export the chat?

**Born**: Here's how you can export the chat:

### Using the Script

```python
// import beautifulsoup4
from bs4 import BeautifulSoup
```

- Save the chat page as HTML
- Run the script with the saved file
- Check the output markdown
```

## Tips

1. Save the entire You.com chat page using browser's "Save as" feature
2. Make sure to include the .html extension in your input file
3. Check the output markdown file for correct formatting
4. Use the -n flag to match your AI agent's name

## License

MIT