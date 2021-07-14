"""
 This file is part of nucypher.

 nucypher is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 nucypher is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""

import click
from marshmallow import fields

from nucypher.control.specifications.exceptions import InvalidInputData


class BaseField:

    click_type = click.STRING

    def __init__(self, *args, **kwargs):
        self.click = kwargs.pop('click', None)
        super().__init__(*args, **kwargs)


#
# Very common, simple field types to build on.
#

class String(BaseField, fields.String):
    pass


class List(BaseField, fields.List):
    pass


class StringList(List):
    """
    Expects a delimited string, if input is not already a list. The string is split using the delimiter arg
    (defaults to ',' if not provided) and returns a corresponding List of object.
    """
    def __init__(self, *args, **kwargs):
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, list):
            value = value.split(self.delimiter)
        return super()._deserialize(value, attr, data, **kwargs)


class Integer(BaseField, fields.Integer):
    click_type = click.INT


class PositiveInteger(Integer):
    def _validate(self, value):
        if not value > 0:
            raise InvalidInputData(f"{self.name} must be a positive integer.")
