#!/usr/bin/env python
"""
PDF to Markdown Converter - Web Interface

This module provides a Flask-based web interface for the PDF to Markdown converter.
It allows users to upload PDF files, configure conversion parameters, and download
the resulting markdown files through a browser interface.

Dependencies:
    - flask: Web framework
    - flask-dropzone: File upload handling
    - flask-wtf: Form handling and validation
    - werkzeug: File handling utilities

Run with:
    python app.py
"""

import os
import json
import uuid
import datetime
from typing import Dict, List, Optional, Any
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_dropzone import Dropzone
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from wtforms import StringField, SelectField
from PdfToMarkdownConverter import PdfToMarkdownConverter

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'development-key-change-in-production')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
    ALLOWED_EXTENSIONS = {'pdf'}
    DROPZONE_MAX_FILE_SIZE = 20  # MB
    DROPZONE_TIMEOUT = 300000  # 5 minutes in milliseconds
    DROPZONE_DEFAULT_MESSAGE = "Drag and drop a PDF file here or click to upload"
    CONVERSION_HISTORY_FILE = os.path.join(os.getcwd(), 'conversion_history.json')
    MAX_RECENT_CONVERSIONS = 10
    LLM_MODELS = [
        ('qwen2.5:14b', 'Qwen 2.5 (14B)'),
        ('qwen2.5:7b', 'Qwen 2.5 (7B)'),
        ('llama3:8b', 'Llama 3 (8B)'),
        ('mistral:7b', 'Mistral (7B)')
    ]
    OUTPUT_FORMATS = [
        ('markdown', 'Markdown'),
        ('html', 'HTML')
    ]

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
csrf = CSRFProtect(app)
dropzone = Dropzone(app)

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Form for PDF conversion
class ConversionForm(FlaskForm):
    output_dir = StringField('Output Directory')
    llm_model = SelectField('LLM Model', choices=Config.LLM_MODELS)
    ollama_base_url = StringField('Ollama Base URL', default='http://localhost:11434')
    output_format = SelectField('Output Format', choices=Config.OUTPUT_FORMATS)

# Conversion history management
class ConversionHistory:
    @staticmethod
    def load() -> List[Dict[str, Any]]:
        """Load conversion history from JSON file."""
        if os.path.exists(Config.CONVERSION_HISTORY_FILE):
            try:
                with open(Config.CONVERSION_HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def save(history: List[Dict[str, Any]]) -> None:
        """Save conversion history to JSON file."""
        with open(Config.CONVERSION_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)

    @staticmethod
    def add_conversion(pdf_path: str, output_path: str) -> str:
        """Add a new conversion to history and return its ID."""
        history = ConversionHistory.load()

        # Generate a unique ID
        conversion_id = str(uuid.uuid4())

        # Create new conversion record
        new_conversion = {
            'id': conversion_id,
            'filename': os.path.basename(pdf_path),
            'pdf_path': pdf_path,
            'output_path': output_path,
            'timestamp': datetime.datetime.now().isoformat(),
            'has_preview': True
        }

        # Add to history and keep only recent conversions
        history.insert(0, new_conversion)
        history = history[:Config.MAX_RECENT_CONVERSIONS]

        # Save updated history
        ConversionHistory.save(history)

        return conversion_id

    @staticmethod
    def get_recent_conversions() -> List[Dict[str, Any]]:
        """Get list of recent conversions."""
        history = ConversionHistory.load()
        return history

    @staticmethod
    def get_conversion(conversion_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific conversion by ID."""
        history = ConversionHistory.load()
        for conversion in history:
            if conversion['id'] == conversion_id:
                return conversion
        return None

# Utility functions
def allowed_file(filename: str) -> bool:
    """Check if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Template filters
@app.template_filter('now')
def _jinja2_filter_now(format_string: str) -> str:
    """Return formatted datetime for templates."""
    if format_string == 'year':
        return datetime.datetime.now().strftime('%Y')
    return datetime.datetime.now().strftime(format_string)

# Routes
@app.route('/')
def index():
    """Render the main page."""
    form = ConversionForm()
    recent_conversions = ConversionHistory.get_recent_conversions()
    return render_template('index.html', form=form, recent_conversions=recent_conversions, dropzone=dropzone)

@app.route('/convert', methods=['POST'])
def convert_pdf():
    """Handle PDF file upload and conversion."""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        # Get form data for configuration
        form = ConversionForm()
        if form.validate_on_submit():
            output_dir = form.output_dir.data or app.config['OUTPUT_FOLDER']

            # Create custom configuration
            config = {
                "output_format": form.output_format.data,
                "use_llm": True,
                "llm_service": "marker.services.ollama.OllamaService",
                "ollama_base_url": form.ollama_base_url.data,
                "ollama_model": form.llm_model.data
            }

            # Save temporary config file
            config_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.json")
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)

            try:
                # Perform conversion
                converter = PdfToMarkdownConverter(config_path=config_path)
                output_path = converter.convert_pdf(pdf_path=pdf_path, output_path=output_dir)

                # Add to conversion history
                conversion_id = ConversionHistory.add_conversion(pdf_path, output_path)

                # Clean up temporary config file
                if os.path.exists(config_path):
                    os.remove(config_path)

                flash('PDF converted successfully!', 'success')
                return redirect(url_for('index', success='PDF converted successfully!'))

            except Exception as e:
                flash(f'Error during conversion: {str(e)}', 'error')
                return redirect(url_for('index', error=f'Error: {str(e)}'))
        else:
            # Flash form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'error')
            return redirect(url_for('index'))

    flash('Invalid file type. Please upload a PDF file.', 'error')
    return redirect(url_for('index'))

@app.route('/preview/<conversion_id>')
def preview(conversion_id):
    """Preview a converted markdown file."""
    conversion = ConversionHistory.get_conversion(conversion_id)
    if not conversion:
        flash('Conversion not found', 'error')
        return redirect(url_for('index'))

    # Get the markdown file path
    filename = os.path.splitext(conversion['filename'])[0]
    markdown_path = os.path.join(conversion['output_path'], f"{filename}.md")

    if not os.path.exists(markdown_path):
        flash('Markdown file not found', 'error')
        return redirect(url_for('index'))

    # Read markdown content
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML for preview
        import markdown
        html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])

        return render_template('preview.html', 
                               markdown_content=html_content, 
                               filename=conversion['filename'],
                               conversion_id=conversion_id)
    except Exception as e:
        flash(f'Error loading preview: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<conversion_id>/<file_type>')
def download_file(conversion_id, file_type):
    """Download a converted file."""
    conversion = ConversionHistory.get_conversion(conversion_id)
    if not conversion:
        flash('Conversion not found', 'error')
        return redirect(url_for('index'))

    filename = os.path.splitext(conversion['filename'])[0]

    if file_type == 'md':
        file_path = os.path.join(conversion['output_path'], f"{filename}.md")
        download_name = f"{filename}.md"
    else:
        flash('Invalid file type', 'error')
        return redirect(url_for('index'))

    if not os.path.exists(file_path):
        flash('File not found', 'error')
        return redirect(url_for('index'))

    return send_from_directory(directory=os.path.dirname(file_path),
                               path=os.path.basename(file_path),
                               download_name=download_name,
                               as_attachment=True)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
