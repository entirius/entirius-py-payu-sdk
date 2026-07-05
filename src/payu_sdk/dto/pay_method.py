# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from payu_sdk.dto import DTO


@dataclass
class PayMethod(DTO):
    type: str
    value: str


@dataclass
class PayMethods(DTO):
    payMethod: PayMethod

    @staticmethod
    def factory(type: str, value: str) -> "PayMethods":
        return PayMethods(
            payMethod=PayMethod(
                type=type,
                value=value,
            )
        )
