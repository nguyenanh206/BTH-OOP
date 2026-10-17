# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# Enum cho trạng thái thiết bị
class DeviceStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    UNDERMAINTANCE = 3


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
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, maxBorrowDays: int):
        super().__init__(id, name, yearInUse, purchasePrice, status, maxBorrowDays)
        
    # Tính chi phí bảo trì
    #    def CalculateAnnualMaintenanceCost(self) -> float:
    #       return self.purchasePrice * 

# MICRO
class Micro(Device):
    def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, maxBorrowDays: int):
            super().__init__(id, name, yearInUse, purchasePrice, status, maxBorrowDays)
    # Tính chi phí bảo trì
    #    def CalculateAnnualMaintenanceCost(self) -> float:
    #           cost = self.purchasePrice *


# PROJECTOR REMOTE
class ProjectorRemote(Device):
   def __init__(self, id: str, name: str, yearInUse: int, purchasePrice: float, status: DeviceStatus, maxBorrowDays: int):
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

    # Sử dụng tính đa hình
    def CalculateAnnualMaintenanceCost(self) -> float:
        totalCost = 0.0
        for dv in self.devices:
            totalCost += dv.CalculateAnnualMaintenanceCost()
        return totalCost

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
    def __init__(self, borrowerId: str, fullName: int):
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
    def __init__(self, borrowerId: str, fullName: int):
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
    
# BORROWITEM

class BorrowItem:
    def __init__(self, device: Device, borrowedDate: datetime.datetime, dueDate: datetime.datetime, fromPeriod: int, toPeriod: int):
        if device is None:
            raise ValueError("device không được null.")
        if dueDate < borrowedDate:
            raise ValueError("DueDate phải sau hoặc bằng BorrowedDate[cite: 8].")
        if fromPeriod > toPeriod:
            raise ValueError("Tiết bắt đầu không được lớn hơn tiết kết thúc[cite: 8].")

        self._device = device
        self._borrowedDate = borrowedDate
        self._dueDate = dueDate
        self._fromPeriod = fromPeriod
        self._toPeriod = toPeriod
        self. borrower: IBorrower 
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
            raise DeviceAlreadyReturnedException(self._device.Id)
        if ReturnedDate < self._borrowed_date:
            raise BorrowingException("Ngày trả không được trước ngày mượn[cite: 8].")
        
        self._ReturnedDate = ReturnedDate
        self._IsReturned = True

# BORROWINGSLIP

class BorrowingSlip:
    def __init__(self, slipId: str, borrower: IBorrower, teachingRoom: str, borrowedDate: datetime.datetime):
        if not slipId or not slipId.strip():
            raise ValueError ("Thông tin slipId không hợp lệ!")
        if not borrower is None:
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
            raise ValueError("Số ngày mượn phải > 0.")
        if borrowDays > device.maxBorrowDays:
            raise InvalidBorrowPeriodException(device.id, borrowDays, device.maxBorrowDays)
        if any(item.device.id == device.id for item in self._items):
            raise DuplicateDeviceException(device.id)
        if len(self._items) >= self._borrower.GetMaximumDevices():
            raise BorrowLimitExceededException(self._borrower.id, self._borrower.GetMaximumDevices())
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
            
        targetItem.returnItem(returnedDate)
        targetItem.device.status = DeviceStatus.AVAILABLE
        return targetItem.calculate_late_fee()
    def calculate_total_late_fee(self) -> float:
        return sum(item.calculate_late_fee() for item in self._items if item.is_returned)


if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ HỆ THỐNG MƯỢN THIẾT BỊ ===")
    today = datetime.datetime.now()

    # Khởi tạo dữ liệu
    lecturer = Lecturer("GV01", "Dr. Nguyen Van A")
    ta = TA = TeachingAssistant("TA01", "Tran Thi B")

    acRemote = AirConditionerRemote("AC01", "Điều hòa Panasonic Remote", 2023, 500000, DeviceStatus.AVAILABLE)
    mic = Micro("MIC01", "Micro không dây Sony", 2022, 1200000, DeviceStatus.AVAILABLE)
    projectorRemote = ProjectorRemote("PRJ01", "Máy chiếu Epson Remote", 2021, 800000, DeviceStatus.AVAILABLE)
    brokenAc = AirConditionerRemote("AC02", "Điều hòa Daikin hỏng", 2020, 500000, DeviceStatus.UNDER_MAINTENANCE)

    # 1. Luồng thành công
    print("\n--- 1. Kiểm thử luồng thành công ---")
    try:
        slip = BorrowingSlip("SLIP01", lecturer, "Phòng P101", today)
        slip.AddDevice(projectorRemote, borrowDays=3)
        slip.AddDevice(mic, borrowDays=1)
        print(f"Tạo phiếu mượn thành công cho {lecturer.fullName} với {len(slip.items)} thiết bị.")

        # Trả máy chiếu đúng hạn
        fee1 = slip.ReturnDevice("PRJ01", today)
        print(f"Đã trả máy chiếu PRJ01 đúng hạn. Phí trễ: {fee1:,.0f} VNĐ")

        # Trả micro muộn 2 ngày
        lateDate = today + datetime.timedelta(days=3)
        fee2 = slip.ReturnDevice("MIC01", lateDate)
        print(f"Đã trả micro MIC01 muộn 2 ngày. Phí trễ: {fee2:,.0f} VNĐ")
    except BorrowingException as e:
        print(f"Lỗi nghiệp vụ: {e}")

    # 2. Luồng phát sinh ngoại lệ
    print("\n--- 2. Kiểm thử các tình huống ngoại lệ ---")
    
    # Tình huống 1: Mượn điều hòa đang UnderMaintenance
    print("\n[Test 1] Mượn thiết bị đang bảo trì:")
    try:
        slip2 = BorrowingSlip("SLIP02", lecturer, "Phòng P102", today)
        slip2.add_device(brokenAc, borrowDays=2)
    except DeviceUnavailableException as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    # Tình huống 2: Trợ giảng mượn thiết bị thứ 3 (vượt giới hạn 2 thiết bị của TA)
    print("\n[Test 2] Trợ giảng mượn vượt quá giới hạn:")
    try:
        slip3 = BorrowingSlip("SLIP03", ta, "Phòng P103", today)
        d1 = AirConditionerRemote("AC10", "Remote 1", 2023, 100000, DeviceStatus.AVAILABLE)
        d2 = AirConditionerRemote("AC11", "Remote 2", 2023, 100000, DeviceStatus.AVAILABLE)
        d3 = AirConditionerRemote("AC12", "Remote 3", 2023, 100000, DeviceStatus.AVAILABLE)
        
        slip3.AddDevice(d1, 1)
        slip3.AddDevice(d2, 1)
        slip3.AddDevice(d3, 1)  # Sẽ ném ngoại lệ BorrowLimitExceededException
    except BorrowLimitExceededException as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    # Tình huống 3: Thêm cùng một micro hai lần
    print("\n[Test 3] Thêm trùng thiết bị vào phiếu:")
    try:
        slip4 = BorrowingSlip("SLIP04", lecturer, "Phòng P104", today)
        slip4.AddDevice(mic, 1)
        slip4.AddDevice(mic, 1)  # Sẽ ném ngoại lệ DuplicateDeviceException
    except DuplicateDeviceException as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    # Tình huống 4: Mượn micro quá giới hạn số ngày cho phép (Micro tối đa 1 ngày)
    print("\n[Test 4] Mượn quá thời hạn cho phép của thiết bị:")
    try:
        slip5 = BorrowingSlip("SLIP05", lecturer, "Phòng P105", today)
        slip5.AddDevice(mic, borrow_days=3)
    except InvalidBorrowPeriodException as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    # Tình huống 5: Trả thiết bị không thuộc phiếu
    print("\n[Test 5] Trả thiết bị không có trong phiếu:")
    try:
        slip6 = BorrowingSlip("SLIP06", lecturer, "Phòng P106", today)
        slip6.ReturnDevice("AC99", today)
    except DeviceNotInSlipException as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    print("\n=== KẾT THÚC KIỂM THỬ ===")
