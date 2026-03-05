# This module focuses on command line styling. 

from rich import print
from rich.console import Console
from rich.table import Table
from models.transaction import Transaction
from services.api import get_current_price

console = Console()

# prints an error message in bold red
def print_error(error_message: str):
    if not error_message.strip():
        raise ValueError("error message cannot be an empty string")
    console.print(f"[bold red]{error_message}[/bold red]")

# prints a success message in bold green
def print_success(success_message: str):
    if not success_message.strip():
        raise ValueError("success message cannot be an empty string")
    console.print(f"[bold green]{success_message}[/bold green]")

# prints a warning message in yellow
def print_warning(warning_message: str):
    if not warning_message.strip():
        raise ValueError("warning message cannot be an empty string")
    console.print(f"[yellow]{warning_message}[/yellow]")

# prints a header in italic bold cyan
def print_header(header_message: str):
    if not header_message.strip():
        raise ValueError("header message cannot be an empty string")
    console.print(f"[italic bold cyan]{header_message}[/italic bold cyan]")

# prints transaction history in a formatted table using Rich
def print_transaction_table(transactions: dict):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=20)
    table.add_column("Type")
    table.add_column("Asset")
    table.add_column("Quantity")
    table.add_column("Purchase Price")
    table.add_column("Date")


    for id, transaction in transactions.items():
        type_color = "green" if transaction.transaction_type == "BUY" else "red"
        table.add_row(
            f"{id}",
            f"[{type_color}]{transaction.transaction_type}[/{type_color}]",
            f"{transaction.coin_id}",
            f"{transaction.quantity}",
            f"{transaction.purchase_price}",
            transaction.timestamp
        )
    
    console.print(table)

# prints asset history in a formatted table using Rich
def print_asset_table(assets: dict, currency_type: str):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Asset")
    table.add_column("Quantity")
    table.add_column("Purchase Price")
    table.add_column("Unrealized Profit")
    table.add_column("Currency")

    for asset_id, asset in assets.items():
        current_asset_price = get_current_price(asset_id, currency_type)
        asset_unrealized_profit = asset.unrealized_profit(current_asset_price)
        profit_color = "green" if asset_unrealized_profit >= 0 else "red"
        table.add_row(
            f"{asset_id}",
            f"{asset.quantity:,}",
            f"{asset.purchase_price}",
            f"[{profit_color}]{asset_unrealized_profit:+,.2f}[/{profit_color}]",
            currency_type
        )

    console.print(table)

# prints the portfolio menu in a formatted table using Rich
def print_menu_table():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option")
    table.add_column("Action")

    table.add_row(
        "1",
        "Buy"
    )
    
    table.add_row(
        "2",
        "Sell"
    )

    table.add_row(
        "3",
        "Display Assets"
    )

    table.add_row(
        "4",
        "Display Transactions"
    )

    table.add_row(
        "5",
        "Display Portfolio Value"
    )

    table.add_row(
        "6",
        "Exit"
    )

    console.print(table)


# returns a formatted profit string in green (if in profit) or red (if in loss)
def format_profit(profit: float):
    if not isinstance(profit, (float, int)):
        raise ValueError("profit must be a valid numeric type")
    color = "green" if profit >= 0 else "red"
    return f"[{color}]{profit:+,.2f}[/{color}]"
