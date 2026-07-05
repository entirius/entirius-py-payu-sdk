# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from payu_sdk.dto import DTO
from payu_sdk.dto.buyer import Buyer
from payu_sdk.dto.pay_method import PayMethods
from payu_sdk.dto.product import Product


@dataclass
class Order(DTO):
    customerIp: str
    merchantPosId: str
    description: str
    totalAmount: str
    buyer: Buyer
    products: list[Product]

    currencyCode: str = "PLN"
    notifyUrl: str | None = None
    extOrderId: str | None = None
    continueUrl: str | None = None
    cardOnFile: str | None = None
    payMethods: PayMethods | None = None
