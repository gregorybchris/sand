import logging
from typing import Optional

import click
from rich.logging import RichHandler

from sand.sand import Simulation, SimulationParams

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    pass


def set_logger_config(info: bool, debug: bool) -> None:
    handlers = [RichHandler(rich_tracebacks=True)]
    log_format = "%(message)s"

    if info:
        logging.basicConfig(level=logging.INFO, handlers=handlers, format=log_format)
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=handlers, format=log_format)


@main.command(name="simulate")
@click.option("--size", type=int, default=12)
@click.option("--steps", type=int, default=100)
@click.option("--seed", type=int, default=None)
@click.option("--stability-threshold", type=int, default=2)
@click.option("--drop-variance", type=float, default=0.1)
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def simulate_command(  # noqa: PLR0913
    size: int,
    steps: int,
    seed: Optional[int],
    stability_threshold: int,
    drop_variance: float,
    info: bool = False,
    debug: bool = False,
) -> None:
    set_logger_config(info=info, debug=debug)

    params = SimulationParams(
        size=size,
        steps=steps,
        seed=seed,
        stability_threshold=stability_threshold,
        drop_variance=drop_variance,
    )
    simulation = Simulation.new(params)
    simulation.simulate(steps)
