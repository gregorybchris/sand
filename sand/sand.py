import logging
import queue
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Optional

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Pile:
    data: np.ndarray
    stability_threshold: int
    rng: np.random.Generator

    @classmethod
    def new(cls, rows: int, cols: int, stability_threshold: int, rng: np.random.Generator) -> "Pile":
        data = np.zeros((rows, cols), dtype=int)
        return cls(data, stability_threshold, rng)

    @property
    def rows(self) -> int:
        return self.data.shape[0]

    @property
    def cols(self) -> int:
        return self.data.shape[1]

    def drop(self, *, variance: float) -> int:
        x_rand = self.rng.normal(0.0, variance)
        y_rand = self.rng.normal(0.0, variance)
        x = int(x_rand * self.rows + self.rows / 2)
        y = int(y_rand * self.cols + self.cols / 2)
        if self.in_bounds(x, y):
            self.inc(x, y)
            return self.cascade(x, y)
        logger.debug("Dropped outside of the pile")
        return 0

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols

    def set(self, x: int, y: int, value: int) -> None:
        if self.in_bounds(x, y):
            self.data[x, y] = value

    def get(self, x: int, y: int) -> int:
        if self.in_bounds(x, y):
            return self.data[x, y]
        return 0

    def inc(self, x: int, y: int) -> None:
        self.set(x, y, self.get(x, y) + 1)

    def dec(self, x: int, y: int) -> None:
        self.set(x, y, self.get(x, y) - 1)

    def iter_neighbors(
        self,
        x: int,
        y: int,
        diag: bool = False,
        in_bounds: bool = False,
    ) -> Iterator[tuple[int, int]]:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if not diag and (dx != 0 and dy != 0):
                    continue
                nx, ny = x + dx, y + dy
                if in_bounds and not self.in_bounds(nx, ny):
                    continue
                yield nx, ny

    def cascade(self, x: int, y: int) -> int:
        falls = 0

        q: queue.Queue[tuple[int, int]] = queue.Queue()
        q.put((x, y))
        while not q.empty():
            x, y = q.get()

            if self.get(x, y) < self.stability_threshold:
                continue

            h = self.get(x, y)
            for nx, ny in self.iter_neighbors(x, y):
                n = self.get(nx, ny)
                if h - n > self.stability_threshold:
                    self.dec(x, y)
                    self.inc(nx, ny)
                    q.put((nx, ny))
                    falls += 1
        return falls


@dataclass
class SimulationParams:
    size: int
    steps: int
    seed: Optional[int]
    stability_threshold: int
    drop_variance: float


@dataclass
class Simulation:
    params: SimulationParams

    @classmethod
    def new(cls, params: SimulationParams) -> "Simulation":
        return cls(params)

    def simulate(self, steps: int) -> None:
        logger.info("Starting simulation with parameters")
        logger.info("size=%d", self.params.size)
        logger.info("steps=%d", self.params.steps)
        logger.info("seed=%s", self.params.seed)
        logger.info("stability_threshold=%d", self.params.stability_threshold)
        logger.info("drop_variance=%f", self.params.drop_variance)

        rng = np.random.default_rng(self.params.seed)
        pile = Pile.new(
            self.params.size,
            self.params.size,
            self.params.stability_threshold,
            rng,
        )

        fall_histogram: defaultdict[int, int] = defaultdict(int)
        for _ in range(steps):
            falls = pile.drop(variance=self.params.drop_variance)
            fall_histogram[falls] += 1

        logger.info("Final pile data:\n%s", pile.data)

        logger.info("Falls histogram:")
        for falls, count in sorted(fall_histogram.items()):
            logger.info("%d: %d", falls, count)

        logger.info("Simulation done")
