"""
MicroManager Interface
for image and Z position

2022.07.06 Phantomlsh
"""

from pycromanager import Core
import atexit
import numpy as np
import time
from magnetic_tweezer.units import Micrometer, Nanometer
import logging


class MicroManagerInterface:
    """Class interfacing with the microscope"""

    def __init__(self, microscope_model: str = 'MCL NanoDrive'):
        """Creates an instance to interface with the microscope.
        This should only be done once."""

        self._core = Core()
        self.microscope_model: str = microscope_model
        """Type of microscope used"""

        self.version_info: str = str(self._core.get_version_info())
        """Running Version of MicroManager"""

        # Snap an image to get height and width
        self._core.snap_image()
        tagged_image = self._core.get_tagged_image()

        self.height: int = tagged_image.tags["Height"]
        """Height of microscope images"""

        self.width: int = tagged_image.tags["Width"]
        """Width of microscope images"""

        logging.info("Mi(Py)croManager Initializing...")
        logging.info(f"Acquisition Size: Width = {self.width}, Height = {self.height}")

        self._core.start_continuous_sequence_acquisition(1)
        time.sleep(1)

    def __del__(self):
        self._core.stop_sequence_acquisition()
        logging.info("Mi(Py)croManager Exiting...")

    def get_image(self) -> np.ndarray:
        """Get the latest microscope image"""
        image = self._core.get_last_image()
        return np.reshape(image, (self.height, self.width))

    @property
    def z(self) -> Nanometer:
        """Z position (vertical) of the microscope in nm"""
        z_pos = Micrometer(
            self._core.get_property(f"{self.microscope_model} Z Stage", "Set position Z (um)")
        )
        return z_pos.to('nm')

    @z.setter
    def z(self, new_z: Nanometer):
        self._core.set_property(f"{self.microscope_model} Z Stage", "Set position Z (um)", new_z.to('um'))


if __name__ == '__main__':
    micro_manager = MicroManagerInterface()
    atexit.register(micro_manager.__del__)  # just in case - maybe not required
    logging.info(f'Version Info: {micro_manager.version_info}')
    logging.info(f'Current Z Value: {micro_manager.z}')
