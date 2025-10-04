"""
Pytest configuration and fixtures for PDF Reader MCP Server tests
"""

import os
import tempfile
from pathlib import Path
import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_reader_server import documents


@pytest.fixture
def sample_pdf_path():
    """Create a sample PDF for testing"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

    c = canvas.Canvas(temp_file.name, pagesize=letter)
    c.drawString(100, 750, "PDF Reader MCP Server Test Document")
    c.drawString(100, 700, "This is page 1 of the test PDF.")
    c.drawString(100, 650, "It contains some sample text to search for.")
    c.drawString(100, 600, "Keywords: neural network, machine learning")
    c.showPage()

    c.drawString(100, 750, "Page 2 - Second Page")
    c.drawString(100, 700, "This is the second page of the test PDF.")
    c.drawString(100, 650, "More content here for testing.")
    c.drawString(100, 600, "Search terms: artificial intelligence, deep learning")
    c.save()

    yield temp_file.name

    # Cleanup
    os.unlink(temp_file.name)


@pytest.fixture
def complex_pdf_path():
    """Create a more complex PDF with multiple pages and content"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

    c = canvas.Canvas(temp_file.name, pagesize=letter)

    # Create 5 pages with different content
    for i in range(1, 6):
        c.drawString(100, 750, f"Page {i} - Complex Test Document")
        c.drawString(100, 700, f"This is content for page {i}.")
        c.drawString(100, 650, f"Special term on page {i}: reinforcement learning")
        c.drawString(100, 600, f"Page {i} contains text about neural networks and AI.")

        if i == 3:
            c.drawString(100, 550, "Unique content only on page 3")
            c.drawString(100, 500, "Algorithm: Q-learning, deep Q-networks")

        if i == 5:
            c.drawString(100, 550, "Final page with conclusion")
            c.drawString(100, 500, "Summary: machine learning frameworks")

        c.showPage()

    c.save()

    yield temp_file.name

    # Cleanup
    os.unlink(temp_file.name)


@pytest.fixture(autouse=True)
def cleanup_documents():
    """Clean up documents after each test"""
    yield

    # Close and clear all documents
    for doc_id in list(documents.keys()):
        try:
            if doc_id in documents:
                documents[doc_id].close()
                del documents[doc_id]
        except Exception:
            pass