"""
PDF Reader Tool

This module provides functionality to read PDF files and convert them to
human-readable text format with proper formatting and structure preservation.
"""

import os
import re
from pathlib import Path
from typing import Any

try:
    import pdfplumber

    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2

    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

from loguru import logger


class PDFReader:
    """
    A comprehensive PDF reader that extracts text and formats it for human readability.

    This class provides methods to read PDF files and convert them to well-formatted
    text files that preserve the original structure while being highly readable.
    """

    def __init__(self, preserve_layout: bool = True, remove_extra_whitespace: bool = True):
        """
        Initialize the PDF reader.

        Args:
            preserve_layout: Whether to attempt to preserve the original layout
            remove_extra_whitespace: Whether to clean up excessive whitespace
        """
        self.preserve_layout = preserve_layout
        self.remove_extra_whitespace = remove_extra_whitespace

        if not PDFPLUMBER_AVAILABLE and not PYPDF2_AVAILABLE:
            raise ImportError(
                "Neither pdfplumber nor PyPDF2 is available. "
                "Please install at least one: pip install pdfplumber PyPDF2"
            )

    def _clean_text(self, text: str) -> str:
        """
        Clean and format extracted text for better readability.

        Args:
            text: Raw text extracted from PDF

        Returns:
            Cleaned and formatted text
        """
        if not text:
            return ""

        # Remove excessive whitespace but preserve intentional spacing
        if self.remove_extra_whitespace:
            # Replace multiple spaces with single space
            text = re.sub(r" +", " ", text)
            # Replace multiple newlines with maximum of two
            text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
            # Remove trailing spaces from lines
            text = re.sub(r" +\n", "\n", text)

        # Fix common PDF extraction issues
        # Fix broken words split across lines
        text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

        # Improve paragraph detection
        # Add double newline before lines that start with capital letters (likely new paragraphs)
        text = re.sub(r"\n([A-Z][a-z])", r"\n\n\1", text)

        # Fix spacing around punctuation
        text = re.sub(r"\s+([.,:;!?])", r"\1", text)
        text = re.sub(r"([.!?])\s*([A-Z])", r"\1 \2", text)

        return text.strip()

    def _extract_with_pdfplumber(self, pdf_path: str) -> tuple[str, dict[str, Any]]:
        """
        Extract text using pdfplumber (preferred method).

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (extracted_text, metadata)
        """
        text_content = []
        metadata = {"pages": 0, "method": "pdfplumber"}

        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata["pages"] = len(pdf.pages)
                metadata["title"] = pdf.metadata.get("Title", "")
                metadata["author"] = pdf.metadata.get("Author", "")
                metadata["subject"] = pdf.metadata.get("Subject", "")

                for page_num, page in enumerate(pdf.pages, 1):
                    logger.debug(f"Processing page {page_num}/{len(pdf.pages)}")

                    # Extract text with layout preservation if requested
                    if self.preserve_layout:
                        page_text = page.extract_text(layout=True)
                    else:
                        page_text = page.extract_text()

                    if page_text:
                        # Add page separator for multi-page documents
                        if page_num > 1:
                            text_content.append(f"\n{'=' * 50} PAGE {page_num} {'=' * 50}\n")
                        text_content.append(page_text)
                    else:
                        logger.warning(f"No text found on page {page_num}")

        except Exception as e:
            logger.error(f"Error extracting with pdfplumber: {e}")
            raise

        return "\n".join(text_content), metadata

    def _extract_with_pypdf2(self, pdf_path: str) -> tuple[str, dict[str, Any]]:
        """
        Extract text using PyPDF2 (fallback method).

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (extracted_text, metadata)
        """
        text_content = []
        metadata = {"pages": 0, "method": "PyPDF2"}

        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata["pages"] = len(pdf_reader.pages)

                # Extract metadata
                if pdf_reader.metadata:
                    metadata["title"] = pdf_reader.metadata.get("/Title", "")
                    metadata["author"] = pdf_reader.metadata.get("/Author", "")
                    metadata["subject"] = pdf_reader.metadata.get("/Subject", "")

                for page_num, page in enumerate(pdf_reader.pages, 1):
                    logger.debug(f"Processing page {page_num}/{len(pdf_reader.pages)}")

                    page_text = page.extract_text()

                    if page_text:
                        # Add page separator for multi-page documents
                        if page_num > 1:
                            text_content.append(f"\n{'=' * 50} PAGE {page_num} {'=' * 50}\n")
                        text_content.append(page_text)
                    else:
                        logger.warning(f"No text found on page {page_num}")

        except Exception as e:
            logger.error(f"Error extracting with PyPDF2: {e}")
            raise

        return "\n".join(text_content), metadata

    def read_pdf(self, pdf_path: str) -> tuple[str, dict[str, Any]]:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (extracted_text, metadata)

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If PDF extraction fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        logger.info(f"Reading PDF: {pdf_path}")

        # Try pdfplumber first (better layout preservation)
        if PDFPLUMBER_AVAILABLE:
            try:
                text, metadata = self._extract_with_pdfplumber(pdf_path)
                logger.info("Successfully extracted text using pdfplumber")
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}")
                if PYPDF2_AVAILABLE:
                    logger.info("Falling back to PyPDF2")
                    text, metadata = self._extract_with_pypdf2(pdf_path)
                else:
                    raise
        elif PYPDF2_AVAILABLE:
            text, metadata = self._extract_with_pypdf2(pdf_path)
            logger.info("Successfully extracted text using PyPDF2")
        else:
            raise RuntimeError("No PDF extraction library available")

        # Clean and format the text
        cleaned_text = self._clean_text(text)

        return cleaned_text, metadata

    def pdf_to_txt(
        self,
        pdf_path: str,
        output_path: str | None = None,
        include_metadata: bool = True,
        encoding: str = "utf-8",
    ) -> str:
        """
        Convert a PDF file to a formatted text file.

        Args:
            pdf_path: Path to the input PDF file
            output_path: Path for the output text file (optional)
            include_metadata: Whether to include PDF metadata in the output
            encoding: Text file encoding (default: utf-8)

        Returns:
            Path to the created text file

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If conversion fails
        """
        # Extract text and metadata
        text_content, metadata = self.read_pdf(pdf_path)

        # Generate output path if not provided
        if output_path is None:
            pdf_name = Path(pdf_path).stem
            output_path = f"{pdf_name}_readable.txt"

        # Prepare the final content
        final_content = []

        # Add metadata header if requested
        if include_metadata and metadata:
            final_content.append("=" * 80)
            final_content.append("DOCUMENT METADATA")
            final_content.append("=" * 80)

            for key, value in metadata.items():
                if value:  # Only include non-empty values
                    final_content.append(f"{key.title()}: {value}")

            final_content.append("\n" + "=" * 80)
            final_content.append("DOCUMENT CONTENT")
            final_content.append("=" * 80 + "\n")

        # Add the main content
        final_content.append(text_content)

        # Write to file
        try:
            with open(output_path, "w", encoding=encoding) as f:
                f.write("\n".join(final_content))

            logger.info(f"Successfully created readable text file: {output_path}")
            logger.info(f"Extracted {metadata.get('pages', 'unknown')} pages")

            return output_path

        except Exception as e:
            logger.error(f"Error writing text file: {e}")
            raise


def convert_pdf_to_readable_text(
    pdf_path: str,
    output_path: str | None = None,
    preserve_layout: bool = True,
    include_metadata: bool = True,
) -> str:
    """
    Convenience function to convert a PDF to human-readable text.

    Args:
        pdf_path: Path to the PDF file
        output_path: Output path for the text file (optional)
        preserve_layout: Whether to preserve the original layout
        include_metadata: Whether to include document metadata

    Returns:
        Path to the created text file
    """
    reader = PDFReader(preserve_layout=preserve_layout)
    return reader.pdf_to_txt(
        pdf_path=pdf_path, output_path=output_path, include_metadata=include_metadata
    )


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_reader.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result_path = convert_pdf_to_readable_text(pdf_file, output_file)
        print(f"Successfully converted PDF to readable text: {result_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
