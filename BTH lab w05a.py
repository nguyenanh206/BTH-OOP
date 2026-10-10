# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# Enum cho trạngt hái thiết bị
class DeviceStatus(Enum):
    ACTIVE = 1
    UNDER_MAINTENANCE = 2
    RETIRED = 3

# Lớp trừu tượng Device
class Device(ABC):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus):
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
        def estimatedAnnualMaintenanceCosts(selff) -> float:
            pass

        def __str__(self) -> str:
            currentYear = datetime.datetime.now().year
            age = currentYear - self._yearInUse
            return{f"Mã thiết bị: {self._id} | Tên thiết bị: {self._name} | "
                   f"Năm đưa vào sử dụng: {self._yearInUse} | "
                   f"Giá mua: {self._purchasePrice: ,.0f} | Trạng thái: {self._status.name}"}


# INTERFACE
class INetworkable(ABC):
    @property
    @abstractmethod
    def IpAddress(self) -> str:
        pass

    @abstractmethod
    def Connect(self, IpAddress: str):
        pass

    @abstractmethod
    def Disconnect(self):
        pass

    @property
    @abstractmethod
    def IsConnected(self) -> bool:
        pass


# CÁC LỚP DẪN XUẤT

# COMPUTER
class Computer(Device, INetworkable):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, 
                 ram: int, processor: str, hasDiscreteGPU: bool):
        super().__init__(id, name, yearInUse, purchasePrice, status)
        self.ram = ram
        self.processor = processor
        self.hasDiscreteGPU = hasDiscreteGPU
        self._IpAddress = None
        self._IsConnected = False

    # Tính chi phí bảo trì
    def estimatedAnnualMaintenanceCosts(self) -> float:
        cost = self.purchasePrice * 0.05
        if self.hasDiscreteGPU:
            cost += self.purchasePrice * 0.02

        if (datetime.datetime.now().year - self.yearInUse) > 5:
            cost += self.purchasePrice * 0.01
        return cost

    @property
    def IpAddress(self) -> str:
        return self._IpAddress

    def Connect(self, IpAddress : str):
        if not IpAddress or not IpAddress.strip():
            raise ValueError("Địa chỉ IP không được rỗng")

        if self.IsConnected:
            raise Exception("Không cho phép kết nối lại khi thiết bị đang kết nối.")

        self._IpAddress = IpAddress
        self._IsConnected = True


    def Disconnect(self):
        self._IsConnected = False
        self._IpAddress = None

    @property
    def IsConnected(self) -> bool:
        return self._IsConnected

# PRINTER
class Printer(Device):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus,
                 printerType: str, pagePrinted: int, hasColor: bool):
        super().__init__(id, name, yearInUse, purchasePrice, status)
        self.printerType = printerType
        self.pagePrinted = pagePrinted
        self.hasColor = hasColor

    # Tính chi phí bảo trì
    def estimatedAnnualMaintenanceCosts(self) -> float:
            cost = self.purchasePrice * 0.04
    
            if self.pagePrinted > 100000:
                cost += 500000

            if self.hasColor:
                cost += 300000
            return cost

# PHƯƠNG ÁN: Mô hình mọi máy in đều có khả năng mạng -> printer chỉ thực thi INetworkable
class NetworkPrinter(Printer, INetworkable):
    def __inti__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus,
                 printerType: str, pagePrinted: int, hasColor: bool):
        super().__init__(id, name, yearInUse, purchasePrice, status, printerType, pagePrinted, hasColor)
        self._IpAddress = None
        self._IsConnected = False

    @property
    def IpAddress(self) -> str:
        return self._IpAddress
    
    def Connect(self, IpAddress : str):
        if not IpAddress or not IpAddress.strip():
            raise ValueError("Địa chỉ IP không được rỗng")
    
        if self.IsConnected:
            raise Exception("Không cho phép kết nối lại khi thiết bị đang kết nối.")
    
        self._IpAddress = IpAddress
        self._IsConnected = True
    
    
    def Disconnect(self):
        self._IsConnected = False
        self._IpAddress = None
    
    @property
    def IsConnected(self) -> bool:
        return self._IsConnected

# PROJECTOR
class Projector(Device):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus,
                 brightNessLumen: int, bulbHoursUsed: int):
        super().__init__(id, name, yearInUse, purchasePrice, status)
        self.brightNessLumen = brightNessLumen
        self.bulbHoursUsed = bulbHoursUsed

# Tính chi phí bảo trì
    def estimatedAnnualMaintenanceCosts(self) -> float:
            cost = self.purchasePrice * 0.03
    
            if self.bulbHoursUsed > 3000:
                cost += 1500000

            return cost


# KẾT TẬP
# LABROOM
class LabRoom:
    def __init__(self, roomId: str, roomName: str, capacity: int):
        self.roomId = roomId
        self.roomName = roomName
        self.capacity = capacity
        self.devices: list[Device] = []

    # Thêm Thiết bị
    def AddDevice(self, device: Device):
        if device is None:
            raise ValueError("Không chấp nhận đối tượng thiết bị Null")

        for dv in self.devices:
            if dv.id == device.id:
                raise ValueError("Không thêm hai thiết bị có cùng mã vào một phòng")

        self.devices.append(device)

    # Tìm thiết bị
    def FindDevice(self, id: str) -> Device | None:
        for dv in self.devices:
            if dv.id == id:
                return dv

        return None

    # xoa thiết bị
    def RemoveDevice(self, id: str) -> bool:
        device = self.FindDevice(id)
        if device:
            self.devices.remove(device)
            return True
        return False

    # Sử dụng tính đa hình
    def estimatedAnnualMaintenanceCosts(self) -> float:
        totalCost = 0.0
        for dv in self.devices:
            totalCost += d.estimatedAnnualMaintenanceCosts()
        return totalCost

    def GetDevicesRequiringMaintenance(self) -> list[Device]:
        result = []

        for dv in self.devices:
            age = datetime.datetime.now().year - d._yearInUse
            if dv.status == DeviceStatus.UNDER_MAINTENANCE or age > 5:
                result.append(dv)
        return result


# KIỂM THỬ
__name__ == "__main__":
   
