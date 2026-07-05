# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time
from dataclasses import dataclass


@dataclass
class Auth:
    access_token: str
    token_type: str
    expires_in: int
    grant_type: str
    expires_timestamp: int = 0

    def __post_init__(self):
        timestamp = int(time.time())
        self.expires_timestamp = timestamp + self.expires_in

    def is_expired(self):
        timestamp = int(time.time())
        if timestamp > self.expires_timestamp:
            return True
        else:
            return False
