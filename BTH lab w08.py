# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, List, Dict, Callable, Optional, Set

# Enum cho trạng thái thiết bị
class DeviceStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    UNDER_MAINTENANCE = 3

#Mức độ cảnh báo - enum
class AlertSeverity(Enum):
    INFORMATION = 1
    WARNING = 2
    CRITICAL = 3

#--------------------------
# LỚP DỮ LIỆU SỰ KIỆN
#--------------------------




#---------------------------
# NGOẠI LỆ NGHIỆP VỤ
#---------------------------

#Trùng ID
class DuplicateIdException(Exception):
    def __init__(self, duplicateId: str):
        super().__init__(f"Mã thiết bị '{duplicateId}' đã tồn tại")
        self._duplicatedId = duplicateId

# Khôgn thấy mục phù hợp
class NoSuitableItemException(Exception):
    def __init__(self, message: str = "Không cthấy mục phù hợp."):
        super().__init__(message)

# Thiết bị không sẵn sàng
class DeviceNotReadyException(Exception):
     def __init__(self, deviceId: str, currentStatus: DeviceStatus):
        super().__init__(f"Thiết bị '{deviceId}' không sẵn sàng (Trạng thái: {currentStatus.name}).")
        self.deviceId = deviceId
        self.currentStatus = currentStatus

#---------------------------
# Lớp trừu tượng 
#---------------------------

# Interface nhận diện đối tượng
class IIdentifiable(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
# TEACHING DEVICE

class TeachingDevice(IIdentifiable, ABC):
    def __init__(self, id: str, name: str, storageLocation: str, status: DeviceStatus = DeviceStatus.AVAILABLE):
        if not id or not id.strip():
            raise ValueError("Mã thiết bị không được rỗng")
        if not name or not name.strip():
            raise ValueError("Tên thiết bị phải hợp lệ")
        if not storageLocation or not storageLocation.strip():
            raise ValueError("Vị trí lưu trữ không được rỗng")
        
        self._id = id
        self._name = name
        self._storageLocation = storageLocation
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def storageLocation(self) -> int:
        return self._storageLocation

    @property
    def status(self) -> DeviceStatus:
        return self._status

    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value

# Ktra khả năng sẵn sàng của thiết bị
    def IsReadyForUse(self) -> bool:
        pass

#Tính điểm ưu tiên của thiết bị 
    def GetDefaultPriorityScore(self) -> float:
        pass

# Mượn thiết bị
    def Borrow(self):
        if not self.IsReadyForUse():
            raise DeviceNotReadyException(self._id, self._status)
        self._status = DeviceStatus.BORROWED

# Trả thiết bị
    def Return(self):
        if self._status != DeviceStatus.BORROWED:
            raise DeviceNotReadyException(self._id, self._status)
        self._status = DeviceStatus.AVAILABLE

    def __str__(self) -> str:
        return (f"[{type(self).__name__}] {self._id} - {self._name} | "
                f"{self._storageLocation} | {self._status.value}")
    
#----------------------------   
# CÁC LỚP DẪN XUẤT
#-----------------------------

# Projector Remote
class ProjectorRemote(TeachingDevice):
    def __init__(self, id: str, name: str, storageLocation: str, batteryLevel: int, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, storageLocation, status)
        if not (0 <= batteryLevel <= 100):
            raise ValueError("Mức pin phải từ 0 đến 100")
        self._batteryLevel = batteryLevel

    @property
    def batteryLevel(self) -> int:
        return self._batteryLevel

    def IsReadyForUse(self) -> bool:
        return self._status == DeviceStatus.AVAILABLE and self._batteryLevel >= 20

    def GetDefaultPriorityScore(self) -> float:
        return float(self._batteryLevel)


# Air Conditioner Remote
class AirConditionerRemote(TeachingDevice):
    def __init__(self, id: str, name: str, storageLocation: str, compatibleRooms, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, storageLocation, status)
        self._compatibleRooms = frozenset(compatibleRooms)

    @property
    def compatibleRooms(self) -> frozenset:
       return self._compatibleRooms

    def IsCompatibleWith(self, roomId: str) -> bool:
       return roomId in self._compatibleRooms

    def IsReadyForUse(self) -> bool:
       return self._status == DeviceStatus.AVAILABLE 
    
    def GetDefaultPriorityScore(self) -> float:
        return 100.0 if self._compatibleRooms else 0.0
    
# WIRELESS MICROPHONE
class WirelessMicrophone(TeachingDevice):
    def __init__(self, id: str, name: str, storageLocation: str, batteryLevel: int, signalQuality: int, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, storageLocation, status)
        if not (0 <= batteryLevel <= 100):
            raise ValueError("Mức pin phải từ 0 đến 100")
        if not (0 <= signalQuality <= 100):
            raise ValueError("CHất lượng tín hiệu phải từ 0 đến 100")
        self._batteryLevel = batteryLevel
        self._signalQuality = signalQuality

    @property
    def batteryLevel(self) -> int:
        return self._batteryLevel

    def signalQuality(self) -> int:
        return self._signalQuality
    
    def IsReadyForUse(self) -> bool:
        return self._status == DeviceStatus.AVAILABLE and self._batteryLevel >= 30 and self._signalQuality >= 40

    def GetDefaultPriorityScore(self) -> float:
        return float(self._batteryLevel + self._signalQuality) / 2.0


#------------------------------
# CÁC SUBSCRIBER
#------------------------------

#-------------------------------
# DELEGATE & CALLBACK
#-------------------------------


# --------------------------------------------
# LỚP ĐIỀU PHỐI ĐĂNG KÍ
# --------------------------------------------


 

# ---------------------------------------
# KIỂM THỬ
# ---------------------------------------
def ExpectError(title: str, action, exc_type) -> None:
    try:
        action()
        print(f"   !! {title}: không có ngoại lệ (không mong đợi)")
    except exc_type as ex:
        print(f"   {title}: bắt {type(ex).__name__} -> {ex}")
 
 
def main():
    p1 = ProjectorRemote("PJ01", "Remote Epson 1", "Kho A", 85)
    p2 = ProjectorRemote("PJ02", "Remote Epson 2", "Kho A", 55)
    p3 = ProjectorRemote("PJ03", "Remote Epson 3", "Kho A", 15)          # pin yếu -> chưa sẵn sàng
    a1 = AirConditionerRemote("AC01", "Remote Daikin", "Kho B", {"A101", "A203"})
    a2 = AirConditionerRemote("AC02", "Remote Panasonic", "Kho B", {"B102"})
    m1 = WirelessMicrophone("MIC01", "Micro Shure", "Kho C", 90, 80)
    m2 = WirelessMicrophone("MIC02", "Micro Sony", "Kho C", 60, 50)
    m3 = WirelessMicrophone("MIC03", "Micro Boya", "Kho C", 20, 90)      # pin yếu -> chưa sẵn sàng
 
    
 
 
if __name__ == "__main__":
    main()