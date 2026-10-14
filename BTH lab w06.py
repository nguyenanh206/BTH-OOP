# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# Enum cho trạngt hái thiết bị
class DeviceStatus(Enum):
    Available = 1
    Borrowed = 2
    UnderMaintenance = 3

# Lớp trừu tượng Device
class Device(ABC):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, maxBorrowDays: int):
        if not id or not id.strip():
            raise ValueError("Mã thiết bị không được rỗng")
        if purchasePrice <= 0:
            raise ValueError("Giá mua phải lớn hơn 0")
        
        currentYear = datetime.datetime.now().year
        if yearInUse > currentYear:
            raise ValueError("Nam đưa vào sử dụng không được lớn hơn năm hiện tại")

        self._id = id
        self._name = name
        self._yearInUse = yearInUse
        self._purchasePrice = purchasePrice
        self._status = status
        self._maxBorrowDays = maxBorrowDays

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def yearInUse(self) -> int:
        return self._yearInUse

    @property
    def purchasePrice(self) -> float:
        return self._purchasePrice
    @property
    def status(self) -> DeviceStatus:
        return self._status
    
# Phương thức trừu tượng tính chi phí bảo trì dự kiến trong một năm.
    @abstractmethod
    def CalculateAnnualMaintenanceCost(self) -> float:
        pass

    def __str__(self) -> str:
        currentYear = datetime.datetime.now().year
        age = currentYear - self._yearInUse
        return (f"Mã thiết bị: {self._id} | Tên thiết bị: {self._name} | "
                f"Năm đưa vào sử dụng: {self._yearInUse} | "
                f"Giá mua: {self._purchasePrice: ,.0f} | Trạng thái: {self._status.name}")