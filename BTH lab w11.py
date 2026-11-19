# Họ và tên : Nguyễn Hà Anh
# MSSV: 20241883

from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import List, Optional


# ==================== 1. GIAO DIỆN CẢM BIẾN & DỮ LIỆU CẢNH BÁO ====================
class ISensor(ABC):
    @abstractmethod
    def ReadValue(self) -> float:
        pass

    @abstractmethod
    def GetUnit(self) -> str:
        pass


@dataclass(frozen=True)
class AlertEvent:
    SensorName: str
    Value: float
    Unit: str
    Severity: str
    OccurredAt: datetime.datetime


# ==================== 2. ADAPTER PATTERN ====================
class LegacySmokeDetector:
    def __init__(self, smokeLevel: int):
        self._smokeLevel = self._clamp(smokeLevel, 0, 1000)

    @staticmethod
    def _clamp(val: int, minVal: int, maxVal: int) -> int:
        return max(minVal, min(maxVal, val))

    def GetSmokeLevel(self) -> int:
        return self._smokeLevel

    def GetDescription(self) -> str:
        return "Legacy smoke detector"

    def SetSmokeLevel(self, value: int):
        self._smokeLevel = self._clamp(value, 0, 1000)

# Chuyển đổi giao diện và thang đo (0..1000 -> 0..100%) của LegacySmokeDetector
class SmokeSensorAdapter(ISensor):
    def __init__(self, legacy: LegacySmokeDetector):
        if legacy is None:
            raise ValueError("LegacySmokeDetector không được null")
        self._legacy = legacy

    def ReadValue(self) -> float:
        #Chuyển đổi thang 0..1000 thành phần trăm 0..100
        return self._legacy.GetSmokeLevel() / 10.0

    def GetUnit(self) -> str:
        return "% smoke"


# ==================== 3. MEDIATOR PATTERN ====================
class IEmergencyMediator(ABC):
    @abstractmethod
    def notify(self, sender: object, eventCode: str):
        pass

#Điều khiển còi báo động
class Alarm:
    def SoundAlarm(self):
        print("[ALARM] Còi báo động khẩn cấp ĐANG KÊU!")

    def StopAlarm(self):
        print("[ALARM] Đã tắt còi báo động")

#Điều khiển cửa thoát hiểm
class DoorController:
    def UnlockAllDoors(self):
        print("[DOOR] Đã mở khóa tất cả cửa thoát hiểm!")

    def LockDoors(self):
        print("[DOOR] Đã khóa cửa.")

#Điều khiển hút khói
class VentilationController:
    def StartExhaust(self):
        print("[VENTILATION] Đã bật quạt thông gió")

    def stop_exhaust(self):
        print("[VENTILATION] Đã tắt quạt hút khói.")

# Phối hợp cho Alarm, Door và Ventilation theo sự kiện
class EmergencyMediator(IEmergencyMediator):
    def __init__(self, alarm: Alarm, doorController: DoorController, ventilationController: VentilationController):
        self._alarm = alarm
        self._door = doorController
        self._ventilation = ventilationController

    def notify(self, sender: object, eventCode: str):
        if eventCode == "FIRE_DETECTED":
            print("\n>>> [MEDIATOR] Tiếp nhận tín hiệu FIRE_DETECTED -> Kích hoạt quy trình khẩn cấp!")
            self._alarm.SoundAlarm()
            self._door.UnlockAllDoors()
            self._ventilation.StartExhaust()


# ==================== 4. OBSERVER PATTERN ====================
#Hợp đồng nhận cảnh báo
class IAlertObserver(ABC):
    @abstractmethod
    def Update(self, alertEvent: AlertEvent):
        pass

# Hiển thị cảnh báo lên bảng điều khiển
class DashboardObserver(IAlertObserver):
    def Update(self, alertEvent: AlertEvent):
        print(f"[DASHBOARD] {alertEvent.SensorName}: {alertEvent.Value:.1f}{alertEvent.Unit} [{alertEvent.Severity}]")

#Mô phỏng gửi email cảnh báo khi có sự cố
class EmailAlertObserver(IAlertObserver):
    def update(self, alertEvent: AlertEvent):
        print(f"[EMAIL ALERT] Gửi mail cảnh báo tới ban quản lý -> Cảm biến: {alertEvent.SensorName} | Mức: {alertEvent.Severity} | Giá trị: {alertEvent.Value:.1f}{alertEvent.Unit}")

#Ghi nhận lịch sử cảnh báo
class AuditLogObserver(IAlertObserver):
    def __init__(self):
        self._logs: List[str] = []

    @property
    def Logs(self) -> List[str]:
        return list(self._logs)

    def Update(self, alertEvent: AlertEvent):
        entry = f"{alertEvent.OccurredAt.strftime('%Y-%m-%d %H:%M:%S')} | {alertEvent.SensorName} | {alertEvent.Value:.1f}{alertEvent.Unit} | {alertEvent.Severity}"
        self._logs.append(entry)
        print(f"[AUDIT LOG] Đã lưu log: {entry}")

#Cầu nối chuyển cảnh báo CRITICAL thành sự kiện cho EmergencyMediator
class EmergencyBridgeObserver(IAlertObserver):
    def __init__(self, mediator: IEmergencyMediator):
        self._mediator = mediator

    def Update(self, alertEvent: AlertEvent):
        if alertEvent.Severity == "CRITICAL":
            self._mediator.notify(self, "FIRE_DETECTED")

#Quản lý observer, đọc sensor, so ngưỡng và phát cảnh báo
class SensorMonitor:
    def __init__(self):
        self._observers: List[IAlertObserver] = []

    def Attach(self, observer: IAlertObserver):
        if observer is None:
            raise ValueError("Observer không được null")
        if observer not in self._observers:
            self._observers.append(observer)

    def Detach(self, observer: IAlertObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def CheckSensor(self, sensorName: str, sensor: ISensor):
        value = sensor.ReadValue()

        #< 50% bình thường, 50%..70% WARNING, >= 70% CRITICAL
        severity: Optional[str] = None
        if value >= 70.0:
            severity = "CRITICAL"
        elif value >= 50.0:
            severity = "WARNING"

        if severity is None:
            print(f"[MONITOR] {sensorName}: {value:.1f}{sensor.GetUnit()} -> Bình thường (không cảnh báo)")
            return

        alertEvent = AlertEvent(
            sensorName = sensorName,
            value = value,
            unit = sensor.GetUnit(),
            severity = severity,
            occurredAt = datetime.datetime.now()
        )
        self._notify(alertEvent)

    def _Notify(self, alertEvent: AlertEvent):
        for observer in list(self._observers):
            try:
                observer.Update(alertEvent)
            except Exception as ex:
                print(f"[ERROR] Lỗi khi thông báo tới {type(observer).__name__}: {ex}")


# ==================== 5. TEST ====================
if __name__ == "__main__":
    print("=== BẮT ĐẦU MÔ PHỎNG CAMPUS SAFETY HUB ===")

    # 1. Khởi tạo cảm biến cũ và Adapter
    legacyDetector = LegacySmokeDetector(350)  # 350 -> 35.0% (Bình thường)
    smokeSensor: ISensor = SmokeSensorAdapter(legacyDetector)
    print(f"Kiểm tra Adapter ban đầu: {smokeSensor.ReadValue():.1f} {smokeSensor.GetUnit()}")

    # 2. Khởi tạo hệ thống ứng phó khẩn cấp (Mediator)
    alarm = Alarm()
    doorCtrl = DoorController()
    ventCtrl = VentilationController()
    mediator = EmergencyMediator(alarm, doorCtrl, ventCtrl)

    # 3. Khởi tạo Monitor và đăng ký các Observer
    monitor = SensorMonitor()
    dashboard = DashboardObserver()
    emailAlert = EmailAlertObserver()
    auditLog = AuditLogObserver()
    bridge = EmergencyBridgeObserver(mediator)

    monitor.Attach(dashboard)
    monitor.Attach(emailAlert)
    monitor.Attach(auditLog)
    monitor.Attach(bridge)
    # Thử đăng ký trùng lặp 
    monitor.Attach(dashboard)

    # Kịch bản 1: Mức khói bình thường (< 50%)
    print("\n--- Kịch bản 1: Cảm biến mức khói bình thường (35%) ---")
    monitor.CheckSensor("SmokeSensor-Lab1", smokeSensor)

    # Kịch bản 2: Mức khói cảnh báo WARNING (50% <= val < 70%)
    print("\n--- Kịch bản 2: Cảm biến tăng lên mức WARNING (58.5%) ---")
    legacyDetector.SetSmokeLevel(585)
    monitor.CheckSensor("SmokeSensor-Lab1", smokeSensor)

    # Kịch bản 3: Mức khói nguy hiểm CRITICAL (>= 70%) -> Kích hoạt Mediator
    print("\n--- Kịch bản 3: Cảm biến tăng lên mức CRITICAL (82.0%) ---")
    legacyDetector.SetSmokeLevel(820)
    monitor.CheckSensor("SmokeSensor-Lab1", smokeSensor)

    # Kịch bản 4: Hủy đăng ký EmailAlertObserver và kiểm tra lại
    print("\n--- Kịch bản 4: Hủy đăng ký EmailAlertObserver và kiểm tra lại ---")
    monitor.detach(emailAlert)
    legacyDetector.SetSmokeLevel(750)  # 75.0% CRITICAL
    monitor.CheckSensor("SmokeSensor-Lab1", smokeSensor)

    print("\n=== KẾT THÚC MÔ PHỎNG ===")
