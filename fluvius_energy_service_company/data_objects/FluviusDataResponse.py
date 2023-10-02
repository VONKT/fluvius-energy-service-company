from typing import Generic, TypeVar



FluviusData = TypeVar('FluviusData')


class FluviusDataResponse(Generic[FluviusData]):
    def __init__(self, data: FluviusData):
        self.data = data
