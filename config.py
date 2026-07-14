# Target output dimensions (width, height) per placement.
# Extend this dict to match whatever platform you're publishing to.
PLACEMENT_DIMENSIONS = {
    "blog_hero": (1600, 900),
    "blog_inline": (1000, 667),
    "social_square": (1080, 1080),
    "social_story": (1080, 1920),
}

PUBLISH_API_URL = "https://example-cms.local/api/v1/posts"
API_TOKEN_ENV_VAR = "CMS_API_TOKEN"
