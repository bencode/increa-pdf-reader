# PDF Reader MCP Server

A Model Context Protocol (MCP) server for reading and searching PDF files.

## Installation

### Option 1: One-click Installation

```bash
git clone https://github.com/your-username/pdf-reader-mcp.git
cd pdf-reader-mcp
./install.sh
```

### Option 2: Using pip

#### For users (install from PyPI):
```bash
pip install pdf-reader-mcp
```

#### For developers (install from source):
```bash
git clone https://github.com/your-username/pdf-reader-mcp.git
cd pdf-reader-mcp
pip install -e .
```

### Option 3: Using uv

#### Install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Install project:
```bash
git clone https://github.com/your-username/pdf-reader-mcp.git
cd pdf-reader-mcp
uv sync
```

### Option 4: Traditional venv + pip

```bash
git clone https://github.com/your-username/pdf-reader-mcp.git
cd pdf-reader-mcp
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Development Setup

Install with development dependencies:
```bash
# Using pip
pip install -e ".[dev]"

# Or using uv
uv sync --dev
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

# Using uv
uv run mcp dev pdf_reader_server.py

# Or using the installed script
pdf-reader-mcp
```

### 2. Install to Claude Code

#### Method A: Automatic installation
```bash
# From project directory
mcp install pdf_reader_server.py

# Or using uv
uv run mcp install pdf_reader_server.py
```

#### Method B: Manual configuration
Add to `~/.claude/claude_desktop_config.json`:
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

#### Method C: Using installed package
```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "pdf-reader-mcp"
    }
  }
}
```

### 3. Using in Claude Code

Once installed, you can use the PDF Reader tools directly in Claude Code conversations:

#### Basic Workflow
```
Please help me read the PDF file "research_paper.pdf" on my desktop.
```

Claude will automatically:
1. Open the PDF using `open_pdf()`
2. Get the page count using `page_count()`
3. Extract text from relevant pages using `extract_text()`

#### Example Prompts

**Read specific pages:**
```
Read page 5 of the document.pdf and summarize the key points.
```

**Search for content:**
```
Search for "machine learning" in all PDFs in my Documents folder and tell me what you find.
```

**Extract and analyze:**
```
Open the contract.pdf, extract all text from pages 1-3, and identify the key obligations.
```

**Render pages as images:**
```
Render page 10 of presentation.pdf as a high-resolution PNG image.
```

**Multi-document analysis:**
```
Compare the methodologies described in paper1.pdf and paper2.pdf.
```

#### Available Tools
The server provides these tools that Claude can use:

1. **open_pdf(path)** - Open PDF and return doc_id
2. **page_count(doc_id)** - Get number of pages
3. **extract_text(doc_id, page)** - Extract text from page
4. **render_page_png(doc_id, page, dpi)** - Render page as PNG
5. **search_text(doc_id, query, max_hits)** - Search for text
6. **close_pdf(doc_id)** - Close document

#### Tips for Claude Code Usage

- **File paths**: Use absolute paths or paths relative to your current working directory
- **Batch processing**: Claude can automatically handle multiple PDF files
- **Security**: Only files in allowed directories can be accessed (home, temp, current directory)
- **Memory management**: Claude automatically closes documents when done

### 4. Using as MCP Server

The server can also be used with other MCP-compatible clients using the tools listed above.

## Example Usage

```
doc_id = open_pdf(path="document.pdf")
count = page_count(doc_id=doc_id)
text = extract_text(doc_id=doc_id, page=1)
png_path = render_page_png(doc_id=doc_id, page=1, dpi=200)
results = search_text(doc_id=doc_id, query="neural network")
close_pdf(doc_id=doc_id)
```

## Requirements

- Python 3.10+
- PyMuPDF for PDF processing
- MCP for Model Context Protocol

## Security

The server includes path security restrictions and only allows access to specific directories:
- User home directory (`/Users` on macOS)
- System temp directory (`/tmp`)
- Current working directory
- Python temp directory

## Development

### Code Quality

```bash
# Run linting
ruff check .

# Format code
ruff format .

# Using uv
uv run ruff check .
uv run ruff format .
```

### Project Structure

```
pdf-reader-mcp/
├── pdf_reader_server.py    # Main MCP server implementation
├── tests/                  # Test suite
│   ├── test_pdf_tools.py   # PDF tool tests
│   ├── test_mcp_integration.py  # MCP integration tests
│   └── conftest.py         # Test fixtures
├── pyproject.toml         # Project configuration and dependencies
├── requirements.txt       # Legacy requirements file
└── README.md              # This file
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
