import logging
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterator, Self

import cv2
import numpy as np
from gunwale.lib.bounding_box import BoundingBox

logger = logging.getLogger(__name__)


@dataclass
class VideoReader:
    """Video reader."""

    filepath: Path
    video_capture: cv2.VideoCapture

    @classmethod
    @contextmanager
    def context(cls, filepath: Path) -> Generator[Self, None, None]:
        """Create a new VideoReader context.

        Args:
            filepath (Path): Path to the video file.

        Yields:
            VideoReader: Video reader instance.
        """
        filepath_str = str(filepath)
        video_capture = cv2.VideoCapture(filepath_str)
        yield cls(filepath=filepath, video_capture=video_capture)
        video_capture.release()

    def iter_frames(self) -> Iterator[np.ndarray]:
        """Iterate over frames in a video.

        Yields:
            np.ndarray: A frame in the video.
        """
        if not self.video_capture.isOpened():
            msg = "Error opening video file"
            raise OSError(msg)

        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break
            yield frame

    def set_frame(self, frame_index: int) -> None:
        """Set the video reader to a specific frame."""
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    @property
    def fps(self) -> float:
        """Get the frames per second of the video.

        Returns:
            float: Frames per second of the video.
        """
        return self.video_capture.get(cv2.CAP_PROP_FPS)

    @property
    def width(self) -> int:
        """Get the width of the video.

        Returns:
            int: Width of the video.
        """
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        """Get the height of the video.

        Returns:
            int: Height of the video.
        """
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def n_frames(self) -> int:
        """Get the number of frames in the video.

        Returns:
            int: Number of frames in the video.
        """
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))


@dataclass
class VideoWriter:
    """Video writer."""

    filepath: Path
    video_writer: cv2.VideoWriter

    @classmethod
    @contextmanager
    def context(cls, filepath: Path, fps: float, width: int, height: int) -> Generator[Self, None, None]:
        """Create a new VideoWriter context.

        Args:
            filepath (Path): Path to the video file.
            fps (float): Frames per second of the video.
            width (int): Width of the video.
            height (int): Height of the video.

        Yields:
            VideoWriter: Video writer instance.
        """
        filepath_str = str(filepath)
        fourcc = cv2.VideoWriter.fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(filepath_str, fourcc, fps, (width, height))
        yield cls(filepath=filepath, video_writer=video_writer)
        video_writer.release()

    def write(self, frame: np.ndarray) -> None:
        """Write a frame to the video."""
        self.video_writer.write(frame)


@dataclass
class Annotator:
    """Video frame annotator."""

    @classmethod
    def draw_bounding_box(  # noqa: PLR0913
        cls,
        frame: np.ndarray,
        bounding_box: BoundingBox,
        text: str = "",
        box_color: tuple[int, int, int] = (255, 0, 0),
        box_thickness: int = 2,
        text_color: tuple[int, int, int] = (255, 0, 0),
        text_font_scale: float = 0.5,
        text_thickness: int = 2,
    ) -> None:
        """Draw bounding box on frame.

        Args:
            frame (np.ndarray): Frame to draw bounding box on.
            bounding_box (BoundingBox): Bounding box to draw.
            text (str): Text to draw.
            box_color (tuple[int, int, int]): Bounding box color.
            box_thickness (int): Bounding box thickness.
            text_color (tuple[int, int, int]): Text color.
            text_font_scale (float): Text font scale.
            text_thickness (int): Text thickness.
        """
        x1, y1, x2, y2 = bounding_box.to_tuple()
        box_color_bgr = box_color[::-1]
        text_color_bgr = text_color[::-1]
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color_bgr, thickness=box_thickness)
        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_font_scale,
            text_color_bgr,
            thickness=text_thickness,
        )


@dataclass
class ColorConversion:
    """Color conversion utilities."""

    @classmethod
    def rgb_to_bgr(cls, frame: np.ndarray) -> np.ndarray:
        """Convert RGB frame to BGR frame.

        Args:
            frame (np.ndarray): RGB frame.

        Returns:
            np.ndarray: BGR frame.
        """
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    @classmethod
    def bgr_to_rgb(cls, frame: np.ndarray) -> np.ndarray:
        """Convert BGR frame to RGB frame.

        Args:
            frame (np.ndarray): BGR frame.

        Returns:
            np.ndarray: RGB frame.
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
