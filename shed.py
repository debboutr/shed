import click
import geopandas as gpd

from overlap import clip_overlaps_by_weight


@click.command()
@click.option("--tolerance", "-t", default=0.0000001, help="snap tolerance")
@click.option(
    "--output",
    "-o",
    default="clipped.gpkg",
    help="output filename, absolute or relative path",
)
@click.argument("input_file", nargs=1, type=click.Path(exists=True))
@click.argument("attr", nargs=1, type=click.Path())
def test(input_file, attr, output, tolerance):
    click.echo(f"{input_file=}  {output=}, {attr=}  {tolerance=}")
    click.echo(click.format_filename(input_file))
    gdf = gpd.read_file(input_file)
    if not attr in gdf.columns:
        click.echo(f"`{attr}` does not exist in the input file.")
        quit()

    out = clip_overlaps_by_weight(gdf, attr, tol=tolerance)
    out.to_file(output, driver="GPKG")


if __name__ == "__main__":

    test()
