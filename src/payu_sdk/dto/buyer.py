# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from payu_sdk.dto import DTO


@dataclass
class Buyer(DTO):
    email: str
    phone: str
    firstName: str
    lastName: str
    language: str | None = None
