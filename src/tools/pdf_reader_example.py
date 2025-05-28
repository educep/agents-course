"""
Example usage of the PDF Reader tool

This script demonstrates various ways to use the PDF reader to convert
PDF files to human-readable text format.
"""
# Standard imports
import sys
from pathlib import Path

# Internal imports
from src.tools.pdf_reader import PDFReader, convert_pdf_to_readable_text


def basic_usage_example(pdf_path: str):
    """
    Basic usage example using the convenience function.
    """
    print("=== Basic Usage Example ===")

    try:
        # Simple conversion with default settings
        output_path = convert_pdf_to_readable_text(pdf_path)
        print(f"✅ Successfully converted PDF to: {output_path}")

        # Read the first few lines to show the result
        with open(output_path, encoding="utf-8") as f:
            preview = f.read(500)
            print("\nPreview of converted text:")
            print("-" * 50)
            print(preview + "..." if len(preview) == 500 else preview)

    except Exception as e:
        print(f"❌ Error: {e}")


def advanced_usage_example(pdf_path: str):
    """
    Advanced usage example using the PDFReader class directly.
    """
    print("\n=== Advanced Usage Example ===")

    try:
        # Create reader with custom settings
        reader = PDFReader(preserve_layout=True, remove_extra_whitespace=True)

        # Extract text and metadata separately
        text_content, metadata = reader.read_pdf(pdf_path)

        print("📄 Document metadata:")
        for key, value in metadata.items():
            if value:
                print(f"   {key.title()}: {value}")

        print("\n📝 Text preview (first 300 characters):")
        print("-" * 50)
        print(text_content[:300] + "..." if len(text_content) > 300 else text_content)

        # Save with custom output path and settings
        custom_output = f"custom_{Path(pdf_path).stem}.txt"
        result_path = reader.pdf_to_txt(
            pdf_path=pdf_path, output_path=custom_output, include_metadata=True
        )

        print(f"\n✅ Saved to custom location: {result_path}")

    except Exception as e:
        print(f"❌ Error: {e}")


def compare_extraction_methods(pdf_path: str):
    """
    Compare different extraction methods and settings.
    """
    print("\n=== Extraction Methods Comparison ===")

    try:
        # Method 1: With layout preservation
        reader_with_layout = PDFReader(preserve_layout=True)
        text_with_layout, _ = reader_with_layout.read_pdf(pdf_path)

        # Method 2: Without layout preservation
        reader_without_layout = PDFReader(preserve_layout=False)
        text_without_layout, _ = reader_without_layout.read_pdf(pdf_path)

        print(f"📊 Text length with layout preservation: {len(text_with_layout)} chars")
        print(f"📊 Text length without layout preservation: {len(text_without_layout)} chars")

        # Save both versions
        output_with_layout = f"{Path(pdf_path).stem}_with_layout.txt"
        output_without_layout = f"{Path(pdf_path).stem}_without_layout.txt"

        reader_with_layout.pdf_to_txt(pdf_path, output_with_layout)
        reader_without_layout.pdf_to_txt(pdf_path, output_without_layout)

        print(f"✅ Saved layout-preserved version: {output_with_layout}")
        print(f"✅ Saved standard version: {output_without_layout}")

    except Exception as e:
        print(f"❌ Error: {e}")


def batch_processing_example(pdf_directory: str):
    """
    Example of processing multiple PDFs in a directory.
    """
    print("\n=== Batch Processing Example ===")

    pdf_dir = Path(pdf_directory)
    if not pdf_dir.exists():
        print(f"❌ Directory not found: {pdf_directory}")
        return

    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in: {pdf_directory}")
        return

    print(f"📁 Found {len(pdf_files)} PDF files")

    reader = PDFReader()
    results = []

    for pdf_file in pdf_files:
        try:
            print(f"🔄 Processing: {pdf_file.name}")
            output_path = reader.pdf_to_txt(str(pdf_file))
            results.append((pdf_file.name, output_path, "Success"))
            print(f"   ✅ Converted to: {output_path}")

        except Exception as e:
            results.append((pdf_file.name, None, f"Error: {e}"))
            print(f"   ❌ Failed: {e}")

    # Summary
    print("\n📋 Batch Processing Summary:")
    successful = len([r for r in results if r[2] == "Success"])
    print(f"   Successfully processed: {successful}/{len(pdf_files)} files")

    if successful < len(pdf_files):
        print("   Failed files:")
        for name, _, status in results:
            if status != "Success":
                print(f"   - {name}: {status}")


def main():
    """
    Main function to run examples based on command line arguments.
    """
    if len(sys.argv) < 2:
        print("PDF Reader Examples")
        print("===================")
        print("")
        print("Usage:")
        print("  python pdf_reader_example.py <pdf_path>                    # Basic example")
        print("  python pdf_reader_example.py <pdf_path> --advanced         # Advanced example")
        print("  python pdf_reader_example.py <pdf_path> --compare          # Compare methods")
        print("  python pdf_reader_example.py --batch <directory>           # Batch processing")
        print("")
        print("Examples:")
        print("  python pdf_reader_example.py document.pdf")
        print("  python pdf_reader_example.py document.pdf --advanced")
        print("  python pdf_reader_example.py --batch ./pdf_folder/")
        return

    if "--batch" in sys.argv:
        if len(sys.argv) >= 3:
            directory = sys.argv[2] if sys.argv[1] == "--batch" else sys.argv[1]
            batch_processing_example(directory)
        else:
            print("❌ Please provide a directory path for batch processing")
        return

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return

    # Run examples based on arguments
    if "--advanced" in sys.argv:
        basic_usage_example(pdf_path)
        advanced_usage_example(pdf_path)
    elif "--compare" in sys.argv:
        basic_usage_example(pdf_path)
        compare_extraction_methods(pdf_path)
    else:
        basic_usage_example(pdf_path)

    print("\n🎉 All examples completed!")


if __name__ == "__main__":
    main()
