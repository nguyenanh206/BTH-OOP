# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
import datetime
from typing import Generic, TypeVar, List, Dict, Callable, Optional, Set

# Enum cho trạng thái thiết bị
class DeviceStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    UNDER_MAINTENANCE = 3


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
    def Id(self) -> str:
        pass
# TEACHING DEVICE

class TeachingDevice(IIdentifiable, ABC):
    def __init__(self, id: str, name: str, storageLocation: str, status: DeviceStatus.AVAILABLE):
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
    def GetDefaultPrioritygScore(self) -> float:
        pass

# Mượn thiết bị
    def Borrow(self):
        if not self.IsReadyForUse():
            raise DeviceNotReadyException(self._id, self._status)
        self._status = DeviceStatus.BORROWED

# Trả thiết bị
    def Return(self):
        if self._status != DeviceStatus.BORROWED:
            raise Exception(f"Thiết bị '{self._id}' không ở trạng thái đang mượn để trả")

    def __str__(self) -> str:
        return (f"[{type(self).__name__}] {self._id} - {self._name} | "
                f"{self._storageLocation} | {self._status.value}")
    
#----------------------------   
# CÁC LỚP DẪN XUẤT
#-----------------------------

# Projector Remote
class ProjectorRemote(TeachingDevice):
    def __init__(self, id: str, name: str, storageLocation: str, status: DeviceStatus.AVAILABLE, batteryLevel: int):
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
    def __init__(self, id: str, name: str, storageLocation: str,status: DeviceStatus = DeviceStatus.AVAILABLE, compatibleRooms: Set[str]):
        super().__init__(id, name, status, storageLocation)
        self._compatibleRooms = frozenset(compatibleRooms)

    @property
    def compatibleRooms(self) -> frozenset:
       return self._compatibleRooms

    def IsCompatibleWith(self, roomId: str) -> bool:
       return roomId in self._compatibleRooms

    def IsReadyForUse(self) -> bool:
       return self._status == DeviceStatus.AVAILABLE 
    
    def GetDefaultPriorityScore(self) -> float:
        return 100.0 if self._compatible_rooms else 0.0
    
# WIRELESS MICROPHONE
class WirelessMicrophone(TeachingDevice):
    def __init__(self, id: str, name: str, storageLocation: str, status: DeviceStatus.AVAILABLE, batteryLevel: int, signalQuality: int):
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

    

#-------------------------------
# KHO LƯU TRỮ TỔNG QUÁT
#-------------------------------
# Interface generic
T = TypeVar("T", bound=IIdentifiable)
class IRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T):
        pass
 
    @abstractmethod
    def remove(self, itemId: str) -> bool: 
        pass
 
    @abstractmethod
    def FindById(self, itemId: str) -> Optional[T]: 
        pass
 
    @abstractmethod
    def GetAll(self) -> List[T]: 
        pass
 
    @abstractmethod
    def Findll(self, condition: Callable[[T], bool]) -> List[T]: 
        pass

#Lớp InMemoryRepository<T>
class InMemoryRepository(IRepository[T]):
    def __init__(self):
        self._items: dict[str, T] = {}
 
    def add(self, item: T) -> None:
        if item is None:
            raise ValueError("Không chấp nhận phần tử null.")
        if not isinstance(item, IIdentifiable):          # ràng buộc kiểm tra thêm ở thời điểm chạy
            raise TypeError("Phần tử phải triển khai IIdentifiable.")
        if item.id in self._items:
            raise DuplicateIdException(item.id)
        self._items[item.id] = item
 
    def remove(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None
 
    def find_by_id(self, item_id: str) -> Optional[T]:
        return self._items.get(item_id)
 
    def get_all(self) -> list[T]:
        return list(self._items.values())                # bản sao, không lộ collection nội bộ
 
    def find_all(self, condition: Callable[[T], bool]) -> list[T]:
        return [x for x in self._items.values() if condition(x)]

# ============================================================
# 6. CHIẾN LƯỢC LỰA CHỌN (generic + đa hình)
# ============================================================
class ISelectionStrategy(ABC, Generic[T]):
    @abstractmethod
    def select(self, candidates: Sequence[T]) -> T: ...
 
 
class HighestPriorityStrategy(ISelectionStrategy[T]):
    def __init__(self, score_selector: Callable[[T], float]):
        if score_selector is None:
            raise ValueError("score_selector không được null.")
        self._score_selector = score_selector
 
    def select(self, candidates: Sequence[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        return max(candidates, key=self._score_selector)   # không sửa danh sách đầu vào
 
 
class FirstAvailableStrategy(ISelectionStrategy[T]):
    def select(self, candidates: Sequence[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        return candidates[0]
 
 
# ============================================================
# 7. DỊCH VỤ CẤP PHÁT TỔNG QUÁT
# ============================================================
D = TypeVar("D", bound=TeachingDevice)     # where T : TeachingDevice
 
 
class AllocationService(Generic[D]):
    def __init__(self, repository: IRepository[D], strategy: ISelectionStrategy[D]):
        if repository is None or strategy is None:
            raise ValueError("repository và strategy không được null.")
        self._repository = repository
        self._strategy = strategy
 
    def change_strategy(self, new_strategy: ISelectionStrategy[D]) -> None:
        if new_strategy is None:
            raise ValueError("Chiến lược mới không được null.")
        self._strategy = new_strategy
 
    def allocate(self, additional_condition: Optional[Callable[[D], bool]] = None) -> D:
        # 1-2. lấy từ repository, chỉ giữ thiết bị sẵn sàng (đa hình qua is_ready_for_use)
        candidates = self._repository.find_all(lambda d: d.is_ready_for_use())
        # 3. áp dụng điều kiện bổ sung nếu có
        if additional_condition is not None:
            candidates = [d for d in candidates if additional_condition(d)]
        # 4. chọn bằng chiến lược hiện tại (không biết chiến lược cụ thể là gì)
        selected = self._strategy.select(candidates)
        # 5-6. cấp phát: nếu borrow() lỗi thì chưa có gì thay đổi
        selected.borrow()
        return selected
 
 
# ============================================================
# 8. KIỂM THỬ
# ============================================================
def expect_error(title: str, action, exc_type) -> None:
    try:
        action()
        print(f"   !! {title}: không có ngoại lệ (không mong đợi)")
    except exc_type as ex:
        print(f"   {title}: bắt {type(ex).__name__} -> {ex}")
 
 
def main() -> None:
    # --- dữ liệu mẫu ---
    p1 = ProjectorRemote("PJ01", "Remote Epson 1", "Kho A", 85)
    p2 = ProjectorRemote("PJ02", "Remote Epson 2", "Kho A", 55)
    p3 = ProjectorRemote("PJ03", "Remote Epson 3", "Kho A", 15)          # pin yếu -> chưa sẵn sàng
    a1 = AirConditionerRemote("AC01", "Remote Daikin", "Kho B", {"A101", "A203"})
    a2 = AirConditionerRemote("AC02", "Remote Panasonic", "Kho B", {"B102"})
    m1 = WirelessMicrophone("MIC01", "Micro Shure", "Kho C", 90, 80)
    m2 = WirelessMicrophone("MIC02", "Micro Sony", "Kho C", 60, 50)
    m3 = WirelessMicrophone("MIC03", "Micro Boya", "Kho C", 20, 90)      # pin yếu -> chưa sẵn sàng
 
    projector_repo = InMemoryRepository[ProjectorRemote]()
    ac_repo = InMemoryRepository[AirConditionerRemote]()
    mic_repo = InMemoryRepository[WirelessMicrophone]()
 
    print("1. Thêm thiết bị vào repository")
    for d in (p1, p2, p3):
        projector_repo.add(d)
    for d in (a1, a2):
        ac_repo.add(d)
    for d in (m2, m1, m3):          # MIC02 (điểm thấp hơn) đứng trước MIC01 để thấy rõ khác biệt giữa hai chiến lược
        mic_repo.add(d)
    print(f"   Máy chiếu: {len(projector_repo.get_all())}, điều hòa: {len(ac_repo.get_all())}, "
          f"micro: {len(mic_repo.get_all())}")
 
    print("\n2. Thêm hai thiết bị trùng mã")
    expect_error("Thêm lại PJ01",
                 lambda: projector_repo.add(ProjectorRemote("PJ01", "Trùng", "Kho A", 70)),
                 DuplicateIdException)
 
    print("\n3. Tìm thiết bị theo mã")
    print("   MIC02 ->", mic_repo.find_by_id("MIC02"))
    print("   XXX   ->", mic_repo.find_by_id("XXX"))
 
    print("\n4. Lọc các thiết bị sẵn sàng")
    print("   Micro sẵn sàng:", [d.id for d in mic_repo.find_all(lambda d: d.is_ready_for_use())])
    print("   Máy chiếu sẵn sàng:", [d.id for d in projector_repo.find_all(lambda d: d.is_ready_for_use())])
 
    print("\n5. Chọn điều khiển máy chiếu có điểm cao nhất")
    projector_service = AllocationService[ProjectorRemote](
        projector_repo,
        HighestPriorityStrategy[ProjectorRemote](lambda d: d.get_default_priority_score()))
    selected = projector_service.allocate(lambda d: True)
    print("   Được chọn:", selected)
 
    print("\n6. Chọn điều khiển điều hòa tương thích phòng A203")
    ac_service = AllocationService[AirConditionerRemote](
        ac_repo, HighestPriorityStrategy[AirConditionerRemote](lambda d: d.get_default_priority_score()))
    selected_ac = ac_service.allocate(lambda d: d.is_compatible_with("A203"))
    print("   Được chọn:", selected_ac)
 
    print("\n7. Chọn micro đầu tiên sẵn sàng")
    mic_service = AllocationService[WirelessMicrophone](mic_repo, FirstAvailableStrategy[WirelessMicrophone]())
    first_mic = mic_service.allocate()
    print("   Được chọn:", first_mic)
 
    print("\n8. Đổi chiến lược trong thời gian chạy")
    first_mic.return_device()                                  # trả MIC01 về kho
    print("   Sau khi trả:", first_mic.status.value)
    chosen = mic_service.allocate()
    print("   FirstAvailable  ->", chosen.id, "(đứng đầu danh sách, điểm", chosen.get_default_priority_score(), ")")
    chosen.return_device()
    mic_service.change_strategy(HighestPriorityStrategy[WirelessMicrophone](lambda d: d.get_default_priority_score()))
    chosen = mic_service.allocate()
    print("   HighestPriority ->", chosen.id, "(điểm cao nhất", chosen.get_default_priority_score(), ")")
 
    print("\n9. Cấp phát khi không có ứng viên phù hợp")
    expect_error("Điều hòa cho phòng Z999",
                 lambda: ac_service.allocate(lambda d: d.is_compatible_with("Z999")),
                 NoSuitableItemException)
    mic_service.allocate()                                     # lấy nốt micro còn sẵn sàng cuối cùng
    expect_error("Micro khi đã hết thiết bị sẵn sàng",
                 lambda: mic_service.allocate(),
                 NoSuitableItemException)
 
    print("\n10. Thiết bị được chọn chuyển sang Borrowed")
    print(f"   {selected.id}: {selected.status.value} | {selected_ac.id}: {selected_ac.status.value}")
    expect_error("Mượn lại thiết bị đang Borrowed", selected.borrow, DeviceNotReadyException)
    expect_error("Trả thiết bị đang Available", p2.return_device, DeviceNotReadyException)
 
    print("\n11. Cùng một lớp InMemoryRepository dùng cho nhiều loại thiết bị")
    for repo in (projector_repo, ac_repo, mic_repo):
        print(f"   {type(repo).__name__} chứa: {[d.id for d in repo.get_all()]}")
    all_devices = InMemoryRepository[TeachingDevice]()           # kho chung cho mọi loại thiết bị
    for d in projector_repo.get_all() + ac_repo.get_all() + mic_repo.get_all():
        all_devices.add(d)
    print("   Kho chung:", [d.id for d in all_devices.get_all()])
 
    # Kho không lộ collection nội bộ
    snapshot = projector_repo.get_all()
    snapshot.clear()
    print("   Xóa bản sao get_all() không ảnh hưởng kho:", len(projector_repo.get_all()), "phần tử vẫn còn")
 
 
if __name__ == "__main__":
    main()