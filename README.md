# Content Auto-Publish

A lightweight pipeline that takes content assembled in a Jupyter Notebook (text + images) and publishes it directly to a website, resizing every image to the target platform's exact required dimensions along the way.

## Problem

Manually resizing images to a CMS's required dimensions and copy-pasting content into a web publishing UI is slow and error-prone when you're producing content regularly. This pipeline lets content be drafted, previewed, and iterated on entirely inside a notebook, then published with a single function call.

## How it works

1. **Draft in-notebook**: content (title, body, image paths) is assembled and previewed directly in the notebook cells.
2. **Resize**: every image referenced in the content is resized (and center-cropped if needed) to the exact pixel dimensions the target platform requires, using Pillow.
3. **Publish**: the resized assets and formatted content are sent to the website's content API as a single publish call.
4. **Confirm**: the pipeline returns the live URL and logs the publish result back into the notebook.

## Structure

```
publish_pipeline.py   # Core resize + publish functions
config.py             # Target dimensions per platform/placement, API endpoint config
demo.ipynb            # End-to-end notebook demo: draft -> resize -> publish
```

## Example

```python
from publish_pipeline import Content, publish

post = Content(
    title="New AI avatar workflow walkthrough",
    body="...",
    image_path="draft_assets/cover.png",
)

result = publish(post, placement="blog_hero")
print(result["url"])
```

## Stack

- Python 3.11, Jupyter
- Pillow (image resizing/cropping)
- `requests` (publish API calls)

## Notes

This is a generalized rebuild of a personal automation pipeline originally wired to a specific CMS. The API client here targets a generic REST content endpoint so the pipeline can be adapted to any platform with a publish API.
