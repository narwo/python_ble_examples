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
        dataLength = len(data)

        if dataLength > 31:
            raise ValueError("Encoded data length {} is > 31 maximum length.".format(dataLength))

        return data
