# PDF to Markdown Converter

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
   git clone [https://github.com/SoenkevL/PdftoMarkdown.git](https://github.com/SoenkevL/PdfToMarkdown.git)
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
   ollama pull qwen2.5:14b
   ```

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

To try the converter with the included sample PDF:

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
