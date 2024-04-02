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


class MicroManagerInterface:
    """Class interfacing with the microscope"""

    def __init__(self, microscope_model: str = 'MCL NanoDrive'):
        """Creates an instance to interface with the microscope.
        This should only be done once."""

        self._core = Core()
        self.microscope_model = microscope_model
        """Type of microscope used"""

        self.version_info: str = str(self._core.get_version_info())
        """Running Version of MicroManager"""

        # Snap an image to get height and width
        self._core.snap_image()
        tagged_image = self._core.get_tagged_image()

        self.height = tagged_image.tags["Height"]
        """Height of microscope images"""

        self.width = tagged_image.tags["Width"]
        """Width of microscope images"""

        print("Mi(Py)croManager Initializing...")
        print(f"Acquisition Size: Width = {self.width}, Height = {self.height}")

        self._core.start_continuous_sequence_acquisition(1)
        time.sleep(1)

    def __del__(self):
        self._core.stop_sequence_acquisition()
        print("Mi(Py)croManager Exiting...")

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
    print(f'Version Info: {micro_manager.version_info}')
    print(f'Current Z Value: {micro_manager.z}')
