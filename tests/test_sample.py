from attrs_strict._error import UnionError
from pytest import raises

from samplesheet import ReadStructure
from samplesheet import Sample
from samplesheet.util import CaselessDict


class TestSample(object):
    """Unit tests for class:`samplesheet.Sample`."""

    #: A dummy sample ID just for unit tests.
    sample_id: str = "4JYC"

    #: A realistic dummy sample.
    complete_sample: Sample = Sample(
        sample_id="4JYC",
        sample_name="sample_name",
        library_id="library_id",
        project="project",
        description="description",
        lane=4,
        i7_index_bases="GTTACTC",
        i5_index_bases="TTGCTAA",
        read_structure=ReadStructure("8M1S142T8B8B8M1S142T"),
        attrs={"REFERENCE": "hg38"},
    )

    def test_required_constructor(self):
        with raises(TypeError):
            Sample()  # The field sample_id is minimally required
        sample = Sample(sample_id=self.sample_id)
        assert sample.sample_id == self.sample_id

    def test_read_structure_promotion(self):
        struct = "8M1S142T"
        sample1 = Sample(self.sample_id, read_structure=struct)
        assert isinstance(sample1.read_structure, ReadStructure)
        assert sample1.read_structure == ReadStructure(struct)
        sample2 = Sample(self.sample_id, read_structure=ReadStructure(struct))
        assert isinstance(sample2.read_structure, ReadStructure)
        assert sample2.read_structure == ReadStructure(struct)

    def test_type_validations_for_non_converted_fields(self):
        with raises(UnionError):
            Sample(self.sample_id, sample_name=1)
        with raises(UnionError):
            Sample(self.sample_id, library_id=1)
        with raises(UnionError):
            Sample(self.sample_id, project=1)
        with raises(UnionError):
            Sample(self.sample_id, description=1)
        with raises(UnionError):
            Sample(self.sample_id, lane=str(1))
        with raises(UnionError):
            Sample(self.sample_id, i7_index_bases=1)
        with raises(UnionError):
            Sample(self.sample_id, i5_index_bases=1)

    def test_attrs_promotion(self):
        attrs = {"REFERENCE": "hg38"}
        sample1 = Sample(self.sample_id, attrs=attrs)
        assert isinstance(sample1.attrs, CaselessDict)
        assert sample1.attrs == CaselessDict(attrs)
        sample2 = Sample(self.sample_id, attrs=CaselessDict(attrs))
        assert isinstance(sample2.attrs, CaselessDict)
        assert sample2.attrs == CaselessDict(attrs)

    def test_fields(self):
        sample = Sample(sample_id=self.sample_id)
        assert sample.fields() == [
            "sample_id",
            "sample_name",
            "library_id",
            "project",
            "description",
            "lane",
            "i7_index_bases",
            "i5_index_bases",
            "read_structure",
            "attrs",
        ]

    def test_copy(self):
        copy = self.complete_sample.copy(project="PROJECT")
        assert copy.sample_id == self.complete_sample.sample_id
        assert copy.sample_name == self.complete_sample.sample_name
        assert copy.library_id == self.complete_sample.library_id
        assert copy.project != self.complete_sample.project
        assert copy.description == self.complete_sample.description
        assert copy.lane == self.complete_sample.lane
        assert copy.i7_index_bases == self.complete_sample.i7_index_bases
        assert copy.i5_index_bases == self.complete_sample.i5_index_bases
        assert copy.read_structure == self.complete_sample.read_structure
        assert copy.attrs == self.complete_sample.attrs

    def test_dict(self):
        assert self.complete_sample.dict() == {
            "sample_id": "4JYC",
            "sample_name": "sample_name",
            "library_id": "library_id",
            "project": "project",
            "description": "description",
            "lane": 4,
            "i7_index_bases": "GTTACTC",
            "i5_index_bases": "TTGCTAA",
            "read_structure": ReadStructure("8M1S142T8B8B8M1S142T"),
            "REFERENCE": "hg38",
        }

    def test_from_dict(self):
        mapping = self.complete_sample.dict()
        assert self.complete_sample == Sample.from_dict(mapping)

    def test_json(self):
        assert self.complete_sample.json() == (
            '{"sample_id": "4JYC", '
            + '"sample_name": "sample_name", '
            + '"library_id": "library_id", '
            + '"project": "project", '
            + '"description": "description", '
            + '"lane": 4, '
            + '"i7_index_bases": "GTTACTC", '
            + '"i5_index_bases": "TTGCTAA", '
            + '"read_structure": "8M1S142T8B8B8M1S142T", '
            + '"REFERENCE": "hg38"}'
        )

    def test__repr__(self):
        assert repr(self.complete_sample) == (
            "Sample(sample_id='4JYC',"
            + " sample_name='sample_name',"
            + " library_id='library_id',"
            + " project='project',"
            + " description='description',"
            + " lane=4,"
            + " i7_index_bases='GTTACTC',"
            + " i5_index_bases='TTGCTAA',"
            + " read_structure=ReadStructure(struct='8M1S142T8B8B8M1S142T'),"
            + " attrs=CaselessDict({'REFERENCE': 'hg38'})"
            + ")"
        )

    def test__str__(self):
        assert str(self.complete_sample) == (
            "Sample(sample_id='4JYC',"
            + " sample_name='sample_name',"
            + " library_id='library_id',"
            + " project='project',"
            + " description='description',"
            + " lane=4,"
            + " i7_index_bases='GTTACTC',"
            + " i5_index_bases='TTGCTAA',"
            + " read_structure=ReadStructure(struct='8M1S142T8B8B8M1S142T'),"
            + " attrs=CaselessDict({'REFERENCE': 'hg38'})"
            + ")"
        )
