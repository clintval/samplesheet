import json

from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

import attr
import cattr

from attr import attrs, attrib
from attrs_strict import type_validator

from ._read_structure import ReadStructure
from .util import CaselessDict, NoneInt, NoneStr


def _maybe_make_read_structure(
    struct: Optional[Union[str, ReadStructure]]
) -> Optional[ReadStructure]:
    """Optionally build a read structure."""
    return ReadStructure(struct) if struct is not None else None


@attrs(auto_attribs=True, frozen=True)
class Sample(object):
    sample_id: str = attrib(validator=type_validator())
    sample_name: NoneStr = attrib(default=None, validator=type_validator())
    library_id: NoneStr = attrib(default=None, validator=type_validator())
    project: NoneStr = attrib(default=None, validator=type_validator())
    description: NoneStr = attrib(default=None, validator=type_validator())
    lane: NoneInt = attrib(default=None, validator=type_validator())
    i7_index_bases: NoneStr = attrib(default=None, validator=type_validator())
    i5_index_bases: NoneStr = attrib(default=None, validator=type_validator())
    read_structure: Optional[ReadStructure] = attrib(
        default=None, converter=_maybe_make_read_structure, validator=type_validator()
    )
    attrs: Mapping[str, str] = attrib(
        factory=CaselessDict, converter=CaselessDict, validator=type_validator()
    )

    @staticmethod
    def fields() -> List[str]:
        return [field.name for field in attr.fields(Sample)]

    def copy(self, **kwargs: Dict[Any, Any]) -> "Sample":
        return attr.evolve(self, **kwargs)

    def dict(self) -> Dict[str, str]:
        cattr.unstructure(self)

    def json(self) -> str:
        return json.dumps(self.dict(), cls=SampleJSONEncoder)

    @classmethod
    def from_dict(cls, mapping: Mapping[Any, Any]) -> "Sample":
        return cattr.structure(mapping, cls)


class SampleJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, ReadStructure):
            return str(obj)
        if isinstance(obj, Sample):
            return obj.json()
        return json.JSONEncoder.default(self, obj)
