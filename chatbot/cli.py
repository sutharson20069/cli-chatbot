"""
Command-line interface for the professional chatbot.

This module provides the main CLI entry point and handles user interaction
through a sophisticated command-line interface.
"""

import click
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from .core import ChatbotCore
from .config import load_config


class ChatbotCLI:
    """Main CLI class for the professional chatbot."""
    
    def __init__(self):
        self.console = Console()
        self.core = ChatbotCore()
        self.config = load_config()
        
    def display_welcome(self):
        """Display the professional welcome message."""
        welcome_md = """
# 🤖 Professional CLI Chatbot

**Interview Assistant v1.0.0**

A sophisticated command-line chatbot designed for professional interview scenarios.

*Type 'exit', 'quit', or 'bye' to end the session*
*Type 'help' for available commands*
        """
        self.console.print(Panel(Markdown(welcome_md), border_style="blue"))
    
    def display_help(self):
        """Display help information."""
        help_text = """
📚 **Available Commands:**

• **General Chat**: Just type your message and press Enter
• **help**: Show this help message
• **about**: Show information about the chatbot
• **clear**: Clear the conversation history
• **exit/quit/bye**: Exit the chatbot
• **config**: Show current configuration
• **version**: Show version information
        """
        self.console.print(Panel(Markdown(help_text), title="Help", border_style="green"))
    
    def display_about(self):
        """Display about information."""
        about_text = """
🤖 **Professional CLI Chatbot**

**Version**: 1.0.0
**Author**: Sutharson
**Email**: sutharsonmohan@gmail.com

A professional-grade CLI chatbot designed for interview scenarios.
Features natural language processing and sophisticated conversation management.
        """
        self.console.print(Panel(Markdown(about_text), title="About", border_style="cyan"))
    
    def display_config(self):
        """Display current configuration."""
        config_info = f"""
📋 **Current Configuration**

**Theme**: {self.config.get('theme', 'default')}
**Verbose**: {self.config.get('verbose', False)}
**Max History**: {self.config.get('max_history', 10)}
**Language**: {self.config.get('language', 'english')}
        """
        self.console.print(Panel(Markdown(config_info), title="Configuration", border_style="magenta"))
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.core.clear_history()
        self.console.print("[green]✓ Conversation history cleared[/green]")
    
    def run(self):
        """Main CLI loop."""
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]", prompt_suffix=" ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.console.print("[bold yellow]👋 Thank you for using Professional CLI Chatbot. Goodbye![/bold yellow]")
                    break
                elif user_input.lower() == 'help':
                    self.display_help()
                elif user_input.lower() == 'about':
                    self.display_about()
                elif user_input.lower() == 'clear':
                    self.clear_conversation()
                elif user_input.lower() == 'config':
                    self.display_config()
                elif user_input.lower() == 'version':
                    from . import __version__
                    self.console.print(f"[bold blue]Version: {__version__}[/bold blue]")
                else:
                    # Process normal chat input
                    response = self.core.process_input(user_input)
                    self.console.print(f"[bold green]Chatbot[/bold green]: {response}")
                    
            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]👋 Thank you for using Professional CLI Chatbot. Goodbye![/bold yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]❌ Error: {str(e)}[/bold red]")
                continue


def main():
    """Entry point for the CLI chatbot."""
    try:
        cli = ChatbotCLI()
        cli.run()
    except Exception as e:
        console = Console()
        console.print(f"[bold red]❌ Fatal Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()