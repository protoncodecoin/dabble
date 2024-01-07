"""
Utils for anime app.
"""
video_format = [
    "mp4",
    "mkv",
]


def video_file_checker(file_type: str):
    """
    Check if video format is supported.
    """
    if file_type in video_format:
        return True
    return False


def media_renamer(
    content_name: str, season_number: int, episode_number: int, file_type: str
):
    """
     Rename media files.
    Format: series name + season number+ episode number + type
    """
    file_name = (
        f"{content_name}_season_{season_number}_episode_{episode_number}.{file_type}"
    )
    return file_name
