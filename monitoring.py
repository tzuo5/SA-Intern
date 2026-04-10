import sys


def render_progress(current: int, total: int, label: str, width: int = 30):
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(f"\r{label} [{bar}] [{current}/{total}]")
    sys.stdout.flush()


