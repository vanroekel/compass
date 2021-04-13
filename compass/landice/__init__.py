from compass.mpas_core import MpasCore
from compass.landice.tests.dome import Dome
from compass.landice.tests.eismint2 import Eismint2
from compass.landice.tests.enthalpy_benchmark import EnthalpyBenchmark
from compass.landice.tests.greenland import Greenland
from compass.landice.tests.hydro_radial import HydroRadial


class Landice(MpasCore):
    """
    The collection of all test case for the MALI core
    """

    def __init__(self):
        """
        Construct the collection of MALI test cases
        """
        super().__init__(name='landice')

        self.add_test_group(Dome(mpas_core=self))
        self.add_test_group(Eismint2(mpas_core=self))
        self.add_test_group(EnthalpyBenchmark(mpas_core=self))
        self.add_test_group(Greenland(mpas_core=self))
        self.add_test_group(HydroRadial(mpas_core=self))
