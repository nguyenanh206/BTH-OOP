# Họ tên: Nguyên Hà Anh
# MSSV: 202418833

from Employee import Employee

class ProjectTeam:
 
    def __init__(self, project_code, project_name, leader=None):
        self._project_code = project_code
        self._project_name = project_name
        self._leader = None      # liên kết không sở hữu tới trưởng nhóm
        self._members = []       # danh sách liên kết không sở hữu tới thành viên
        if leader is not None:
            self._require_employee(leader)
            self._members.append(leader)   # trưởng nhóm tự động là thành viên
            self._leader = leader
 
    # ---------------------------- Getter ----------------------------
    @property
    def project_code(self):
        return self._project_code
 
    @property
    def project_name(self):
        return self._project_name
 
    @property
    def leader(self):
        return self._leader
 
    @property
    def members(self):
        return tuple(self._members)
 
    def __len__(self):
        return len(self._members)
 
    @staticmethod
    def _require_employee(employee):
        if not isinstance(employee, Employee):
            raise TypeError(f"Cần đối tượng Employee, nhận được {type(employee).__name__}")
 
    def _find_index(self, employee_id):
        employee_id = str(employee_id)
        for index, member in enumerate(self._members):
            if member.id == employee_id:
                return index
        return -1
 
    def check_invariants(self):
        ids = [member.id for member in self._members]
        no_duplicate_id = len(ids) == len(set(ids))
        no_duplicate_object = len({id(m) for m in self._members}) == len(self._members)
        leader_is_member = (self._leader is None
                            or any(m is self._leader for m in self._members))
        return no_duplicate_id and no_duplicate_object and leader_is_member
 
    def add_member(self, employee, make_leader=False):
        self._require_employee(employee)
        if not isinstance(make_leader, bool):
            raise TypeError("make_leader phải là bool (True/False)")
        if self._find_index(employee.id) >= 0:
            return False
        self._members.append(employee)
        if make_leader:
            self._leader = employee
        assert self.check_invariants()
        return True
 
    def remove_member(self, employee_id):
        index = self._find_index(employee_id)
        if index < 0:
            return False
        if self._members[index] is self._leader:
            return False       # không cho xóa trưởng nhóm khi chưa có người thay thế
        del self._members[index]
        assert self.check_invariants()
        return True
 
    def change_leader(self, employee):
        self._require_employee(employee)
        index = self._find_index(employee.id)
        if index >= 0:
            if self._members[index] is not employee:
                return False
        else:
            self._members.append(employee)
        self._leader = employee      # trưởng nhóm cũ vẫn giữ nguyên tư cách thành viên
        assert self.check_invariants()
        return True
 
    def contains(self, employee_id):
        return self._find_index(employee_id) >= 0
 
    def calculate_total_monthly_cost(self):
        return sum(member.calculate_monthly_cost() for member in self._members)
 
    def display_team(self):
        print(f"=== Nhóm dự án {self._project_code} - {self._project_name} ===")
        if self._leader is None:
            print("Trưởng nhóm: (chưa có)")
        else:
            print(f"Trưởng nhóm: {self._leader.full_name} ({self._leader.id})")
        print(f"Số thành viên: {len(self._members)}")
        for number, member in enumerate(self._members, start=1):
            marker = "(Trưởng nhóm) " if member is self._leader else ""
            print(f"  {number}. {marker}", end="")
            member.display_info()
        print(f"Tổng chi phí hằng tháng: {self.calculate_total_monthly_cost():,.0f}")
 
    def __del__(self):
        members = getattr(self, "_members", None)
        if members is not None:
            print(f"[ProjectTeam] Hủy nhóm {self._project_code} "
                  f"(chỉ giải phóng danh sách liên kết, không hủy nhân sự)")
            members.clear()
        self._leader = None