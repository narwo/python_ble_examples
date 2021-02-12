from bleson.core.roles import Advertiser
from bleson.core.types import Advertisement
from bleson.interfaces.adapter import Adapter
from bleson.logger import log


class FooBeacon(Advertiser):
    def __init__(self, adapter, data=None):
        super().__init__(adapter)
        self.advertisement=Advertisement()
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        if data:
            self.advertisement.raw_data=self.foo_data_adv_data(data)
            log.info("Beacon Adv raw data = {}".format(self.advertisement.raw_data))

    @classmethod
    def foo_data_adv_data(cls, data):
        log.info("Encoding data for Foo beacon: '{}'".format(data))
        encodeddata = data
        encodeddataLength = len(encodeddata)

        if encodeddataLength > 18:
            raise ValueError("Encoded data length {} is > 18 maximum length.".format(encodeddataLength))

        message = [
                # 0x02,   # Flags length
                # 0x01,   # Flags data type value
                # 0x1a,   # Flags data

                # 0x03,   # Service UUID length
                # 0x03,   # Service UUID data type value
                # 0xaa,   # 16-bit Foo UUID
                # 0xfe,   # 16-bit Foo UUID

                # len(encodeddata), # Service Data length
                ]

        message += encodeddata

        return bytearray(message)