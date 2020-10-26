import json

from typing import Any, Dict, List, Mapping, Optional, Union

import attr

from attr import attrs, attrib
from attrs_strict import type_validator

from samplesheet.util import CaselessDict

NoneInt = Optional[int]
NoneStr = Optional[str]
Section = Mapping[str, str]


@attrs(auto_attribs=True, frozen=True)
class ReadStructure(object):
    struct: str = attrib(converter=str, validator=type_validator())

    def __str__(self) -> str:
        return self.struct


def _maybe_make_read_structure(
    struct: Optional[Union[str, ReadStructure]]
) -> Optional[ReadStructure]:
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
    attrs: Mapping[str, str] = attrib(factory=CaselessDict, validator=type_validator())

    @staticmethod
    def fields() -> List[str]:
        return [field.name for field in attr.fields(Sample)]

    def copy(self, **kwargs: Dict[Any, Any]) -> "Sample":
        return attr.evolve(self, **kwargs)

    def dict(self) -> Dict[str, str]:
        signature = {field: getattr(self, field) for field in self.fields()}
        signature.pop("attrs")
        return {**signature, **self.attrs}

    def json(self) -> str:
        return json.dumps(self.dict(), cls=SampleSheetJSONEncoder)

    @classmethod
    def from_dict(cls, mapping: Mapping[Any, Any]) -> "Sample":
        required = {field: mapping.get(field, None) for field in cls.fields()}
        optional = {key: value for key, value in mapping.items() if key not in cls.fields()}
        return cls(**{**required, **optional})


class SampleSheetJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, ReadStructure):
            return str(obj)
        if isinstance(obj, Sample):
            return obj.json()
        # if isinstance(obj, SampleSheet):
        #    return obj.json()
        return json.JSONEncoder.default(self, obj)
