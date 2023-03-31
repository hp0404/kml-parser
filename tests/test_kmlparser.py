# -*- coding: utf-8 -*-
import tempfile
from pathlib import Path

import pytest
from kmlparser import KMLParser


@pytest.fixture
def kml_file():
    content = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Sample KML</name>
        <Folder>
            <name>Folder1</name>
            <Placemark>
                <name>Place1</name>
                <address>Address1</address>
                <description><![CDATA[field1: value1 <br>field2: value2]]></description>
                <ExtendedData>
                    <Data name="field1">
                        <value>value1</value>
                    </Data>
                    <Data name="field2">
                        <value>value2</value>
                    </Data>
                </ExtendedData>
            </Placemark>
        </Folder>
        <Folder>
            <name>Folder2</name>
            <Placemark>
                <name>Place2</name>
                <description>Description2</description>
                <Point>
                    <coordinates>-122.08198699999999,37.422362,0</coordinates>
                </Point>
            </Placemark>
        </Folder>
    </Document>
</kml>
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file.flush()
        yield tmp_file.name


@pytest.fixture
def kml_file_without_folders():
    content = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Sample KML</name>
        <Placemark>
            <name>Place1</name>
            <address>Address1</address>
            <description><![CDATA[field1: value1 <br>field2: value2]]></description>
            <ExtendedData>
                <Data name="field1">
                    <value>value1</value>
                </Data>
                <Data name="field2">
                    <value>value2</value>
                </Data>
            </ExtendedData>
        </Placemark>
        <Placemark>
            <name>Place2</name>
            <description>Description2</description>
            <Point>
                <coordinates>-122.08198699999999,37.422362,0</coordinates>
            </Point>
        </Placemark>
    </Document>
</kml>
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file.flush()
        yield tmp_file.name


def test_kml_parser_parse(kml_file):
    input_path = Path(kml_file).resolve()
    parser = KMLParser(input_path)
    parsed_data = parser.parse()

    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2

    item1 = parsed_data[0]
    assert item1["name"] == "Place1"
    assert item1["address"] == "Address1"
    assert item1["description"] == "field1: value1 <br>field2: value2"
    assert item1["folder"] == "Folder1"
    assert item1["extended_data"] == {"field1": "value1", "field2": "value2"}

    item2 = parsed_data[1]
    assert item2["name"] == "Place2"
    assert item2["description"] == "Description2"
    assert item2["x"] == "-122.08198699999999"
    assert item2["y"] == "37.422362"
    assert item2["folder"] == "Folder2"


def test_kml_parser_parse_without_folders(kml_file_without_folders):
    input_path = Path(kml_file_without_folders).resolve()
    parser = KMLParser(input_path)
    parsed_data = parser.parse()

    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2

    item1 = parsed_data[0]
    assert item1["name"] == "Place1"
    assert item1["address"] == "Address1"
    assert item1["description"] == "field1: value1 <br>field2: value2"
    assert item1["extended_data"] == {"field1": "value1", "field2": "value2"}

    item2 = parsed_data[1]
    assert item2["name"] == "Place2"
    assert item2["description"] == "Description2"
    assert item2["x"] == "-122.08198699999999"
    assert item2["y"] == "37.422362"


def test_kml_parser_parse_with_mapping(kml_file):
    input_path = Path(kml_file).resolve()
    mapping = {"folder": "region", "name": "city"}
    parser = KMLParser(input_path, mapping=mapping)
    parsed_data = parser.parse()

    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2

    item1 = parsed_data[0]
    assert item1["city"] == "Place1"
    assert item1["region"] == "Folder1"


def test_kml_parser_parse_with_mapping_raises(kml_file):
    input_path = Path(kml_file).resolve()
    mapping = {"folder": "region", "name": "city"}
    parser = KMLParser(input_path, mapping=mapping)
    parsed_data = parser.parse()

    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2

    item1 = parsed_data[0]
    with pytest.raises(KeyError):
        assert (
            item1["address"] == "Address1"
        ), "keys not specified in `mapping` are excluded"
