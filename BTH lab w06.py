# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# Enum cho trạng thái thiết bị
class DeviceStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    UNDER_MAINTENANCE = 3


#---------------------------
# NGOẠI LỆ NGHIỆP VỤ
#---------------------------

# Ngoại lệ cơ sở
class BorrowingException(Exception):
    def __init__(self, message: str, innerException: Exception = None):
        super().__init__(message)
        self.innerException = innerException

#các ngoại lệ dẫn xuất bắt buộc

# Phát sinh khi thiết bị không ở trạng thái Available
class DeviceUnavailableException(BorrowingException):
    def __init__(self, deviceId: str, currentStatus: DeviceStatus):
        super().__init__(f"Thiết bị {deviceId} không sẵn sàng (Trạng thái hiện tại: {currentStatus.name}).")
        self.deviceId = deviceId
        self.currentStatus = currentStatus

#Phát sinh khi người mượn đã đạt số thiết bị tối đa.
class BorrowLimitExceededException(BorrowingException):
    def __init__(self, borrowerId: str, maximumDevices: int):
        super().__init__(f"Người mượn {borrowerId} đã vượt quá giới hạn cho phép ({maximumDevices} thiết bị).")
        self.borrowerId = borrowerId
        self.maximumDevices = maximumDevices

#Phát sinh khi thời hạn/số ngày mượn không hợp lệ
class InvalidBorrowPeriodException(BorrowingException):
    def __init__(self, id: str, requestedDays: int, maxDays: int):
        super().__init__(f"Số ngày mượn {requestedDays} không hợp lệ hoặc vượt quá giới hạn tối đa {maxDays} của thiết bị {id}.")
        self.id = id
        self.requestedDays = requestedDays
        self.maxDays = maxDays

#Phát sinh khi cùng một thiết bị đã tồn tại trong phiếu
class DuplicateDeviceException(BorrowingException):
    def __init__(self, id: str):
        super().__init__(f"Thiết bị {id} đã tồn tại trong phiếu mượn.")
        self.id = id

#Phát sinh khi yêu cầu trả một thiết bị không thuộc phiếu
class DeviceNotInSlipException(BorrowingException):
    def __init__(self, id: str):
        super().__init__(f"Thiết bị {id} không thuộc phiếu mượn này.")
        self.id = id

#Phát sinh khi thiết bị trong phiếu đã được trả trước đó
class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, id: str):
        super().__init__(f"Thiết bị {id} đã được trả trước đó.")
        self.id = id      

# Ngoại lệ bổ sung: ngày trả không hợp lệ (để catch riêng, rõ nghĩa hơn BorrowingException chung)
class InvalidReturnDateException(BorrowingException):
    def __init__(self, id: str, borrowedDate: datetime.datetime, returnedDate: datetime.datetime):
        super().__init__(f"Ngày trả {returnedDate} của thiết bị {id} trước ngày mượn {borrowedDate}.")
        self.id = id
#---------------------------
# Lớp trừu tượng 
#---------------------------

# DEVICE

class Device(ABC):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, maxBorrowDays: int):
        if not id or not id.strip():
            raise ValueError("Mã thiết bị không được rỗng")
        if purchasePrice <= 0:
            raise ValueError("Giá mua phải lớn hơn 0")
        
        currentYear = datetime.datetime.now().year
        if yearInUse > currentYear:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại")

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

    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value

    @property
    def maxBorrowDays(self) -> int:
        return self._maxBorrowDays
    
# Phương thức trừu tượng tính chi phí bảo trì dự kiến trong một năm.
#   @abstractmethod
 #   def CalculateAnnualMaintenanceCost(self) -> float:
  #      pass

    def __str__(self) -> str:
        currentYear = datetime.datetime.now().year
        age = currentYear - self._yearInUse
        return (f"Mã thiết bị: {self._id} | Tên thiết bị: {self._name} | "
                f"Năm đưa vào sử dụng: {self._yearInUse} | "
                f"Giá mua: {self._purchasePrice: ,.0f} | Trạng thái: {self._status.name}")

#----------------------------   
# CÁC LỚP DẪN XUẤT
#-----------------------------

# AIR CONDITIONER REMOTE CONTROL
class AirConditionerRemote(Device):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus = DeviceStatus.AVAILABLE, maxBorrowDays: int = 3):
        super().__init__(id, name, yearInUse, purchasePrice, status, maxBorrowDays)
        
    # Tính chi phí bảo trì
    #    def CalculateAnnualMaintenanceCost(self) -> float:
    #       return self.purchasePrice * 

# MICRO
class Micro(Device):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus = DeviceStatus.AVAILABLE, maxBorrowDays: int = 1):
            super().__init__(id, name, yearInUse, purchasePrice, status, maxBorrowDays)
    # Tính chi phí bảo trì
    #    def CalculateAnnualMaintenanceCost(self) -> float:
    #           cost = self.purchasePrice *


# PROJECTOR REMOTE
class ProjectorRemote(Device):
   def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus = DeviceStatus.AVAILABLE, maxBorrowDays: int = 5):
           super().__init__(id, name, yearInUse, purchasePrice, status, maxBorrowDays)

    # Tính chi phí bảo trì
   # def CalculateAnnualMaintenanceCost(self) -> float:
    #        cost = self.purchasePrice *


#-------------------------------
# KẾT TẬP
#-------------------------------
# CLASSROOM
class ClassRoom:
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


    def GetDevicesRequiringMaintenance(self) -> list[Device]:
        result = []

        for dv in self.devices:
            age = datetime.datetime.now().year - dv._yearInUse
            if dv.status == DeviceStatus.UNDER_MAINTENANCE or age > 5:
                result.append(dv)
        return result

#---------------------------------
# INTERFACE + 2 lớp thực thi
#---------------------------------
#IBORROWER

class IBorrower(ABC):
    @property
    @abstractmethod
    def borrowerId(self) -> str:
        pass

    @property
    @abstractmethod
    def fullName(self) -> str:
        pass

    @abstractmethod
    def GetMaximumDevices(self) -> int:
        pass

class Lecturer(IBorrower):
    def __init__(self, borrowerId: str, fullName: str):
        self._borrowerId = borrowerId
        self._fullName = fullName
    @property
    def borrowerId(self) -> str:
        return self._borrowerId

    @property
    def fullName(self) -> str:
        return self._fullName

    def GetMaximumDevices(self) -> int:
        return 3

class TeachingAssistant(IBorrower):
    def __init__(self, borrowerId: str, fullName: str):
        self._borrowerId = borrowerId
        self._fullName = fullName
    @property
    def borrowerId(self) -> str:
        return self._borrowerId

    @property
    def fullName(self) -> str:
        return self._fullName

    def GetMaximumDevices(self) -> int:
        return 2
    
# BORROWITEM

class BorrowItem:
    def __init__(self, device: Device, borrowedDate: datetime.datetime, dueDate: datetime.datetime, fromPeriod: int, toPeriod: int):
        if device is None:
            raise ValueError("device không được null.")
        if dueDate < borrowedDate:
            raise ValueError("DueDate phải sau hoặc bằng BorrowedDate.")
        if fromPeriod > toPeriod:
            raise ValueError("Tiết bắt đầu không được lớn hơn tiết kết thúc.")

        self._device = device
        self._borrowedDate = borrowedDate
        self._dueDate = dueDate
        self._fromPeriod = fromPeriod
        self._toPeriod = toPeriod
        self._borrower: IBorrower 
        self._ReturnedDate = None
        self._IsReturned = False

    @property
    def device(self) -> Device:
        return self._device

    @property
    def borrowedDate(self) -> datetime.datetime:
        return self._borrowedDate

    @property
    def dueDate(self) -> datetime.datetime:
        return self._dueDate

    @property
    def ReturnedDate(self) -> datetime.datetime | None:
        return self._ReturnedDate

    @property
    def IsReturned(self) -> bool:
        return self._IsReturned

    def Return(self, ReturnedDate: datetime.datetime):
        if self._IsReturned:
            raise DeviceAlreadyReturnedException(self._device.id)
        if ReturnedDate < self._borrowedDate:
            raise InvalidReturnDateException(self._device.id, self._borrowedDate, ReturnedDate)
        
        self._ReturnedDate = ReturnedDate
        self._IsReturned = True

    def calculate_late_fee(self) -> float:
        lateDays = max(0, (self._ReturnedDate.date() - self._dueDate.date()).days)
        return lateDays * 10000

# BORROWINGSLIP

class BorrowingSlip:
    def __init__(self, slipId: str, borrower: IBorrower, teachingRoom: str, borrowedDate: datetime.datetime):
        if not slipId or not slipId.strip():
            raise ValueError ("Thông tin slipId không hợp lệ!")
        if  borrower is None:
            raise ValueError ("Thông tin borrower không được rỗng")
        if not teachingRoom or not teachingRoom.strip():
            raise ValueError ("Thông tin teachingRoom không hợp lệ!")

        self._slipId = slipId
        self._borrower = borrower
        self._teachingRoom = teachingRoom
        self._borrowedDate = borrowedDate
        self._items: list[BorrowItem] = []

    @property
    def slipId(self) -> str:
        return self._slipId 

    @property
    def borrower(self) -> IBorrower:
        return self._borrower

    @property
    def teachingRoom(self) -> str:
        return self._teachingRoom

    @property
    def borrowedDate(self) -> datetime.datetime:
        return self._borrowedDate

    @property
    def items(self) -> list[BorrowItem]:
        return self._items
    
# Thêm thiết bị

    def AddDevice(self, device: Device, borrowDays: int, fromPeriod: int = 1, toPeriod: int = 5):
        if device is None:
            raise ValueError("Thiết bị không được null")
        if borrowDays <= 0:
            raise InvalidBorrowPeriodException(device.id, borrowDays, device.maxBorrowDays)
        if borrowDays > device.maxBorrowDays:
            raise InvalidBorrowPeriodException(device.id, borrowDays, device.maxBorrowDays)
        if any(item.device.id == device.id for item in self._items):
            raise DuplicateDeviceException(device.id)
        if len(self._items) >= self._borrower.GetMaximumDevices():
            raise BorrowLimitExceededException(self._borrower.borrowerId, self._borrower.GetMaximumDevices())
        if device.status != DeviceStatus.AVAILABLE:
            raise DeviceUnavailableException(device.id, device.status)

        dueDate = self._borrowedDate + datetime.timedelta(days=borrowDays)
        item = BorrowItem(device, self._borrowedDate, dueDate, fromPeriod, toPeriod)
        
        device.status = DeviceStatus.BORROWED
        self._items.append(item)

#Trả thiết bị
    def ReturnDevice(self, id: str, returnedDate: datetime.datetime) -> float:
        if not id or not id.strip():
            raise ValueError("Mã thiết bị không được rỗng.")
            
        targetItem = None
        for item in self._items:
            if item.device.id == id:
                targetItem = item
                break
                
        if not targetItem:
            raise DeviceNotInSlipException(id)
            
        targetItem.Return(returnedDate)
        targetItem.device.status = DeviceStatus.AVAILABLE
        return targetItem.calculate_late_fee()

# ---------------------------
# HÀM HỖ TRỢ HIỂN THỊ
# ---------------------------
def PrintSlipReport(slip: BorrowingSlip, asOf: datetime.datetime):
    print(f"Phiếu {slip.slipId} | {slip.borrower.fullName} | {slip.teachingRoom} | mượn {slip.borrowedDate:%d/%m/%Y}")
    for item in slip.items:
        if not item.IsReturned:
            tt = "QUÁ HẠN - CHƯA TRẢ" if asOf.date() > item.dueDate.date() else "Chưa trả"
        elif item.calculate_late_fee() > 0:
            tt = f"TRẢ MUỘN {(item.ReturnedDate.date() - item.dueDate.date()).days} ngày (phạt {item.calculate_late_fee():,.0f})"
        else:
            tt = "Trả đúng hạn"
        print(f"   - {item.device.id:<6} hạn {item.dueDate:%d/%m} | {tt}")
    print(f"   => Tổng phí trả muộn: {sum(item.calculate_late_fee() for item in slip.items if item.IsReturned):,.0f} VNĐ")
 
 
def RunCase(title: str, action, device: Device = None):
    """Chạy một tình huống, bắt ngoại lệ, và kiểm tra trạng thái thiết bị còn nhất quán."""
    print(f"\n[{title}]")
    before = device.status if device else None
    try:
        action()
        print("   !! Không có ngoại lệ (không mong đợi)")
    except BorrowingException as e:
        print(f"   Bắt {type(e).__name__}: {e}")
    except ValueError as e:
        print(f"   Bắt lỗi: {e}")
    finally:
        if device is not None:
            print(f"   (Kiểm tra) {device.id}: {before.name} -> {device.status.name}")
 
 
if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ HỆ THỐNG MƯỢN THIẾT BỊ ===")
    today = datetime.datetime(2026, 10, 15)
 
    # Khởi tạo dữ liệu
    lecturer = Lecturer("GV01", "TS.HTTB")
    ta = TeachingAssistant("TA01", "ThS.BTĐ")
 
    acRemote = AirConditionerRemote("AC01", "Panasonic Remote", 2023, 500000, DeviceStatus.AVAILABLE)
    mic = Micro("MIC01", "Micro không dây Sony", 2022, 1200000, DeviceStatus.AVAILABLE)
    projectorRemote = ProjectorRemote("PRJ01", "Epson Remote", 2021, 800000, DeviceStatus.AVAILABLE)
    brokenAc = AirConditionerRemote("AC02", "Điều hòa Daikin hỏng", 2020, 500000, DeviceStatus.UNDER_MAINTENANCE)
 
    # Phòng học (kết tập)
    room = ClassRoom("P101", "Phòng 101", 60)
    for d in (acRemote, mic, projectorRemote, brokenAc):
        room.AddDevice(d)
    print("Thiết bị cần bảo trì:", [d.id for d in room.GetDevicesRequiringMaintenance()])
 
    # 1. Luồng thành công
    print("\n--- 1. Kiểm thử luồng thành công ---")
    slip = BorrowingSlip("SLIP01", lecturer, "Phòng P101", today)
    try:
        slip.AddDevice(projectorRemote, borrowDays=3)
        slip.AddDevice(mic, borrowDays=1)
        print(f"Tạo phiếu mượn thành công cho {lecturer.fullName} với {len(slip.items)} thiết bị.")
 
        # Trả máy chiếu đúng hạn (hạn 18/10)
        fee1 = slip.ReturnDevice("PRJ01", today + datetime.timedelta(days=3))
        print(f"Đã trả PRJ01 đúng hạn. Phí trễ: {fee1:,.0f} VNĐ")
 
        # Trả micro muộn 2 ngày (hạn 16/10 -> trả 18/10)
        fee2 = slip.ReturnDevice("MIC01", today + datetime.timedelta(days=3))
        print(f"Đã trả MIC01 muộn 2 ngày. Phí trễ: {fee2:,.0f} VNĐ")
    except BorrowingException as e:
        print(f"Lỗi nghiệp vụ: {e}")
    finally:
        # Mượn thêm 1 thiết bị chưa trả để minh họa danh sách "chưa trả / quá hạn"
        slip.AddDevice(acRemote, borrowDays=2)
        PrintSlipReport(slip, asOf=today + datetime.timedelta(days=5))
 
    # 2. Luồng phát sinh ngoại lệ
    print("\n--- 2. Kiểm thử các tình huống ngoại lệ ---")
 
    # Tình huống 1: Mượn điều hòa đang UnderMaintenance
    slip2 = BorrowingSlip("SLIP02", lecturer, "Phòng P102", today)
    RunCase("Test 1: Mượn thiết bị đang bảo trì",
            lambda: slip2.AddDevice(brokenAc, borrowDays=2), brokenAc)
 
    # Tình huống 2: Trợ giảng mượn thiết bị thứ 3
    slip3 = BorrowingSlip("SLIP03", ta, "Phòng P103", today)
    d1 = AirConditionerRemote("AC10", "Remote 1", 2023, 100000)
    d2 = AirConditionerRemote("AC11", "Remote 2", 2023, 100000)
    d3 = AirConditionerRemote("AC12", "Remote 3", 2023, 100000)
    slip3.AddDevice(d1, 1)
    slip3.AddDevice(d2, 1)
    RunCase("Test 2: Trợ giảng mượn thiết bị thứ 3",
            lambda: slip3.AddDevice(d3, 1), d3)
    print(f"   Số item trong phiếu vẫn là: {len(slip3.items)}")
 
    # Tình huống 3: Thêm cùng một micro hai lần
    mic2 = Micro("MIC02", "Micro 02", 2024, 1500000)
    slip4 = BorrowingSlip("SLIP04", lecturer, "Phòng P104", today)
    slip4.AddDevice(mic2, 1)
    RunCase("Test 3: Thêm trùng thiết bị vào phiếu",
            lambda: slip4.AddDevice(mic2, 1), mic2)
 
    # Tình huống 4: Mượn micro 3 ngày (giới hạn 1 ngày) - dùng micro mới, còn Available
    mic3 = Micro("MIC03", "Micro 03", 2024, 1500000)
    slip5 = BorrowingSlip("SLIP05", lecturer, "Phòng P105", today)
    RunCase("Test 4: Mượn quá thời hạn cho phép của thiết bị",
            lambda: slip5.AddDevice(mic3, borrowDays=3), mic3)
 
    # Tình huống 5: Trả thiết bị không thuộc phiếu
    slip6 = BorrowingSlip("SLIP06", lecturer, "Phòng P106", today)
    RunCase("Test 5: Trả thiết bị không có trong phiếu",
            lambda: slip6.ReturnDevice("AC99", today))
 
    # Tình huống 6: Trả cùng một thiết bị hai lần
    prj2 = ProjectorRemote("PRJ02", "ĐK máy chiếu 02", 2024, 400000)
    slip7 = BorrowingSlip("SLIP07", lecturer, "Phòng P107", today)
    slip7.AddDevice(prj2, 2)
    slip7.ReturnDevice("PRJ02", today + datetime.timedelta(days=1))
    RunCase("Test 6: Trả cùng một thiết bị hai lần",
            lambda: slip7.ReturnDevice("PRJ02", today + datetime.timedelta(days=1)), prj2)
 
    # Tình huống 7: Ngày trả trước ngày mượn
    prj3 = ProjectorRemote("PRJ03", "ĐK máy chiếu 03", 2024, 400000)
    slip8 = BorrowingSlip("SLIP08", lecturer, "Phòng P108", today)
    slip8.AddDevice(prj3, 2)
    RunCase("Test 7: Ngày trả trước ngày mượn",
            lambda: slip8.ReturnDevice("PRJ03", today - datetime.timedelta(days=1)), prj3)
    print(f"   Thiết bị vẫn đang được mượn? {not slip8.items[0].IsReturned}")
 
    print("\n=== KẾT THÚC KIỂM THỬ ===")
