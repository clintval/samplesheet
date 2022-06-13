from .util import NoneInt
from .util import NoneStr
from ._samplesheet import Section

from ._read_structure import ReadStructure
from ._sample import Sample

from .util import CaselessDict
from .util import FrozenDict

from typing import Mapping

Mapping.register(CaselessDict)
Mapping.register(FrozenDict)
