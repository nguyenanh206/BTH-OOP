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
    def FindAll(self, condition: Callable[[T], bool]) -> List[T]: 
        pass

#Lớp InMemoryRepository<T>
class InMemoryRepository(IRepository[T], Generic[T]):
    def __init__(self):
        self._items: dict[str, T] = {}
 
    def add(self, item: T):
        if item is None:
            raise ValueError("Không chấp nhận phần tử null.")
        if item.id in self._items:
            raise DuplicateIdException(item.id)
        self._items[item.id] = item
 
    def remove(self, itemId: str) -> bool:
        if itemId in self._items:
            del self._items[itemId]
            return True
        return False
      
 
    def FindById(self, itemId: str) -> Optional[T]:
        return self._items.get(itemId)
 
    def GetAll(self) -> List[T]:
        return list(self._items.values())               
 
    def FindAll(self, condition: Callable[[T], bool]) -> List[T]:
        return  [item for item in self._items.values() if condition(item)]

# --------------------------------------------
# CHIẾN LƯỢC LỰA CHỌN (generic + đa hình)
# --------------------------------------------

#Interface chiến lược
class ISelectionStrategy(ABC, Generic[T]):
    @abstractmethod
    def select(self, candidates: List[T]) -> T:
        pass
 
# Các chiến lược bắt buộc 
class HighestPriorityStrategy(ISelectionStrategy[T], Generic[T]):
    def __init__(self, scoreSelector: Callable[[T], float]):
        if scoreSelector is None:
            raise ValueError("score_selector không được null.")
        self._scoreSelector = scoreSelector
 
    def select(self, candidates: List[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        return max(candidates, key=self._scoreSelector)  
 
 
class FirstAvailableStrategy(ISelectionStrategy[T], Generic[T]):
    def select(self, candidates: List[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        return candidates[0]
 
 
# ------------------------------------------
# DỊCH VỤ CẤP PHÁT TỔNG QUÁT
# ------------------------------------------
D = TypeVar("D", bound=TeachingDevice)     # where T : TeachingDevice
 
 
class AllocationService(Generic[D]):
    def __init__(self, repository: IRepository[D], strategy: ISelectionStrategy[D]):
        if repository is None or strategy is None:
            raise ValueError("repository và strategy không được null.")
        self._repository = repository
        self._strategy = strategy
 
    def ChangeStrategy(self, newStrategy: ISelectionStrategy[D]) -> None:
        if newStrategy is None:
            raise ValueError("Chiến lược mới không được null.")
        self._strategy = newStrategy
 
    def Allocate(self, additionalCondition: Optional[Callable[[D], bool]] = None) -> D:
        # lấy từ repository, chỉ giữ thiết bị sẵn sàng (đa hình qua is_ready_for_use)
        candidates = self._repository.FindAll(lambda d: d.IsReadyForUse())
        # áp dụng điều kiện bổ sung nếu có
        if additionalCondition is not None:
            candidates = [d for d in candidates if additionalCondition(d)]
        # chọn bằng chiến lược hiện tại (không biết chiến lược cụ thể là gì)
        selected = self._strategy.select(candidates)
        # cấp phát: nếu borrow() lỗi thì chưa có gì thay đổi
        selected.Borrow()
        return selected
 
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
 
    projectorRepo = InMemoryRepository[ProjectorRemote]()
    acRepo = InMemoryRepository[AirConditionerRemote]()
    micRepo = InMemoryRepository[WirelessMicrophone]()
 
    print("1. Thêm thiết bị vào repository")
    for d in (p1, p2, p3):
        projectorRepo.add(d)
    for d in (a1, a2):
        acRepo.add(d)
    for d in (m2, m1, m3):          # MIC02 (điểm thấp hơn) đứng trước MIC01 để thấy rõ khác biệt giữa hai chiến lược
        micRepo.add(d)
    print(f"   Máy chiếu: {len(projectorRepo.GetAll())}, điều hòa: {len(acRepo.GetAll())}, "
          f"micro: {len(micRepo.GetAll())}")
 
    print("\n2. Thêm hai thiết bị trùng mã")
    ExpectError("Thêm lại PJ01",
                 lambda: projectorRepo.add(ProjectorRemote("PJ01", "Trùng", "Kho A", 70)),
                 DuplicateIdException)
 
    print("\n3. Tìm thiết bị theo mã")
    print("   MIC02 ->", micRepo.FindById("MIC02"))
    print("   XXX   ->", micRepo.FindById("XXX"))
 
    print("\n4. Lọc các thiết bị sẵn sàng")
    print("   Micro sẵn sàng:", [d.id for d in micRepo.FindAll(lambda d: d.IsReadyForUse())])
    print("   Máy chiếu sẵn sàng:", [d.id for d in projectorRepo.FindAll(lambda d: d.IsReadyForUse())])
 
    print("\n5. Chọn điều khiển máy chiếu có điểm cao nhất")
    projectorService = AllocationService[ProjectorRemote](
        projectorRepo,
        HighestPriorityStrategy[ProjectorRemote](lambda d: d.GetDefaultPriorityScore()))
    selected = projectorService.Allocate(lambda d: True)
    print("   Được chọn:", selected)
 
    print("\n6. Chọn điều khiển điều hòa tương thích phòng A203")
    acService = AllocationService[AirConditionerRemote](
        acRepo, HighestPriorityStrategy[AirConditionerRemote](lambda d: d.GetDefaultPriorityScore()))
    selectedAc = acService.Allocate(lambda d: d.IsCompatibleWith("A203"))
    print("   Được chọn:", selectedAc)
 
    print("\n7. Chọn micro đầu tiên sẵn sàng")
    micService = AllocationService[WirelessMicrophone](micRepo, FirstAvailableStrategy[WirelessMicrophone]())
    firstMic = micService.Allocate()
    print("   Được chọn:", firstMic)
 
    print("\n8. Đổi chiến lược trong thời gian chạy")
    firstMic.Return()                                  # trả MIC01 về kho
    print("   Sau khi trả:", firstMic.status.value)
    chosen = micService.Allocate()
    print("   FirstAvailable  ->", chosen.id, "(đứng đầu danh sách, điểm", chosen.GetDefaultPriorityScore(), ")")
    chosen.Return()
    micService.ChangeStrategy(HighestPriorityStrategy[WirelessMicrophone](lambda d: d.GetDefaultPriorityScore()))
    chosen = micService.Allocate()
    print("   HighestPriority ->", chosen.id, "(điểm cao nhất", chosen.GetDefaultPriorityScore(), ")")
 
    print("\n9. Cấp phát khi không có ứng viên phù hợp")
    ExpectError("Điều hòa cho phòng Z999",
                 lambda: acService.Allocate(lambda d: d.IsCompatibleWith("Z999")),
                 NoSuitableItemException)
    micService.Allocate()                                     # lấy nốt micro còn sẵn sàng cuối cùng
    ExpectError("Micro khi đã hết thiết bị sẵn sàng",
                 lambda: micService.Allocate(),
                 NoSuitableItemException)
 
    print("\n10. Thiết bị được chọn chuyển sang Borrowed")
    print(f"   {selected.id}: {selected.status.value} | {selectedAc.id}: {selectedAc.status.value}")
    ExpectError("Mượn lại thiết bị đang Borrowed", selected.Borrow, DeviceNotReadyException)
    ExpectError("Trả thiết bị đang Available", p2.Return, DeviceNotReadyException)
 
    print("\n11. Cùng một lớp InMemoryRepository dùng cho nhiều loại thiết bị")
    for repo in (projectorRepo, acRepo, micRepo):
        print(f"   {type(repo).__name__} chứa: {[d.id for d in repo.GetAll()]}")
    allDevices = InMemoryRepository[TeachingDevice]()           # kho chung cho mọi loại thiết bị
    for d in projectorRepo.GetAll() + acRepo.GetAll() + micRepo.GetAll():
        allDevices.add(d)
    print("   Kho chung:", [d.id for d in allDevices.GetAll()])
 
    # Kho không lộ collection nội bộ
    snapshot = projectorRepo.GetAll()
    snapshot.clear()
    print("   Xóa bản sao GetAll() không ảnh hưởng kho:", len(projectorRepo.GetAll()), "phần tử vẫn còn")
 
 
if __name__ == "__main__":
    main()
