# PDF to Markdown Converter
# PDF to Markdown Converter with Web Interface
# PDF to Markdown Converter

A Python application that converts PDF documents to Markdown format using the Marker library and Ollama's LLM capabilities.

## Features

- Convert PDF documents to clean, formatted Markdown
- Web interface for easy upload and configuration
- Command-line interface for batch processing
- LLM-powered content extraction and formatting
- Support for custom configuration

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pdf-to-markdown-converter.git
   cd pdf-to-markdown-converter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have Ollama running locally or specify a remote Ollama server in the configuration.

## Usage

### Web Interface

1. Start the web server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to http://localhost:5000

3. Upload a PDF file, configure options if needed, and click "Convert PDF to Markdown"

4. Download the converted Markdown file or preview it in the browser

### Command Line Interface

```bash
# Basic usage
python PdfToMarkdownConverter.py --pdf path/to/document.pdf

# Specify output directory
python PdfToMarkdownConverter.py --pdf path/to/document.pdf --output path/to/output_dir

# Use custom configuration
python PdfToMarkdownConverter.py --pdf path/to/document.pdf --config path/to/config.json

# Create a default configuration file
python PdfToMarkdownConverter.py --create-config config.json
```

## Configuration

The converter can be configured using a JSON file with the following options:

```json
{
  "output_format": "markdown",
  "use_llm": true,
  "llm_service": "marker.services.ollama.OllamaService",
  "ollama_base_url": "http://localhost:11434",
  "ollama_model": "qwen2.5:14b"
}
```

## Requirements

- Python 3.7+
- Flask 2.2+
- Marker library
- Ollama (running locally or remotely)
- See requirements.txt for complete list

## License

[MIT License](LICENSE)
This application provides a simple web interface for converting PDF documents to Markdown format using the Marker library. It leverages Ollama's LLM capabilities for enhanced conversion quality.

## Features

- Easy-to-use web interface for uploading and converting PDF files
- Configuration management through the web UI
- Real-time conversion status updates
- View and download converted files
- Dark mode support for markdown preview
- Drag-and-drop file upload

## Prerequisites

- Python 3.13+ 
- Marker library
- Flask
- Ollama (running locally or on a specified endpoint)

## Installation

1. Clone this repository
2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running and accessible (default: http://localhost:11434)

## Usage

1. Start the web server:

```bash
python app.py
```

2. Open your browser and navigate to http://localhost:5000
3. Upload a PDF file using the web interface
4. Configure conversion settings if needed
5. View and download the converted markdown files

## Configuration

You can customize the conversion process by modifying the configuration through the web interface or by directly editing the `config.json` file.

Available configuration options:

- `output_format`: Format of the output (currently only markdown is supported)
- `use_llm`: Whether to use LLM for enhanced conversion
- `llm_service`: Service to use for LLM (default: Ollama)
- `ollama_base_url`: URL of the Ollama service
- `ollama_model`: Ollama model to use for conversion

## Project Structure

- `app.py`: Main Flask application
- `PdfToMarkdownConverter.py`: Core conversion functionality
- `templates/`: HTML templates for the web interface
- `uploads/`: Temporary storage for uploaded PDF files
- `output/`: Directory for converted markdown files
- `config.json`: Configuration file

## License

This project is licensed under the MIT License - see the LICENSE file for details.
A powerful tool that converts PDF documents to well-formatted Markdown using the Marker library and Ollama's LLM capabilities. This tool extracts structured content from PDFs, including text, tables, and images, and generates high-quality markdown documents.

## Features

- Converts PDF documents to clean, structured Markdown
- Preserves document structure including headings, lists, and tables
- Extracts and saves images from the PDF
- Creates a well-organized output folder structure
- Uses Ollama's LLM capabilities for enhanced text extraction and formatting
- Generates metadata for the converted document

## Requirements

- Python 3.8+
- [Marker](https://github.com/VikParuchuri/marker) library
- [Ollama](https://ollama.ai/) for LLM capabilities
- NVIDIA GPU with at least 16GB VRAM (for running the Qwen2.5 model)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/SoenkevL/PdfToMarkdown.git
   cd PdfToMarkdown
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install marker-pdf ollama
   ```

## Setting Up Ollama

Ollama is required to run the LLM that enhances the PDF conversion process. Follow these steps to set it up:

1. Install Ollama by following the instructions at [ollama.ai](https://ollama.ai/download)

2. Start the Ollama service:
   ```bash
   ollama serve
   ```

3. Pull the Qwen2.5 model (requires at least 16GB VRAM):
   ```bash
   ollama run qwen2.5:14b
   ```
   The first time this is run, the model needs to be pulled which may take some time

   Note: If you have less VRAM, you can use a smaller model by modifying the `ollama_model` parameter in the `PdfToMarkdown.py` file. For example:
   ```python
   ollama_config = {
       "output_format": "markdown",
       'use_llm': True,
       'llm_service': 'marker.services.ollama.OllamaService',
       'ollama_base_url': 'http://localhost:11434',
       'ollama_model': 'llama3:8b'  # Use a smaller model
   }
   ```

## Usage

### Basic Usage

Convert a PDF file to Markdown:

```bash
python PdfToMarkdown.py --pdf path/to/your/document.pdf
```

This will create a new folder named after your PDF file in the current directory, containing:
- A markdown file with the converted content
- Extracted images from the PDF
- A meta.json file with document metadata

### Specifying Output Directory

You can specify a custom output directory:

```bash
python PdfToMarkdown.py --pdf path/to/your/document.pdf --output path/to/output/directory
```

### Example with Sample PDF

To try the converter with the included sample PDF (my Master Thesis):

```bash
# Make sure Ollama is running in another terminal with: ollama serve
python PdfToMarkdown.py --pdf Thesis.pdf
```

This will create a `Thesis` folder containing the converted markdown file, extracted images, and metadata.

## How It Works

1. The script takes a PDF file as input
2. It uses the Marker library to process the PDF and extract its content
3. Ollama's LLM capabilities are used to enhance the extraction and formatting
4. The converted content is saved as a markdown file
5. Images are extracted and saved separately
6. Metadata about the document is generated and saved as JSON

## Troubleshooting

- **Ollama Connection Error**: Make sure the Ollama service is running with `ollama serve`
- **Out of Memory Error**: If you encounter CUDA out of memory errors, try using a smaller model
- **Missing Dependencies**: Ensure all required packages are installed
- **PDF Not Found**: Verify the path to your PDF file is correct

## License

[MIT License](LICENSE)

## Acknowledgements

- [Marker](https://github.com/VikParuchuri/marker) for the PDF conversion library
- [Ollama](https://ollama.ai/) for the local LLM capabilities
