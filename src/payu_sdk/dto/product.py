# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from payu_sdk.dto import DTO


@dataclass
class Product(DTO):
    name: str
    unitPrice: str
    quantity: str
