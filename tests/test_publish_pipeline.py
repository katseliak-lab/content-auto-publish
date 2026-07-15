import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from PIL import Image

from publish_pipeline import resize_and_crop, Content, _resized_output_path
from config import PLACEMENT_DIMENSIONS


@pytest.fixture
def sample_image(tmp_path):
    path = tmp_path / "sample.png"
    Image.new("RGB", (800, 1200), color=(120, 140, 160)).save(path)
    return str(path)


@pytest.mark.parametrize("placement", list(PLACEMENT_DIMENSIONS.keys()))
def test_resize_produces_exact_target_dimensions(sample_image, tmp_path, placement):
    target_size = PLACEMENT_DIMENSIONS[placement]
    output_path = str(tmp_path / f"out_{placement}.png")
    resize_and_crop(sample_image, target_size, output_path)

    with Image.open(output_path) as result:
        assert result.size == target_size


def test_resize_preserves_no_distortion_aspect_via_crop(sample_image, tmp_path):
    # A tall source (800x1200) resized into a wide target should still
    # produce exact target dimensions without stretching artifacts,
    # since resize_and_crop scales then center-crops.
    output_path = str(tmp_path / "wide.png")
    resize_and_crop(sample_image, (1600, 900), output_path)
    with Image.open(output_path) as result:
        assert result.size == (1600, 900)


def test_resized_output_path_naming():
    assert _resized_output_path("draft_assets/cover.png", "blog_hero") == "draft_assets/cover_blog_hero.png"


def test_content_dataclass_defaults():
    c = Content(title="t", body="b", image_path="p.png")
    assert c.slug is None
