import click
from src.gui.main import Main

# Python je sra*ka

KEY_MOCK = "mocked"

@click.group(invoke_without_command=True)
@click.option("--mocked", is_flag = True, default=False, help="Use testing data sources")
@click.pass_context
def app(ctx : click.Context, mocked: bool):
    if ctx.invoked_subcommand is None:
        # Start interactive
        Main().start_app()
    else:
        # Started command
        ctx.ensure_object(dict)
        ctx.obj[KEY_MOCK] = mocked

@click.command("list", help = "Shown menza list")
@click.pass_context
def list(ctx: click.Context):
    mocked : bool = ctx.obj[KEY_MOCK]
    pass

@click.command("dish", help = "Show menu for the menza given")
@click.argument("name")
@click.pass_context
def dish(ctx: click.Context, name: str):
    mocked : bool = ctx.obj[KEY_MOCK]
    click.echo("Param: " + name)
    pass

@click.command("info", help = "List info about menza given")
@click.argument("name")
@click.pass_context
def info(ctx: click.Context, name: str):
    mocked : bool = ctx.obj[KEY_MOCK]
    click.echo("Param: " + name)
    pass

app.add_command(list)
app.add_command(dish)
app.add_command(info)
