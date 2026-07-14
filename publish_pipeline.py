import os
from dataclasses import dataclass
from typing import Optional

import requests
from PIL import Image

from config import PLACEMENT_DIMENSIONS, PUBLISH_API_URL, API_TOKEN_ENV_VAR


@dataclass
class Content:
    title: str
    body: str
    image_path: str
    slug: Optional[str] = None


def resize_and_crop(image_path: str, target_size: tuple, output_path: str) -> str:
    """
    Resizes an image to fill target_size exactly, center-cropping any
    excess so the aspect ratio matches without distortion.
    """
    target_w, target_h = target_size
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        src_w, src_h = img.size
        src_ratio = src_w / src_h
        target_ratio = target_w / target_h

        if src_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * src_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / src_ratio)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))

        img.save(output_path, quality=90)

    return output_path


def publish(content: Content, placement: str) -> dict:
    if placement not in PLACEMENT_DIMENSIONS:
        raise ValueError(f"Unknown placement '{placement}'. Add it to config.PLACEMENT_DIMENSIONS.")

    target_size = PLACEMENT_DIMENSIONS[placement]
    output_path = _resized_output_path(content.image_path, placement)
    resize_and_crop(content.image_path, target_size, output_path)

    token = os.environ.get(API_TOKEN_ENV_VAR, "")
    with open(output_path, "rb") as image_file:
        response = requests.post(
            PUBLISH_API_URL,
            headers={"Authorization": f"Bearer {token}"},
            data={"title": content.title, "body": content.body, "slug": content.slug or ""},
            files={"image": image_file},
            timeout=30,
        )
    response.raise_for_status()
    return response.json()


def _resized_output_path(original_path: str, placement: str) -> str:
    base, ext = os.path.splitext(original_path)
    return f"{base}_{placement}{ext}"
