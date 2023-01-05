import click
from src.cli.list import command_list
from src.cli.dish import command_dish
from src.cli.info import command_info
from src import di

# Python je sra*ka

KEY_MOCK = "mocked"

@click.group(invoke_without_command=True)
@click.option("--mocked", is_flag = True, default=False, help="Use testing data sources")
@click.pass_context
def app(ctx : click.Context, mocked: bool):
    if ctx.invoked_subcommand is None:
        # Start interactive
        di.get_main_gui(mocked).start_app()
    else:
        # Started command
        ctx.ensure_object(dict)
        ctx.obj[KEY_MOCK] = mocked

@click.command("list", help = "Shown menza list")
@click.pass_context
def list(ctx: click.Context):
    mocked : bool = ctx.obj[KEY_MOCK]
    command_list(mocked)

@click.command("dish", help = "Show menu for the menza given")
@click.argument("name")
@click.pass_context
def dish(ctx: click.Context, name: str):
    mocked : bool = ctx.obj[KEY_MOCK]
    command_dish(mocked, name)

@click.command("info", help = "List info about menza given")
@click.argument("name")
@click.pass_context
def info(ctx: click.Context, name: str):
    mocked : bool = ctx.obj[KEY_MOCK]
    command_info(mocked, name)
    

app.add_command(list)
app.add_command(dish)
app.add_command(info)
