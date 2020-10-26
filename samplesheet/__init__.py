from ._samplesheet import NoneInt
from ._samplesheet import NoneStr
from ._samplesheet import Section

from ._samplesheet import ReadStructure
from ._samplesheet import Sample

# from ._samplesheet import SampleSheet

from .util import CaselessDict
from .util import FrozenDict

from typing import Mapping

Mapping.register(CaselessDict)
Mapping.register(FrozenDict)
