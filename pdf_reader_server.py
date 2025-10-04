#!/usr/bin/env python3
"""
PDF Reader MCP Server - An MCP server for reading and searching PDF files using FastMCP
"""

import asyncio
import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF is required. Install with: pip install PyMuPDF")

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("pdf-reader")

# Global document store
documents: Dict[str, fitz.Document] = {}


def generate_doc_id() -> str:
    """Generate a unique document ID"""
    return str(uuid.uuid4())


@mcp.tool()
def open_pdf(path: str) -> str:
    """Open a PDF file and return a document ID

    Args:
        path: Path to the PDF file
    """
    # Security check - only allow certain paths
    allowed_paths = ["/Users", "/tmp", os.getcwd(), tempfile.gettempdir()]
    if not any(Path(path).resolve().is_relative_to(Path(allowed_path).resolve()) for allowed_path in allowed_paths):
        raise ValueError(f"Access denied for path: {path}")

    try:
        doc = fitz.open(path)
        doc_id = generate_doc_id()
        documents[doc_id] = doc
        return doc_id
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF: {str(e)}")


@mcp.tool()
def page_count(doc_id: str) -> int:
    """Get the number of pages in a PDF document

    Args:
        doc_id: Document ID returned by open_pdf
    """
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")

    doc = documents[doc_id]
    return doc.page_count


@mcp.tool()
def extract_text(doc_id: str, page: int) -> str:
    """Extract text from a specific page

    Args:
        doc_id: Document ID returned by open_pdf
        page: Page number (1-based)
    """
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")

    doc = documents[doc_id]

    if page < 1 or page > doc.page_count:
        raise ValueError(f"Page number out of range. Valid range: 1-{doc.page_count}")

    try:
        page_obj = doc[page - 1]  # Convert to 0-based
        return page_obj.get_text()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {str(e)}")


@mcp.tool()
def render_page_png(doc_id: str, page: int, dpi: int = 144) -> str:
    """Render a page as PNG image

    Args:
        doc_id: Document ID returned by open_pdf
        page: Page number (1-based)
        dpi: Resolution in DPI (default: 144)
    """
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")

    doc = documents[doc_id]

    if page < 1 or page > doc.page_count:
        raise ValueError(f"Page number out of range. Valid range: 1-{doc.page_count}")

    try:
        page_obj = doc[page - 1]  # Convert to 0-based
        pix = page_obj.get_pixmap(dpi=dpi)

        # Save to temporary file
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"pdf_page_{page}_{uuid.uuid4().hex[:8]}.png")
        pix.save(temp_file)
        return temp_file
    except Exception as e:
        raise RuntimeError(f"Failed to render page: {str(e)}")


@mcp.tool()
def search_text(doc_id: str, query: str, max_hits: int = 20) -> str:
    """Search for text in the PDF document

    Args:
        doc_id: Document ID returned by open_pdf
        query: Text to search for
        max_hits: Maximum number of results (default: 20)
    """
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")

    if not query:
        raise ValueError("Missing required parameter: query")

    doc = documents[doc_id]
    results = []

    try:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text_instances = page.search_for(query)

            for inst in text_instances:
                # Extract surrounding text
                rect = inst
                surrounding_rect = fitz.Rect(
                    rect.x0 - 50, rect.y0 - 20,
                    rect.x1 + 50, rect.y1 + 20
                )
                surrounding_text = page.get_text("text", clip=surrounding_rect)

                results.append({
                    "page": page_num + 1,  # Convert to 1-based
                    "text": surrounding_text.strip(),
                    "bbox": [rect.x0, rect.y0, rect.x1, rect.y1]
                })

                if len(results) >= max_hits:
                    break

            if len(results) >= max_hits:
                break

        return json.dumps(results, indent=2)
    except Exception as e:
        raise RuntimeError(f"Failed to search text: {str(e)}")


@mcp.tool()
def close_pdf(doc_id: str) -> str:
    """Close a PDF document and free resources

    Args:
        doc_id: Document ID returned by open_pdf
    """
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")

    try:
        doc = documents[doc_id]
        doc.close()
        del documents[doc_id]
        return "Document closed successfully"
    except Exception as e:
        raise RuntimeError(f"Failed to close document: {str(e)}")


if __name__ == "__main__":
    # Run the server
    mcp.run()