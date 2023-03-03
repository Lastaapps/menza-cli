"""Handles cli args"""

import click

from menza_cli import di
from menza_cli.cli.dish import command_dish
from menza_cli.cli.info import command_info
from menza_cli.cli.list import command_list
from menza_cli.cli.week import command_week

# Used in context passing
KEY_MOCK = "mocked"


@click.group(invoke_without_command=True)
@click.option("--mocked", is_flag=True, default=False, help="Use testing data sources")
@click.pass_context
def app(ctx: click.Context, mocked: bool):
    """Default, launches gui"""

    if ctx.invoked_subcommand is None:
        # Start interactive
        di.get_main_gui(mocked).start_app()
    else:
        # Started command
        ctx.ensure_object(dict)
        ctx.obj[KEY_MOCK] = mocked


@click.command("list", help="Shown menza list")
@click.pass_context
def list_wtf_is_this_built_in(ctx: click.Context):
    """Handles the list command"""

    mocked: bool = ctx.obj[KEY_MOCK]
    command_list(mocked)


@click.command("dish", help="Show menu for the menza given")
@click.argument("name")
@click.pass_context
def dish(ctx: click.Context, name: str):
    """Handles the dish command"""

    mocked: bool = ctx.obj[KEY_MOCK]
    command_dish(mocked, name)


@click.command("week", help="Show week menu for the menza given")
@click.argument("name")
@click.pass_context
def week(ctx: click.Context, name: str):
    """Handles the week command"""

    mocked: bool = ctx.obj[KEY_MOCK]
    command_week(mocked, name)


@click.command("info", help="List info about menza given")
@click.argument("name")
@click.pass_context
def info(ctx: click.Context, name: str):
    """Handles the info command"""

    mocked: bool = ctx.obj[KEY_MOCK]
    command_info(mocked, name)


app.add_command(list_wtf_is_this_built_in)
app.add_command(dish)
app.add_command(week)
app.add_command(info)
