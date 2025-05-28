# PDF Reader Tool

A comprehensive Python tool for converting PDF files to human-readable text format with intelligent formatting and structure preservation.

## Features

- **Dual Library Support**: Uses `pdfplumber` (preferred) with `PyPDF2` fallback for maximum compatibility
- **Layout Preservation**: Maintains original document structure when possible
- **Intelligent Text Cleaning**:
  - Fixes hyphenated words split across lines
  - Removes excessive whitespace while preserving intentional spacing
  - Improves paragraph detection
  - Fixes spacing around punctuation
- **Metadata Extraction**: Extracts and includes document metadata (title, author, subject)
- **Page Separation**: Clearly separates multi-page documents
- **Customizable Output**: Flexible formatting options and output paths
- **Robust Error Handling**: Graceful fallbacks and informative error messages
- **Batch Processing Support**: Process multiple PDFs at once

## Installation

First, install the required dependencies:

```bash
pip install pdfplumber PyPDF2
```

These are already included in the project's `requirements.txt`.

## Quick Start

### Basic Usage

```python
from tools.pdf_reader import convert_pdf_to_readable_text

# Convert a PDF to readable text (simplest usage)
output_path = convert_pdf_to_readable_text("document.pdf")
print(f"Converted PDF saved to: {output_path}")
```

### Advanced Usage

```python
from tools.pdf_reader import PDFReader

# Create reader with custom settings
reader = PDFReader(
    preserve_layout=True,        # Maintain original layout
    remove_extra_whitespace=True # Clean up excessive whitespace
)

# Extract text and metadata
text_content, metadata = reader.read_pdf("document.pdf")

# Save with custom options
output_path = reader.pdf_to_txt(
    pdf_path="document.pdf",
    output_path="my_custom_output.txt",
    include_metadata=True,
    encoding="utf-8"
)
```

## Command Line Usage

You can also use the tool directly from the command line:

```bash
# Basic conversion
python src/tools/pdf_reader.py document.pdf

# Specify output file
python src/tools/pdf_reader.py document.pdf output.txt
```

## API Reference

### `PDFReader` Class

#### Constructor
```python
PDFReader(preserve_layout=True, remove_extra_whitespace=True)
```

**Parameters:**
- `preserve_layout` (bool): Whether to attempt to preserve the original layout
- `remove_extra_whitespace` (bool): Whether to clean up excessive whitespace

#### Methods

##### `read_pdf(pdf_path: str) -> tuple[str, Dict[str, Any]]`
Extract text from a PDF file.

**Parameters:**
- `pdf_path` (str): Path to the PDF file

**Returns:**
- Tuple of (extracted_text, metadata_dict)

**Raises:**
- `FileNotFoundError`: If the PDF file doesn't exist
- `Exception`: If PDF extraction fails

##### `pdf_to_txt(pdf_path, output_path=None, include_metadata=True, encoding="utf-8") -> str`
Convert a PDF file to a formatted text file.

**Parameters:**
- `pdf_path` (str): Path to the input PDF file
- `output_path` (str, optional): Path for the output text file
- `include_metadata` (bool): Whether to include PDF metadata in the output
- `encoding` (str): Text file encoding (default: utf-8)

**Returns:**
- Path to the created text file

### Convenience Function

##### `convert_pdf_to_readable_text(pdf_path, output_path=None, preserve_layout=True, include_metadata=True) -> str`
One-function solution for PDF to text conversion.

**Parameters:**
- `pdf_path` (str): Path to the PDF file
- `output_path` (str, optional): Output path for the text file
- `preserve_layout` (bool): Whether to preserve the original layout
- `include_metadata` (bool): Whether to include document metadata

**Returns:**
- Path to the created text file

## Text Processing Features

### Hyphenated Word Fixing
The tool automatically fixes words that are split across lines with hyphens:
```
Input:  "This is a hyp-\nhenated word"
Output: "This is a hyphenated word"
```

### Paragraph Detection
Intelligently detects paragraph breaks and adds appropriate spacing:
```
Input:  "First sentence.\nSecond sentence starts here."
Output: "First sentence.\n\nSecond sentence starts here."
```

### Whitespace Cleaning
Removes excessive whitespace while preserving intentional formatting:
```
Input:  "Hello    world\n\n\n\nNext paragraph"
Output: "Hello world\n\nNext paragraph"
```

### Punctuation Spacing
Fixes spacing around punctuation marks:
```
Input:  "Hello , world ! How are you ?"
Output: "Hello, world! How are you?"
```

## Output Format

The generated text files include:

1. **Metadata Header** (if enabled):
   ```
   ================================================================================
   DOCUMENT METADATA
   ================================================================================
   Title: Document Title
   Author: Document Author
   Pages: 5
   Method: pdfplumber

   ================================================================================
   DOCUMENT CONTENT
   ================================================================================
   ```

2. **Page Separators** (for multi-page documents):
   ```
   ================================================== PAGE 2 ==================================================
   ```

3. **Cleaned Text Content**: The main document text with intelligent formatting

## Examples

### Example 1: Research Paper Processing
```python
from tools.pdf_reader import PDFReader

reader = PDFReader(preserve_layout=True)

# Process academic paper
text, metadata = reader.read_pdf("research_paper.pdf")
print(f"Extracted {metadata['pages']} pages")
print(f"Title: {metadata.get('title', 'N/A')}")

# Save with descriptive filename
output_path = reader.pdf_to_txt(
    "research_paper.pdf",
    "research_paper_readable.txt"
)
```

### Example 2: Batch Processing
```python
from pathlib import Path
from tools.pdf_reader import PDFReader

reader = PDFReader()
pdf_dir = Path("./pdf_documents/")

for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        output_path = reader.pdf_to_txt(str(pdf_file))
        print(f"✅ Converted: {pdf_file.name} -> {output_path}")
    except Exception as e:
        print(f"❌ Failed: {pdf_file.name} - {e}")
```

### Example 3: Custom Formatting
```python
from tools.pdf_reader import PDFReader

# Reader without layout preservation for simpler output
reader = PDFReader(
    preserve_layout=False,
    remove_extra_whitespace=True
)

# Convert without metadata for cleaner output
output_path = reader.pdf_to_txt(
    "document.pdf",
    "clean_output.txt",
    include_metadata=False
)
```

## Error Handling

The tool includes comprehensive error handling:

- **Missing Libraries**: Clear error message if PDF libraries aren't installed
- **File Not Found**: Descriptive error for missing PDF files
- **Extraction Failures**: Automatic fallback between libraries
- **Encoding Issues**: Configurable text encoding
- **Empty PDFs**: Graceful handling of PDFs with no extractable text

## Library Fallback Strategy

1. **Primary**: Uses `pdfplumber` for better layout preservation and table handling
2. **Fallback**: Falls back to `PyPDF2` if pdfplumber fails
3. **Error**: Raises informative error if both libraries fail or are unavailable

## Performance Considerations

- **Memory Usage**: Processes large PDFs efficiently by reading page by page
- **Speed**: `pdfplumber` is generally slower but more accurate; `PyPDF2` is faster
- **Layout Quality**: `pdfplumber` with `layout=True` provides best results for complex layouts

## Troubleshooting

### Common Issues

1. **"Neither pdfplumber nor PyPDF2 is available"**
   - Install the required libraries: `pip install pdfplumber PyPDF2`

2. **Poor text extraction quality**
   - Try with `preserve_layout=False` for simpler documents
   - Some PDFs with complex layouts or images may not extract well

3. **Encoding errors in output**
   - Specify a different encoding: `encoding="latin-1"` or `encoding="cp1252"`

4. **Empty output file**
   - The PDF might be image-based (scanned) - consider OCR tools for these cases
   - Check if the PDF has selectable text

### Performance Optimization

For better performance with large batches:
```python
# Reuse reader instance
reader = PDFReader()
for pdf_file in pdf_files:
    reader.pdf_to_txt(pdf_file)  # Reuses the same reader
```

## Testing

Run the unit tests to verify functionality:
```bash
python -m pytest tests/test_pdf_reader.py -v
```

## License

This tool is part of the agents-course project. See the main LICENSE file for details.
