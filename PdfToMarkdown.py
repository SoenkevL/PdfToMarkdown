"""
PDF to Markdown Converter

This module provides functionality to convert PDF documents to Markdown format using the Marker library.
It leverages Ollama's LLM capabilities to enhance the conversion process, extracting structured content
from PDFs and generating well-formatted markdown documents.

The module creates a directory structure for each converted PDF, storing the markdown output,
extracted images, and metadata in a folder named after the PDF file.

Dependencies:
    - marker: For PDF conversion functionality
    - argparse: For command-line argument parsing
    - os: For file and directory operations

Example usage:
    python PdfToMarkdown.py --pdf path/to/document.pdf --output path/to/output_dir
"""

from marker.converters.pdf import PdfConverter
import argparse
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import text_from_rendered, save_output
import os

def parse_pdf(pdf_path: [os.PathLike] = None, output_path :[os.PathLike] = None) -> None:
    """
    Convert a PDF file to Markdown format and save the results.

    This function processes a PDF file using the Marker library and Ollama LLM service,
    converting it to markdown format. It creates a new folder using the PDF's name where
    it stores the markdown content, extracted images, and a meta.json file with metadata.

    The function configures the Marker library to use Ollama's LLM service for enhanced
    text extraction and formatting. The output files will be named exactly like the PDF
    or keep their internal naming from Marker for the extracted images.

    Args:
        pdf_path (os.PathLike): Path to the PDF file to process. Must be a valid file path.
        output_path (os.PathLike): Directory where the output folder will be created.
            If not provided or invalid, the current working directory will be used.

    Returns:
        None

    Raises:
        SystemExit: If no valid PDF file path is provided.
        Exception: Various exceptions may be raised during PDF processing.

    Note:
        The function uses a fixed Ollama configuration that could be modified for more flexibility.
        It currently uses the 'qwen2.5:14b' model from Ollama running on localhost:11434.
    """
    # checking arguments
    if not pdf_path or not os.path.exists(pdf_path):
        exit('no or faulty pdf file provided')
    if not output_path or not os.path.exists(output_path):
        output_path = os.getcwd()
        print('no or faulty output path provided, using cwd')
    # infer the rest of the needed filepaths
    pdf_name = os.path.basename(pdf_path)
    fname = os.path.splitext(pdf_name)[0]
    output_path = os.path.join(output_path, fname)
    os.makedirs(output_path, exist_ok=True)
    # set up a config, this could be altered for more flexibility
    ollama_config = {
        "output_format": "markdown",
        'use_llm': True,
        'llm_service': 'marker.services.ollama.OllamaService',
        'ollama_base_url': 'http://localhost:11434',
        'ollama_model': 'qwen2.5:14b'
    }
    config_parser = ConfigParser(ollama_config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service()
    )
    rendered = converter(pdf_path)
    save_output(rendered,
                output_path,
                fname)
    print('finished')

def main():
    """
    Main function to handle command-line arguments and call parse_pdf.

    This function parses command-line arguments, validates input and output paths,
    and calls the parse_pdf function to convert the PDF to markdown. It provides
    appropriate error handling and status codes for command-line usage.

    Usage:
        python PdfToMarkdown.py --pdf path/to/pdf [--output path/to/output]

    Returns:
        int: 0 for successful execution, 1 for errors
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown using Marker')

    # Add required argument for PDF file path
    parser.add_argument('--pdf', type=str, required=True,
                        help='Path to the PDF file to be converted')

    # Add optional argument for output directory
    parser.add_argument('--output', type=str, default=None,
                        help='Path to the output directory (defaults to current working directory)')

    # Parse arguments
    args = parser.parse_args()

    # Validate PDF path
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found at '{args.pdf}'")
        return 1

    # Validate output path if provided
    if args.output and not os.path.exists(args.output):
        print(f"Warning: Output directory '{args.output}' does not exist. Attempting to create it.")
        try:
            os.makedirs(args.output)
        except Exception as e:
            print(f"Error creating output directory: {e}")
            return 1

    # Call the parse_pdf function
    try:
        parse_pdf(pdf_path=args.pdf, output_path=args.output)
        return 0
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
