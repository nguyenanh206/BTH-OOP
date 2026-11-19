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
    def notify(self, sender: object, event_code: str):
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
    def update(self, alert_event: AlertEvent):
        print(f"[EMAIL ALERT] Gửi mail cảnh báo tới ban quản lý -> Cảm biến: {alert_event.sensor_name} | Mức: {alert_event.severity} | Giá trị: {alert_event.value:.1f}{alert_event.unit}")


class AuditLogObserver(IAlertObserver):
    """Ghi nhận lịch sử cảnh báo[cite: 37, 38]."""
    def __init__(self):
        self._logs: List[str] = []

    @property
    def logs(self) -> List[str]:
        return list(self._logs)

    def update(self, alert_event: AlertEvent):
        entry = f"{alert_event.occurred_at.strftime('%Y-%m-%d %H:%M:%S')} | {alert_event.sensor_name} | {alert_event.value:.1f}{alert_event.unit} | {alert_event.severity}"
        self._logs.append(entry)
        print(f"[AUDIT LOG] Đã lưu log: {entry}")


class EmergencyBridgeObserver(IAlertObserver):
    """Cầu nối chuyển cảnh báo CRITICAL thành sự kiện cho EmergencyMediator[cite: 37, 38]."""
    def __init__(self, mediator: IEmergencyMediator):
        self._mediator = mediator

    def update(self, alert_event: AlertEvent):
        if alert_event.severity == "CRITICAL":
            self._mediator.notify(self, "FIRE_DETECTED")


class SensorMonitor:
    """Quản lý observer, đọc sensor, so ngưỡng và phát cảnh báo[cite: 38, 40]."""
    def __init__(self):
        self._observers: List[IAlertObserver] = []

    def attach(self, observer: IAlertObserver):
        if observer is None:
            raise ValueError("Observer không được null[cite: 40].")
        # Không cho cùng một observer đăng ký hai lần[cite: 40, 41]
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IAlertObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def check_sensor(self, sensor_name: str, sensor: ISensor):
        value = sensor.read_value()

        # Quy ước mức độ: < 50% bình thường, 50%..70% WARNING, >= 70% CRITICAL[cite: 38, 40]
        severity: Optional[str] = None
        if value >= 70.0:
            severity = "CRITICAL"
        elif value >= 50.0:
            severity = "WARNING"

        if severity is None:
            print(f"[MONITOR] {sensor_name}: {value:.1f}{sensor.get_unit()} -> Bình thường (không cảnh báo)[cite: 38].")
            return

        alert_event = AlertEvent(
            sensor_name=sensor_name,
            value=value,
            unit=sensor.get_unit(),
            severity=severity,
            occurred_at=datetime.datetime.now()
        )
        self._notify(alert_event)

    def _notify(self, alert_event: AlertEvent):
        # Duyệt trên bản sao danh sách để an toàn khi observer bị gỡ trong lúc thông báo[cite: 40, 41]
        for observer in list(self._observers):
            try:
                observer.update(alert_event)
            except Exception as ex:
                # Một observer lỗi không làm ảnh hưởng tới các observer khác[cite: 41]
                print(f"[ERROR] Lỗi khi thông báo tới {type(observer).__name__}: {ex}")


# ==================== 5. CHƯƠNG TRÌNH KIỂM THỬ (MAIN) ====================
if __name__ == "__main__":
    print("=== BẮT ĐẦU MÔ PHỎNG CAMPUS SAFETY HUB ===")

    # 1. Khởi tạo cảm biến cũ và Adapter[cite: 39]
    legacy_detector = LegacySmokeDetector(350)  # 350 -> 35.0% (Bình thường)
    smoke_sensor: ISensor = SmokeSensorAdapter(legacy_detector)
    print(f"Kiểm tra Adapter ban đầu: {smoke_sensor.read_value():.1f} {smoke_sensor.get_unit()}")

    # 2. Khởi tạo hệ thống ứng phó khẩn cấp (Mediator)[cite: 37, 38]
    alarm = Alarm()
    door_ctrl = DoorController()
    vent_ctrl = VentilationController()
    mediator = EmergencyMediator(alarm, door_ctrl, vent_ctrl)

    # 3. Khởi tạo Monitor và đăng ký các Observer[cite: 37, 38, 40]
    monitor = SensorMonitor()
    dashboard = DashboardObserver()
    email_alert = EmailAlertObserver()
    audit_log = AuditLogObserver()
    bridge = EmergencyBridgeObserver(mediator)

    monitor.attach(dashboard)
    monitor.attach(email_alert)
    monitor.attach(audit_log)
    monitor.attach(bridge)
    # Thử đăng ký trùng lặp (sẽ bị bỏ qua nhờ kiểm tra trong attach)[cite: 40, 41]
    monitor.attach(dashboard)

    # Kịch bản 1: Mức khói bình thường (< 50%)[cite: 38]
    print("\n--- Kịch bản 1: Cảm biến mức khói bình thường (35%) ---")
    monitor.check_sensor("SmokeSensor-Lab1", smoke_sensor)

    # Kịch bản 2: Mức khói cảnh báo WARNING (50% <= val < 70%)[cite: 38]
    print("\n--- Kịch bản 2: Cảm biến tăng lên mức WARNING (58.5%) ---")
    legacy_detector.set_smoke_level(585)
    monitor.check_sensor("SmokeSensor-Lab1", smoke_sensor)

    # Kịch bản 3: Mức khói nguy hiểm CRITICAL (>= 70%) -> Kích hoạt Mediator[cite: 38]
    print("\n--- Kịch bản 3: Cảm biến tăng lên mức CRITICAL (82.0%) ---")
    legacy_detector.set_smoke_level(820)
    monitor.check_sensor("SmokeSensor-Lab1", smoke_sensor)

    # Kịch bản 4: Hủy đăng ký EmailAlertObserver và kiểm tra lại[cite: 41]
    print("\n--- Kịch bản 4: Hủy đăng ký EmailAlertObserver và kiểm tra lại ---")
    monitor.detach(email_alert)
    legacy_detector.set_smoke_level(750)  # 75.0% CRITICAL
    monitor.check_sensor("SmokeSensor-Lab1", smoke_sensor)

    print("\n=== KẾT THÚC MÔ PHỎNG ===")
