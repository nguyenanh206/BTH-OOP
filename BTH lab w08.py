# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, List, Dict, Callable, Optional, Set
from datetime import datetime

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

#Sự kiện thay đổi trạng thái
class DeviceStatusChangedEventArgs:
    def __init__(self, deviceId: str, oldStatus: DeviceStatus, newStatus: DeviceStatus, changedAt: datetime.datetime):
        self._deviceId = deviceId
        self._oldStatus = oldStatus
        self._newStatus = newStatus
        self._changedAt = changedAt

    @property
    def deviceId(self) -> str:
        return self._deviceId

    @property
    def oldStatus(self) -> DeviceStatus:
        return self._oldStatus

    @property
    def newStatus(self) -> DeviceStatus:
        return self._newStatus

    @property
    def changedAt(self) -> datetime.datetime:
        return self._changedAt
,
#Sự kiện cảnh báo thiết bị
class DeviceAlertEventArgs:
    def __init__(self, deviceId: str, message: str, severity: AlertSeverity, occurredAt: datetime.datetime):
        self._deviceId = deviceId
        self._message = message
        self._severity = severity
        self._occurredAt = occurredAt

    @property
    def deviceId(self) -> str:
        return self._deviceId

    @property
    def message(self) -> str:
        return self._message

    @property
    def severity(self) -> AlertSeverity:
        return self._severity

    @property
    def occurredAt(self) -> datetime.datetime:
        return self._occurredAt



#---------------------------
# NGOẠI LỆ NGHIỆP VỤ
#---------------------------

class InvalidDeviceReadingException(Exception):
    def __init__(self, deviceId: str, invalidValue: int):
        super().__init__(f"Giá trị đọc không hợp lệ ({invalidValue}) cho thiết bị {deviceId}. Phải từ 0 đến 100")
        self._deviceId = deviceId
        self._invalidValue = invalidValue

    @property
    def device_Id(self) -> str:
        return self._deviceId

    @property
    def invalidValue(self) -> int:
        return self._invalidValue

class Event:
    def __init__(self):
        self._listeners: List[Callable] = []

    def __iadd__(self, listener: Callable):
        if listener not in self._listeners:
            self._listeners.append(listener)
        return self

    def __isub__(self, listener: Callable):
        if listener in self._listeners:
            self._listeners.remove(listener)
        return self

    def invoke(self, sender, e):
        for listener in self._listeners:
            listener(sender, e)


#---------------------------
# Lớp trừu tượng 
#---------------------------
# TEACHING DEVICE

class TeachingDevice(ABC):
    def __init__(self, id: str, name: str, status: DeviceStatus = DeviceStatus.AVAILABLE):
        if not id or not id.strip():
            raise ValueError("Mã thiết bị không được rỗng")
        if not name or not name.strip():
            raise ValueError("Tên thiết bị phải hợp lệ")
        
        self._id = id
        self._name = name
        self._status = status

        self.statusChanged = Event()
        self.alertRaised = Event

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name


    @property
    def status(self) -> DeviceStatus:
        return self._status

    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value


    def ChangeStatus(self, newStatus: DeviceStatus):
        if newStatus == self._status:
            return
        oldStatus = self._status
        self._status = newStatus
        self.OnStatusChanged(
            DeviceStatusChangedEventArgs(self._id, oldStatus, self._status, datetime.datetime.now()))

    def RaiseAlert(self, message: str, severity: AlertSeverity):
        self.OnAlertRaised(
            DeviceAlertEventArgs(self._id, message, severity, datetime.datetime.now()))

    def OnStatusChanged(self, e: DeviceStatusChangedEventArgs):
        self.statusChanged.invoke(self, e)

    def OnAlertRaised(self, e: DeviceAlertEventArgs):
        self.alertRaised.invoke(self, e)

#----------------------------   
# CÁC LỚP DẪN XUẤT
#-----------------------------

# Projector Remote
class ProjectorRemote(TeachingDevice):
    def __init__(self, id: str, name: str, batteryLevel: int, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, status)
        if not (0 <= batteryLevel <= 100):
            raise ValueError("Mức pin phải từ 0 đến 100")
        self._batteryLevel = batteryLevel

    @property
    def batteryLevel(self) -> int:
        return self._batteryLevel

    def UpdateBatteryLevel(self, newLevel: int):
        if not (0 <= newLevel <= 100):
            raise InvalidDeviceReadingException(self.id, newLevel)

        oldLevel = self._batteryLevel
        self._batteryLevel = newLevel

        if self._batteryLevel == 0 and oldLevel != 0:
            self.RaiseAlert("Mức pin bằng 0%, thiết bị ngừng hoạt động!", AlertSeverity.CRITICAL)
        elif self._batteryLevel < 20 and oldLevel >= 20:
            self.RaiseAlert(f"Mức pin xuống thấp ({self._batteryLevel}%)", AlertSeverity.WARNING)

# Air Conditioner Remote
class AirConditionerRemote(TeachingDevice):
    def __init__(self, id: str, name: str, assignedRoom: str, isResponsive: bool = True, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, status)
        self._assignedRoom = assignedRoom
        self._isResponsive = isResponsive

    @property
    def assignedRoom(self) -> str:
        return self._assignedRoom

    @property
    def isResponsive(self) -> bool:
        return self._isResponsive

    def UpdateResponseState(self, isResponsive: bool):
        if self._isResponsive and not isResponsive:
            self._isResponsive = False
            self.RaiseAlert(f"Điều hòa tại phòng {self._assignedRoom} không phản hồi tín hiệu", AlertSeverity.CRITICAL)
        elif not self._isResponsive and isResponsive:
            self._isResponsive = True
            self.RaiseAlert(f"Điều hòa tại phòng {self._assignedRoom} đã hoạt động trở lại.", AlertSeverity.INFORMATION)
    
# WIRELESS MICROPHONE
class WirelessMicrophone(TeachingDevice):
    def __init__(self, id: str, name: str, batteryLevel: int, signalQuality: int, status: DeviceStatus = DeviceStatus.AVAILABLE):
        super().__init__(id, name, status)
        if not (0 <= batteryLevel <= 100):
            raise InvalidDeviceReadingException(id, batteryLevel)
        if not (0 <= signalQuality <= 100):
            raise InvalidDeviceReadingException(id, signalQuality)
        
        self._batteryLevel = batteryLevel
        self._signalQuality = signalQuality

    @property
    def batteryLevel(self) -> int:
        return self._batteryLevel

    def signalQuality(self) -> int:
        return self._signalQuality
    
    def UpdateBatteryLevel(self, newLevel: int):
        if not (0 <= newLevel <= 100):
            raise InvalidDeviceReadingException(self.id, newLevel)
        self._batteryLevel = newLevel
        
        if self._batterylevel == 0:
            self.RaiseAlert("Pin micro bằng 0%!", AlertSeverity.CRITICAL)
        elif self._batteryLevel < 30:
            self.RaiseAlert(f"Pin micro thấp ({self._batteryLevel}%)", AlertSeverity.WARNING)

    def UpdateSignalQuality(self, newQuality: int):
        if not (0 <= newQuality <= 100):
            raise InvalidDeviceReadingException(self.id, newQuality)
        self._signalQuality = newQuality
        
        if self._signalQuality == 0:
            self.RaiseAlert("Tín hiệu micro mất hoàn toàn (0%)!", AlertSeverity.CRITICAL)
        elif self._signalSuality < 40:
            self.RaiseAlert(f"Chất lượng tín hiệu micro kém ({self._signalQuality}%)", AlertSeverity.WARNING)


#------------------------------
# CÁC SUBSCRIBER
#------------------------------
# Hiển thị cảnh báo
class ConsoleNotificationService:
    def HandleAlert(self, sender, e: DeviceAlertEventArgs):
        print(f"[THÔNG BÁO CONSOLE] [{e.severity.name}] {e.deviceId}: {e.message}")

#Ghi lại lịch sử thay đổi trạng thái
class DeviceAuditLogger:
    def __init__(self):
        self._entries: List[str] = []

    @property
    def entries(self) -> List[str]:
        return list(self._entries)

    def HandleStatusChanged(self, sender, e: DeviceStatusChangedEventArgs):
        logEntry = f"{e.changedAt.strftime('%Y-%m-%d %H:%M:%S')} : {e.deviceId}, {e.oldStatus.name} -> {e.newStatus.name}"
        self._entries.append(logEntry)
        print(f"[AUDIT LOGGER] {logEntry}")

# Yêu cầu bảo trì
class MaintenanceService:
    def __init__(self):
        self._requests: List[str] = []

    @property
    def requests(self) -> List[str]:
        return list(self._requests)

    def HandleCriticalAlert(self, sender, e: DeviceAlertEventArgs):
        if e.severity != AlertSeverity.CRITICAL:
            return
        requestMsg = f"Yêu cầu bảo trì cho {e.deviceId}: {e.message}"
        self._requests.append(requestMsg)
        print(f"[MAINTENANCE SERVICE] Đã tạo phiếu: {requestMsg}")


#-------------------------------
# DELEGATE & CALLBACK
#-------------------------------
#áp dụng delegate trước khi thực thi 

class FilteredAlertSubscriber:
    def __init__(self, filterFunc: AlertFilter, action: Callable[[DeviceAlertEventArgs], None]):
        self._filter = filterFunc
        self._action = action

    def HandleAlert(self, sender, e: DeviceAlertEventArgs):
        if self._filter(e):
            self._action(e)

# --------------------------------------------
# LỚP ĐIỀU PHỐI ĐĂNG KÍ
# --------------------------------------------
class DeviceMonitoringCoordinator:
    def __init__(self, devices: IEnumerable[TeachingDevice], 
                 notificationService: ConsoleNotificationService, 
                 auditLogger: DeviceAuditLogger, 
                 maintenanceService: MaintenanceService):
        self._devices = list(devices)
        self._notificationService = notificationService
        self._auditLogger = auditLogger
        self._maintenanceService = maintenanceService
        self._isSubscribed = False

    def subscribe(self):
        if self._isSubscribed:
            return
        for device in self._devices:
            device.statusChanged -= self._auditLogger.HandleStatusChanged
            device.statusChanged += self._auditLogger.HandleStatusChanged

            device.alertRaised -= self._notificationService.HandleAlert
            device.alertRaised += self._notificationService.HandleAlert

            device.alertRaised -= self._maintenanceService.HandleCriticalAlert
            device.alertRaised += self._maintenanceService.HandleCriticalAlert
        self._isSubscribed = True
        print("[COORDINATOR] Đã đăng ký thành công các event cho thiết bị.")

    def unsubscribe(self):
        if not self._isSubscribed:
            return
        for device in self._devices:
            device.statusChanged -= self._auditLogger.HandleStatusChanged
            device.alertRaised -= self._notificationService.HandleAlert
            device.alertRaised -= self._maintenanceService.HandleCriticalAlert
        self._isSubscribed = False
        print("[COORDINATOR] Đã hủy đăng ký các event.")

    def dispose(self):
        self.unsubscribe()

 

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
