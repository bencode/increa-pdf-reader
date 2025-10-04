# Development Guidelines

## Programming Style

This project follows **functional programming** principles and preferences.

### Key Principles

1. **Function-First Design**
   - Prefer functions over classes when possible
   - Use pure functions without side effects
   - Keep functions small and focused

2. **Simple Data Structures**
   - Use built-in types (dict, list, str) over complex classes
   - Avoid unnecessary object-oriented abstractions
   - Prefer composition over inheritance

3. **Minimal Dependencies**
   - Only import what is actually used
   - Avoid over-engineering
   - Keep the codebase lean

4. **Code Organization**
   - Group related functionality in simple functions
   - Use helper functions for validation and common operations
   - Keep the code structure flat and readable

### Examples

#### ✅ Preferred: Functional Style
```python
def _validate_doc_id(doc_id: str) -> fitz.Document:
    """Validate and return document by ID"""
    if doc_id not in documents:
        raise ValueError("Invalid or missing doc_id")
    return documents[doc_id]

@mcp.tool()
def page_count(doc_id: str) -> int:
    """Get the number of pages in a PDF document"""
    doc = _validate_doc_id(doc_id)
    return doc.page_count
```

#### ❌ Avoid: Object-Oriented Style
```python
class PDFReader:
    def __init__(self):
        self.documents = {}

    def _validate_doc_id(self, doc_id: str):
        # validation logic

    def page_count(self, doc_id: str):
        doc = self._validate_doc_id(doc_id)
        return doc.page_count
```

### Testing Style

Follow the same functional approach in tests:

- Use flat test functions instead of test classes
- Prefer simple assertions
- Keep test setup minimal
- Focus on testing behavior, not implementation

```python
def test_page_count_valid_doc(sample_pdf_path):
    """Test getting page count for valid document"""
    doc_id = open_pdf(sample_pdf_path)
    count = page_count(doc_id)
    assert count == 2
    assert isinstance(count, int)
```

### Rationale

Functional programming in Python provides:
- **Simplicity**: Less boilerplate and clearer intent
- **Testability**: Pure functions are easier to test
- **Maintainability**: Fewer abstractions mean easier changes
- **Performance**: Less overhead from unnecessary objects

This style aligns with Python's philosophy: "Simple is better than complex."