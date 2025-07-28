"""Public API for the ICF (IOBEWI Capsule Format) package."""

# Export the core classes from the CLI implementation so that callers can write
# ``from icf import icfCapsule`` without having to know the internal layout of
# the package.  The command line interface relies on this behaviour.

from .cli.icf import icfCapsule, Cycle, Matiere, BadgeType

__all__ = ["icfCapsule", "Cycle", "Matiere", "BadgeType"]

