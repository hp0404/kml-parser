# -*- coding: utf-8 -*-
import typing
from pathlib import Path
import bs4


class KMLParser:
    def __init__(
        self,
        document: typing.Union[Path, str],
        mapping: typing.Optional[typing.Dict[str, str]] = None,
    ) -> None:
        self.soup = self._parse_document(document)
        self.mapping = mapping

    @staticmethod
    def _parse_document(document: typing.Union[Path, str]) -> bs4.BeautifulSoup:
        if isinstance(document, Path):
            with document.open("r") as f:
                contents = f.read()
        else:
            contents = document
        return bs4.BeautifulSoup(contents, "lxml-xml")

    def _rename_fields(self, response: typing.Dict[str, str]) -> typing.Dict[str, str]:
        if self.mapping is None:
            return response
        _data = {}
        for k, v in response.items():
            if k in self.mapping:
                _data[self.mapping[k]] = v
        return _data

    def _parse_placemark(self, placemark: bs4.element.Tag):
        response = {}
        coords = placemark.find("coordinates")
        if coords is not None:
            response["x"] = coords.text.split(",")[0].strip("\n").strip()
            response["y"] = coords.text.split(",")[1].strip("\n").strip()

        description = placemark.find("description")
        if description is not None:
            response["description"] = description.text

        address = placemark.find("address")
        if address is not None:
            response["address"] = address.text

        name = placemark.find("name")
        if name is not None:
            response["name"] = name.text

        extended_data = placemark.find("ExtendedData")
        if extended_data is not None:
            metadata = {}
            for item in extended_data.find_all("Data"):
                metadata[item["name"]] = item.find("value").text.strip()
            response["extended_data"] = metadata

        return response

    def parse(self) -> typing.List[typing.Dict[str, typing.Any]]:
        data = []
        # assuming there are Folder attrs in the document
        for folder in self.soup.find_all("Folder"):
            for placemark in folder.find_all("Placemark"):
                item = self._parse_placemark(placemark)
                item["folder"] = folder.find("name").text
                data.append(self._rename_fields(item))
        # assuming there's no Folder attributes
        if not data:
            for placemark in self.soup.find_all("Placemark"):
                item = self._parse_placemark(placemark)
                data.append(self._rename_fields(item))
        return data
