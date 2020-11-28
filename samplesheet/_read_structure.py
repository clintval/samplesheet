from attr import attrs, attrib
from attrs_strict import type_validator


@attrs(auto_attribs=True, frozen=True)
class ReadStructure(object):
    struct: str = attrib(converter=str, validator=type_validator())

    def __str__(self) -> str:
        return self.struct
