from django import template
import os

register = template.Library()

CATEGORY_EMOJIS = {
    "images": "🖼️",
    "documents": "📄",
    "videos": "🎥",
    "audio": "🎵",
    "archives": "📦",
    "other": "📎",
}

CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "svg", "webp"],
    "documents": ["pdf", "txt", "doc", "docx", "odt"],
    "videos": ["mp4", "webm", "ogg", "avi", "mov", "mkv"],
    "audio": ["mp3", "wav", "ogg", "flac"],
    "archives": ["zip", "tar", "gz", "rar", "7z"],
    "other": [],
}


@register.filter
def basename(value):
    return os.path.basename(value)


@register.filter
def file_emoji(value):
    ext = value.split(".")[-1].lower()

    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return CATEGORY_EMOJIS.get(category, CATEGORY_EMOJIS["other"])

    return CATEGORY_EMOJIS["other"]
