# -*- coding: utf-8 -*-
import typing
from pathlib import Path
import bs4


class KMLParser:
    def __init__(
        self, file_path: Path, mapping: typing.Optional[typing.Dict[str, str]] = None
    ) -> None:
        with file_path.open("r") as f:
            self.soup = bs4.BeautifulSoup(f, "lxml-xml")
        self.mapping = mapping

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
        for folder in self.soup.find_all("Folder"):
            if folder is None:
                raise KeyError("Folder key is missing.")
            for placemark in folder.find_all("Placemark"):
                item = self._parse_placemark(placemark)
                item["folder"] = folder.find("name").text
                data.append(self._rename_fields(item))
        return data
