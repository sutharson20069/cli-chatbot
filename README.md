# Professional CLI Chatbot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

A sophisticated command-line chatbot designed for professional interview scenarios.

## Features

✅ **Professional Interface**: Clean, polished CLI with rich formatting
✅ **Interview Assistance**: Built-in knowledge base for interview questions
✅ **Natural Language Processing**: Sentiment analysis and keyword extraction
✅ **Conversation Management**: History tracking and context awareness
✅ **Extensible Architecture**: Modular design for easy customization
✅ **Configuration Support**: Environment variables and .env files
✅ **Error Handling**: Robust exception management
✅ **Security**: Input validation and sanitization

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Install from source

```bash
# Clone the repository
git clone https://github.com/sutharson20069/cli-chatbot.git
cd cli-chatbot

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install via pip (when published)

```bash
pip install cli-chatbot
```

## Usage

### Basic Usage

```bash
# Start the chatbot
chatbot
```

### Available Commands

- **General Chat**: Just type your message and press Enter
- **help**: Show help information
- **about**: Show information about the chatbot
- **clear**: Clear the conversation history
- **config**: Show current configuration
- **version**: Show version information
- **exit/quit/bye**: Exit the chatbot

### Example Session

```
🤖 Professional CLI Chatbot

Interview Assistant v1.0.0

A sophisticated command-line chatbot designed for professional interview scenarios.

*Type 'exit', 'quit', or 'bye' to end the session*
*Type 'help' for available commands*

You: hello
Chatbot: Hi there! What would you like to discuss?

You: I have a job interview tomorrow
Chatbot: Can you explain your experience with Python?

You: tell me about behavioral questions
Chatbot: Tell me about a time you worked in a team.

You: exit
👋 Thank you for using Professional CLI Chatbot. Goodbye!
```

## Configuration

### Environment Variables

Create a `.env` file by copying `.env.example`:

```bash
cp .env.example .env
```

Then edit the `.env` file to customize your settings.

### Available Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `CHATBOT_THEME` | `default` | UI theme |
| `CHATBOT_VERBOSE` | `false` | Verbose logging |
| `CHATBOT_MAX_HISTORY` | `10` | Maximum conversation history |
| `CHATBOT_LANGUAGE` | `english` | Language setting |
| `CHATBOT_DEBUG` | `false` | Debug mode |
| `CHATBOT_LOG_LEVEL` | `INFO` | Logging level |
| `CHATBOT_LOG_FILE` | `chatbot.log` | Log file path |

## Development

### Project Structure

```
cli-chatbot/
├── chatbot/                  # Main package
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── core.py               # Core chatbot logic
│   ├── config.py             # Configuration management
│   └── utils.py              # Utility functions
├── setup.py                  # Package setup
├── requirements.txt          # Dependencies
├── .env.example             # Example configuration
├── LICENSE                   # MIT License
└── README.md                 # Documentation
```

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy isort

# Run tests
pytest

# Run linting
black .
flake8 .
mypy .
isort .
```

### Building and Distribution

```bash
# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI (requires twine)
pip install twine
twine upload dist/*
```

## Architecture

### Core Components

1. **CLI Interface** (`cli.py`): Handles user interaction and display
2. **Core Logic** (`core.py`): Contains chatbot intelligence and conversation management
3. **Configuration** (`config.py`): Manages settings and environment variables
4. **Utilities** (`utils.py`): Helper functions for common tasks

### Design Patterns

- **MVC-like Architecture**: Separation of interface, logic, and data
- **Singleton Pattern**: Configuration management
- **Factory Pattern**: Response generation
- **Observer Pattern**: Event handling (future extension)

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions
- Include tests for new features
- Keep functions small and focused

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [x] Basic CLI interface
- [x] Core chatbot logic
- [x] Configuration management
- [x] Interview question knowledge base
- [ ] Advanced NLP integration
- [ ] Plugin system for extensibility
- [ ] Multi-language support
- [ ] Conversation persistence
- [ ] API integration for external services

## Author

**Sutharson** - [GitHub](https://github.com/sutharson20069) - sutharson20069@gmail.com

## Acknowledgments

- Thanks to all contributors and users
- Inspired by professional interview preparation tools
- Built with Python and modern CLI libraries