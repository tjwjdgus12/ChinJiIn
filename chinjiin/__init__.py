"""Public API for the ChinJiIn typo corrector."""

from .chinjiin import fix, fix_dir, fix_file

__all__ = ["fix", "fix_file", "fix_dir"]
