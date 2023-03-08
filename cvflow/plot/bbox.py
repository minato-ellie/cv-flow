from typing import List, Tuple, Optional, Literal

import numpy as np
import cv2

from cvflow.utils.color import generate_farthest_colors


def draw_bbox(
        image: np.ndarray,
        bbox: np.ndarray,
        color: Tuple[int, int, int],
        *,
        thickness: int = 2,
        fill: Optional[float] = None,
) -> np.ndarray:
    """
    Draw bounding box on image.

    Args:
        image: Image to draw bounding box.
        bbox: Bounding box, position must be (x1, y1, x2, y2) and dtype must be int.
        color: Color of bounding box.
        thickness: Thickness of bounding box.
        fill: Fill bounding box.

    Returns:
        Image with bounding box.
    """
    x1, y1, x2, y2 = bbox
    image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    if fill is not None:
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)
        image = cv2.addWeighted(image, fill, image, 1 - fill, 0)
    return image


def draw_label(
        image: np.ndarray,
        label: str,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        *,
        align: Literal['left', 'center', 'right'] = 'left',
        thickness: int = 2,
        font_scale: float = 0.5,
) -> np.ndarray:
    """
    Draw label on image.

    Args:
        image: Image to draw label.
        label: Label.
        position: Position of label.
        color: Color of label.
        align: Align of label.
        thickness: Thickness of label.
        font_scale: Font scale of label.

    Returns:
        Image with label.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, _ = cv2.getTextSize(label, font, font_scale, thickness)
    if align == 'left':
        text_position = (position[0], position[1] + text_size[1])
    elif align == 'center':
        text_position = (position[0] - text_size[0] // 2, position[1] + text_size[1])
    elif align == 'right':
        text_position = (position[0] - text_size[0], position[1] + text_size[1])
    else:
        raise ValueError(f'Unknown align: {align}')
    image = cv2.putText(image, label, text_position, font, font_scale, color, thickness, cv2.LINE_AA)
    return image


def randomize_ids_color(ids: List[int]) -> List[Tuple[int, int, int]]:
    """
    Randomize ids color.

    Args:
        ids: Ids.

    Returns:
        Randomized ids color.
    """
    ids = list(set(ids))
    n = len(ids)
    colors = generate_farthest_colors(n)
    colors = {ids[i]: colors[i] for i in range(n)}
    return [colors[itm] for itm in ids]
