"""
Unit tests for PDF Reader MCP Server tools
"""

import json
import os
import tempfile
from pathlib import Path
import pytest

from pdf_reader_server import (
    open_pdf, page_count, extract_text, search_text,
    close_pdf, render_page_png, documents, generate_doc_id
)


class TestDocIdGeneration:
    """Test document ID generation"""

    def test_generate_doc_id(self):
        """Test that doc IDs are unique"""
        id1 = generate_doc_id()
        id2 = generate_doc_id()
        assert id1 != id2
        assert isinstance(id1, str)
        assert isinstance(id2, str)


class TestOpenPdf:
    """Test open_pdf function"""

    def test_open_pdf_success(self, sample_pdf_path):
        """Test successful PDF opening"""
        doc_id = open_pdf(sample_pdf_path)
        assert isinstance(doc_id, str)
        assert doc_id in documents
        assert documents[doc_id].page_count == 2

    def test_open_pdf_nonexistent_file(self):
        """Test opening non-existent file"""
        with pytest.raises(RuntimeError, match="Failed to open PDF"):
            open_pdf("/tmp/nonexistent.pdf")

    def test_open_pdf_denied_path(self):
        """Test path security restrictions"""
        denied_path = "/etc/passwd"
        with pytest.raises(ValueError, match="Access denied"):
            open_pdf(denied_path)

    def test_open_pdf_invalid_file(self):
        """Test opening invalid file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False) as f:
            f.write("This is not a PDF file")
            invalid_path = f.name

        try:
            with pytest.raises(RuntimeError, match="Failed to open PDF"):
                open_pdf(invalid_path)
        finally:
            os.unlink(invalid_path)


class TestPageCount:
    """Test page_count function"""

    def test_page_count_valid_doc(self, sample_pdf_path):
        """Test getting page count for valid document"""
        doc_id = open_pdf(sample_pdf_path)
        count = page_count(doc_id)
        assert count == 2
        assert isinstance(count, int)

    def test_page_count_invalid_doc_id(self):
        """Test page count with invalid doc ID"""
        with pytest.raises(ValueError, match="Invalid or missing doc_id"):
            page_count("invalid_doc_id")


class TestExtractText:
    """Test extract_text function"""

    def test_extract_text_valid_page(self, sample_pdf_path):
        """Test extracting text from valid page"""
        doc_id = open_pdf(sample_pdf_path)
        text = extract_text(doc_id, 1)
        assert isinstance(text, str)
        assert "PDF Reader MCP Server Test Document" in text
        assert "neural network" in text

    def test_extract_text_page_out_of_range(self, sample_pdf_path):
        """Test extracting text from non-existent page"""
        doc_id = open_pdf(sample_pdf_path)
        with pytest.raises(ValueError, match="Page number out of range"):
            extract_text(doc_id, 99)

    def test_extract_text_invalid_doc_id(self):
        """Test extracting text with invalid doc ID"""
        with pytest.raises(ValueError, match="Invalid or missing doc_id"):
            extract_text("invalid_doc_id", 1)


class TestSearchText:
    """Test search_text function"""

    def test_search_text_existing_term(self, sample_pdf_path):
        """Test searching for existing text"""
        doc_id = open_pdf(sample_pdf_path)
        results_json = search_text(doc_id, "neural", 10)
        results = json.loads(results_json)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all("page" in result for result in results)
        assert all("text" in result for result in results)

    def test_search_text_nonexistent_term(self, sample_pdf_path):
        """Test searching for non-existent text"""
        doc_id = open_pdf(sample_pdf_path)
        results_json = search_text(doc_id, "nonexistent_term_xyz", 10)
        results = json.loads(results_json)

        assert isinstance(results, list)
        assert len(results) == 0

    def test_search_text_empty_query(self, sample_pdf_path):
        """Test searching with empty query"""
        doc_id = open_pdf(sample_pdf_path)
        with pytest.raises(ValueError, match="Missing required parameter: query"):
            search_text(doc_id, "", 10)


class TestRenderPagePng:
    """Test render_page_png function"""

    def test_render_page_png_valid(self, sample_pdf_path):
        """Test rendering valid page"""
        doc_id = open_pdf(sample_pdf_path)
        png_path = render_page_png(doc_id, 1, 72)

        assert os.path.exists(png_path)
        assert os.path.getsize(png_path) > 0
        assert png_path.endswith('.png')

        # Cleanup
        os.unlink(png_path)


class TestClosePdf:
    """Test close_pdf function"""

    def test_close_pdf_valid(self, sample_pdf_path):
        """Test closing valid document"""
        doc_id = open_pdf(sample_pdf_path)
        assert doc_id in documents

        result = close_pdf(doc_id)
        assert result == "Document closed successfully"
        assert doc_id not in documents

    def test_close_pdf_invalid_doc_id(self):
        """Test closing with invalid doc ID"""
        with pytest.raises(ValueError, match="Invalid or missing doc_id"):
            close_pdf("invalid_doc_id")


class TestIntegration:
    """Integration tests combining multiple operations"""

    def test_complete_workflow(self, complex_pdf_path):
        """Test complete workflow with all operations"""
        # Open document
        doc_id = open_pdf(complex_pdf_path)
        assert doc_id in documents

        # Get page count
        count = page_count(doc_id)
        assert count == 5

        # Extract text from multiple pages
        text1 = extract_text(doc_id, 1)
        text3 = extract_text(doc_id, 3)
        assert "Page 1" in text1
        assert "Page 3" in text3

        # Search for specific terms
        results_json = search_text(doc_id, "reinforcement", 10)
        results = json.loads(results_json)
        assert len(results) >= 5

        # Render page as image
        png_path = render_page_png(doc_id, 2, 100)
        assert os.path.exists(png_path)

        # Close document
        result = close_pdf(doc_id)
        assert result == "Document closed successfully"

        # Cleanup
        os.unlink(png_path)