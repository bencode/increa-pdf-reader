# PDF Reader MCP Server

A Model Context Protocol (MCP) server for reading and searching PDF files.

## Installation

### Option 1: Quick Install

```bash
pip install git+https://github.com/bencode/pdf-reader-mcp.git@stable
claude mcp add pdf-reader pdf-reader-mcp
```

### Option 2: Development Setup

```bash
git clone https://github.com/bencode/pdf-reader-mcp.git
cd pdf-reader-mcp
./install.sh
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=pdf_reader_server

# Using uv
uv run pytest tests/ -v
```

## Usage

### 1. Development Mode
```bash
# Using pip installation
mcp dev pdf_reader_server.py

# Or using the installed script
pdf-reader-mcp
```

### 2. Install to Claude Code

Based on the [Claude Code MCP documentation](https://docs.claude.com/en/docs/claude-code/mcp):

```bash
# For Option 1 (quick install) - already configured above ✅

# For Option 2 (development setup) - replace /absolute/path with your actual path
claude mcp add pdf-reader /absolute/path/increa-pdf-reader/.venv/bin/python /absolute/path/increa-pdf-reader/pdf_reader_server.py
```

### 3. Available Tools

The server provides these tools that Claude can use:

1. **open_pdf(path)** - Open PDF and return doc_id
2. **page_count(doc_id)** - Get number of pages
3. **extract_text(doc_id, page)** - Extract text from page
4. **render_page_png(doc_id, page, dpi)** - Render page as PNG
5. **search_text(doc_id, query, max_hits)** - Search for text
6. **close_pdf(doc_id)** - Close document
