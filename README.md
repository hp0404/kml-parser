# kml-parser

A library for parsing KML files.

## Installation
Install this tool using poetry:

```console
poetry install
```

## Usage

```python
>>> from pathlib import Path
>>> from kmlparser import KMLParser
>>> input_path = Path("sample.kml").resolve()
>>> parser = KMLParser(input_path)
>>> data = parser.parse()
```

The `mapping` parameter is an optional dictionary that allows you to specify custom names for the fields in the KML file. 

This is useful when the KML file you are parsing has fields with different names than the ones you want to use in your application. 

Also, note that only the keys mentioned will be included if you provide the mapping, e.g. {"name": "region", "folder": "building_type"} will only return those, discarding the default "placemark", "address", and "description" keys.

```python
>>> from pathlib import Path
>>> from kmlparser import KMLParser
>>> input_path = Path("sample.kml").resolve()
>>> mapping = {"name": "region", "folder": "building_type"}
>>> parser = KMLParser(input_path, mapping=mapping)
>>> data = parser.parse()
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```console
cd kmlparser
python -m venv env
source env/bin/activate
```

Now install the dependencies:

```console
pip install -e ".[testing]"
```