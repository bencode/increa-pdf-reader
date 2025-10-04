# PDF Reader MCP Server

A Model Context Protocol (MCP) server for reading and searching PDF files.

## Installation

### 1. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Test the server
```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=pdf_reader_server
```

## Usage

### Development mode
```bash
mcp dev pdf_reader_server.py
```

### Install to Claude Code
```bash
mcp install pdf_reader_server.py
```

### Manual configuration
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "python",
      "args": ["-u", "/ABS/PATH/TO/pdf_reader_server.py"]
    }
  }
}
```

## Available Tools

1. **open_pdf(path)** - Open PDF and return doc_id
2. **page_count(doc_id)** - Get number of pages
3. **extract_text(doc_id, page)** - Extract text from page
4. **render_page_png(doc_id, page, dpi)** - Render page as PNG
5. **search_text(doc_id, query, max_hits)** - Search for text
6. **close_pdf(doc_id)** - Close document

## Example Usage

```
doc_id = open_pdf(path="document.pdf")
count = page_count(doc_id=doc_id)
text = extract_text(doc_id=doc_id, page=1)
png_path = render_page_png(doc_id=doc_id, page=1, dpi=200)
results = search_text(doc_id=doc_id, query="neural network")
close_pdf(doc_id=doc_id)
```