from bleson.core.roles import Advertiser
from bleson.core.types import Advertisement
from bleson.interfaces.adapter import Adapter
from bleson.logger import log


class FooBeacon(Advertiser):
    def __init__(self, adapter, url=None):
        super().__init__(adapter)
        self.advertisement=Advertisement()
        self.url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        if url:
            self.advertisement.raw_data=self.foo_url_adv_data(url)
            log.debug("Beacon Adv raw data = {}".format(self.advertisement.raw_data))

    schemes = [
        "http://www.",
        "https://www.",
        "http://",
        "https://",
    ]

    extensions = [
        ".com/", ".org/", ".edu/", ".net/", ".info/", ".biz/", ".gov/",
        ".com", ".org", ".edu", ".net", ".info", ".biz", ".gov",
    ]

    @classmethod
    def encode_url(cls, url):
        i = 0
        data = []

        for s in range(len(cls.schemes)):
            scheme = cls.schemes[s]
            if url.startswith(scheme):
                data.append(s)
                i += len(scheme)
                break
        else:
            raise Exception("Invalid url scheme")

        while i < len(url):
            if url[i] == '.':
                for e in range(len(cls.extensions)):
                    expansion = cls.extensions[e]
                    if url.startswith(expansion, i):
                        data.append(e)
                        i += len(expansion)
                        break
                else:
                    data.append(0x2E)
                    i += 1
            else:
                data.append(ord(url[i]))
                i += 1

        return data

    @classmethod
    def foo_url_adv_data(cls, url):
        log.info("Encoding URL for Foo beacon: '{}'".format(url))
        encodedurl = cls.encode_url(url)
        encodedurlLength = len(encodedurl)

        if encodedurlLength > 18:
            raise ValueError("Encoded url length {} is > 18 maximum length.".format(encodedurlLength))

        message = [
                0x02,   # Flags length
                0x01,   # Flags data type value
                0x1a,   # Flags data

                0x03,   # Service UUID length
                0x03,   # Service UUID data type value
                0xaa,   # 16-bit Foo UUID
                0xfe,   # 16-bit Foo UUID

                5 + len(encodedurl), # Service Data length
                0x16,   # Service Data data type value
                0xaa,   # 16-bit Foo UUID
                0xfe,   # 16-bit Foo UUID

                0x10,   # Foo-url frame type
                0xed,   # txpower
                ]

        message += encodedurl

        return bytearray(message)