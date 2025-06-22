
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
    - json: For configuration file parsing

Example usage:
    python PdfToMarkdown.py --pdf path/to/document.pdf --output path/to/output_dir --config config.json
"""

from marker.converters.pdf import PdfConverter
import argparse
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import text_from_rendered, save_output
import os
import json
from typing import Optional, Dict, Any


class PdfToMarkdownConverter:
    """
    A class for converting PDF files to Markdown format using the Marker library.
    
    This class handles the configuration, setup, and execution of PDF to Markdown conversion
    with support for external JSON configuration files and Ollama LLM integration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PDF to Markdown converter.
        
        Args:
            config_path (Optional[str]): Path to the JSON configuration file.
                                       If None, uses default configuration.
        """
        self.config = self._load_config(config_path)
        self.converter = None
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from JSON file or use default configuration.
        
        Args:
            config_path (Optional[str]): Path to the JSON configuration file.
            
        Returns:
            Dict[str, Any]: Configuration dictionary.
            
        Raises:
            FileNotFoundError: If config file path is provided but file doesn't exist.
            json.JSONDecodeError: If config file contains invalid JSON.
        """
        default_config = {
            "output_format": "markdown",
            "use_llm": True,
            "llm_service": "marker.services.ollama.OllamaService",
            "ollama_base_url": "http://localhost:11434",
            "ollama_model": "qwen2.5:14b"
        }
        
        if config_path is None:
            print("No config file provided, using default configuration")
            return default_config
            
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                
            # Merge with defaults to ensure all required keys are present
            merged_config = default_config.copy()
            merged_config.update(loaded_config)
            
            print(f"Configuration loaded from: {config_path}")
            return merged_config
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in config file {config_path}: {e}")
    
    def _setup_converter(self):
        """
        Set up the PDF converter with the loaded configuration.
        """
        config_parser = ConfigParser(self.config)
        
        self.converter = PdfConverter(
            config=config_parser.generate_config_dict(),
            artifact_dict=create_model_dict(),
            processor_list=config_parser.get_processors(),
            renderer=config_parser.get_renderer(),
            llm_service=config_parser.get_llm_service()
        )
    
    def convert_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert a PDF file to Markdown format and save the results.
        
        Args:
            pdf_path (str): Path to the PDF file to process.
            output_path (Optional[str]): Directory where the output folder will be created.
                                       If None, uses current working directory.
        
        Returns:
            str: Path to the output directory containing the converted files.
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist.
            Exception: Various exceptions during PDF processing.
        """
        # Validate PDF path
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Set output path
        if output_path is None or not os.path.exists(output_path):
            if output_path is not None:
                print(f"Output path '{output_path}' doesn't exist, using current directory")
            output_path = os.getcwd()
        
        # Prepare output directory
        pdf_name = os.path.basename(pdf_path)
        fname = os.path.splitext(pdf_name)[0]
        final_output_path = os.path.join(output_path, fname)
        os.makedirs(final_output_path, exist_ok=True)
        
        # Setup converter if not already done
        if self.converter is None:
            self._setup_converter()
        
        # Convert PDF
        print(f"Converting PDF: {pdf_path}")
        print(f"Output directory: {final_output_path}")
        
        rendered = self.converter(pdf_path)
        save_output(rendered, final_output_path, fname)
        
        print("Conversion completed successfully!")
        return final_output_path
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration.
        
        Returns:
            Dict[str, Any]: Current configuration dictionary.
        """
        return self.config.copy()


def create_default_config(config_path: str = "config.json"):
    """
    Create a default configuration file.
    
    Args:
        config_path (str): Path where to save the configuration file.
    """
    default_config = {
        "output_format": "markdown",
        "use_llm": True,
        "llm_service": "marker.services.ollama.OllamaService",
        "ollama_base_url": "http://localhost:11434",
        "ollama_model": "qwen2.5:14b"
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4)
    
    print(f"Default configuration created at: {config_path}")


def main():
    """
    Main function to handle command-line arguments and execute PDF conversion.
    
    Returns:
        int: 0 for successful execution, 1 for errors.
    """
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown using Marker')
    
    parser.add_argument('--pdf', type=str, required=True,
                       help='Path to the PDF file to be converted')
    
    parser.add_argument('--output', type=str, default=None,
                       help='Path to the output directory (defaults to current working directory)')
    
    parser.add_argument('--config', type=str, default=None,
                       help='Path to the JSON configuration file')
    
    parser.add_argument('--create-config', type=str, default=None,
                       help='Create a default configuration file at the specified path')
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        try:
            create_default_config(args.create_config)
            return 0
        except Exception as e:
            print(f"Error creating configuration file: {e}")
            return 1
    
    # Validate PDF path
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found at '{args.pdf}'")
        return 1
    
    # Create output directory if specified and doesn't exist
    if args.output and not os.path.exists(args.output):
        print(f"Creating output directory: {args.output}")
        try:
            os.makedirs(args.output, exist_ok=True)
        except Exception as e:
            print(f"Error creating output directory: {e}")
            return 1
    
    # Convert PDF
    try:
        converter = PdfToMarkdownConverter(config_path=args.config)
        output_dir = converter.convert_pdf(pdf_path=args.pdf, output_path=args.output)
        print(f"Files saved to: {output_dir}")
        return 0
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
        return 1


if __name__ == "__main__":
    exit(main())