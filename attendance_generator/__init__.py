from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("attendance-generator")
except PackageNotFoundError:
    __version__ = "dev"

from attendance_generator.generator import generate_doc
from attendance_generator.pipeline import run
from attendance_generator.wizard import run_wizard

__all__ = ["run", "generate_doc", "run_wizard", "__version__"]
