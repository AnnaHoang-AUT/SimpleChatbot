"""CLI interface for SimpleChatbot."""

import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from simplechatbot.chatbot import SimpleChatbot
from simplechatbot.config import AVAILABLE_MODELS, ChatbotConfig


def print_welcome(console: Console, config: ChatbotConfig) -> None:
    welcome_text = Text()
    welcome_text.append("SimpleChatbot", style="bold bright_cyan")
    welcome_text.append(" - Powered by Amazon Bedrock\n\n", style="dim")
    welcome_text.append(f"Model: {config.model.display_name}\n", style="green")
    welcome_text.append(f"Region: {config.aws_region}\n", style="green")
    welcome_text.append("\nCommands:\n", style="bold")
    welcome_text.append("  /model <key>  ", style="cyan")
    welcome_text.append("- Switch model\n")
    welcome_text.append("  /models       ", style="cyan")
    welcome_text.append("- List available models\n")
    welcome_text.append("  /clear        ", style="cyan")
    welcome_text.append("- Clear conversation history\n")
    welcome_text.append("  /quit         ", style="cyan")
    welcome_text.append("- Exit the chatbot\n")
    console.print(Panel(welcome_text, title="Welcome", border_style="bright_cyan"))


def main() -> None:
    console = Console()
    config = ChatbotConfig()
    print_welcome(console, config)

    try:
        chatbot = SimpleChatbot(config)
    except RuntimeError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        console.print("[dim]Ensure your AWS credentials are configured: aws configure[/dim]")
        sys.exit(1)

    console.print()

    while True:
        try:
            user_input = console.input("[bold bright_cyan]You:[/bold bright_cyan] ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
                console.print("\n[dim]Goodbye![/dim]")
                break
            if user_input.lower() == "/clear":
                chatbot.clear_history()
                console.print("[dim]Conversation history cleared.[/dim]\n")
                continue
            if user_input.lower() == "/models":
                for key, model in AVAILABLE_MODELS.items():
                    indicator = " <-- current" if key == config.model_key else ""
                    console.print(f"  [cyan]{key:12s}[/cyan] {model.display_name}{indicator}")
                console.print()
                continue
            if user_input.lower().startswith("/model "):
                model_key = user_input[7:].strip()
                try:
                    chatbot.set_model(model_key)
                    console.print(f"[green]Model switched to: {chatbot.current_model_name}[/green]\n")
                except ValueError as e:
                    console.print(f"[red]{e}[/red]\n")
                continue

            with console.status("[dim]Thinking...[/dim]", spinner="dots"):
                response = chatbot.get_response(user_input)
            console.print()
            console.print(Panel(Markdown(response), title=f"[bold]{chatbot.current_model_name}[/bold]", border_style="bright_green", padding=(1, 2)))
            console.print()

        except RuntimeError as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}\n")
        except KeyboardInterrupt:
            console.print("\n\n[dim]Goodbye![/dim]")
            break


if __name__ == "__main__":
    main()
