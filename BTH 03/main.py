# Họ tên: Nguyễn Hà Anh
# MSSV: 202418833

import gc
import sys
 
from Employee import Employee
from projectTeam import ProjectTeam
from SofewareEngineer import SoftwareEngineer
 
 
def print_step(number, title):
    print(f"\n--- Bước {number}: {title} ---")
 
 
def expect_error(label, action, expected):
    try:
        action()
    except expected as error:
        print(f"  [OK] {label} -> {type(error).__name__}: {error}")
    else:
        print(f"  [LỖI] {label} -> không có ngoại lệ nào được ném!")
 
 
def check(label, condition):
    print(f"  [{'OK' if condition else 'LỖI'}] {label}")
 
 
def demo_second_team(shared_employee, extra_engineer):
    team2 = ProjectTeam("PRJ02", "Ứng dụng di động")
    team2.add_member(shared_employee)              # nhân sự đã thuộc nhóm thứ nhất
    team2.add_member(extra_engineer, True)         # đặt làm trưởng nhóm
    team2.display_team()
    print("  -> Kết thúc khối lệnh cục bộ, nhóm thứ hai sắp bị hủy...")
 
 
def run_required_scenario():
    print("=" * 70)
    print("PHẦN 1: KỊCH BẢN 15 BƯỚC THEO ĐỀ BÀI")
    print("=" * 70)
 
    print_step(1, "Tạo hai Employee bằng hai constructor khác nhau")
    print("Constructor mặc định (đối tượng tạm, bị hủy ngay sau dòng lệnh):")
    Employee().display_info()
    emp1 = Employee("E001", "Nguyễn Hà Anh")                # constructor 2 tham số
    emp2 = Employee("E002", "Nguyễn Thị Huyền Trang", 12_000_000)    # constructor 3 tham số
    emp1.display_info()
    emp2.display_info()
 
    print_step(2, "Tạo hai SoftwareEngineer bằng hai constructor khác nhau")
    eng1 = SoftwareEngineer("S001", "Nguyễn Trọng Hưng", "Python")
    eng2 = SoftwareEngineer("S002", "Nguyễn Thu Hà", 25_000_000, "C++", 5_000_000)
    eng1.display_info()
    eng2.display_info()
 
    print_step(3, "Tăng lương một nhân sự bằng số tiền cố định")
    print(f"Lương E001 trước: {emp1.base_salary:,.0f}")
    emp1.increase_salary(8_000_000)
    print(f"Lương E001 sau khi tăng 8,000,000: {emp1.base_salary:,.0f}")
 
    print_step(4, "Tăng lương một nhân sự khác theo phần trăm")
    print(f"Lương E002 trước: {emp2.base_salary:,.0f}")
    emp2.increase_salary(10, True)
    print(f"Lương E002 sau khi tăng 10%: {emp2.base_salary:,.0f}")
 
    print_step(5, "Tạo nhóm dự án không có trưởng nhóm")
    team1 = ProjectTeam("PRJ01", "Hệ thống quản lý nhân sự")
    print(f"Trưởng nhóm hiện tại: {team1.leader}, số thành viên: {len(team1)}")
 
    print_step(6, "Thêm một nhân sự vào nhóm bằng addMember(employee)")
    print(f"add_member(E001) -> {team1.add_member(emp1)}")
 
    print_step(7, "Thêm một kỹ sư bằng addMember(employee, True) để làm trưởng nhóm")
    print(f"add_member(S002, True) -> {team1.add_member(eng2, True)}")
    print(f"Trưởng nhóm: {team1.leader.full_name}")
    # Thêm hai thành viên nữa để các bước sau có dữ liệu phong phú hơn
    team1.add_member(emp2)
    team1.add_member(eng1)
 
    print_step(8, "Thử thêm lại một thành viên đã tồn tại")
    print(f"add_member(E001) lần 2 -> {team1.add_member(emp1)} (bị từ chối)")
    print(f"Số thành viên vẫn là {len(team1)}")
 
    print_step(9, "Hiển thị danh sách bằng lời gọi đa hình")
    team1.display_team()
 
    print_step(10, "Tính tổng chi phí nhân sự hằng tháng")
    expected = (emp1.calculate_monthly_cost() + emp2.calculate_monthly_cost()
                + eng1.calculate_monthly_cost() + eng2.calculate_monthly_cost())
    total = team1.calculate_total_monthly_cost()
    print(f"Tổng chi phí: {total:,.0f}")
    check("Khớp với tổng tính tay từng người", total == expected)
 
    print_step(11, "Thử xóa trưởng nhóm hiện tại")
    result = team1.remove_member("S002")
    print(f"remove_member('S002') -> {result} (bị từ chối vì là trưởng nhóm)")
    check("Trưởng nhóm vẫn là S002", team1.leader is eng2)
 
    print_step(12, "Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm")
    print(f"change_leader(E001) -> {team1.change_leader(emp1)}")
    print(f"remove_member('S002') -> {team1.remove_member('S002')}")
    team1.display_team()
    check("Các bất biến của nhóm vẫn thỏa", team1.check_invariants())
 
    print_step(13, "Tạo nhóm thứ hai với nhân sự đã có ở nhóm thứ nhất")
    print_step(14, "Hủy nhóm thứ hai bằng cách kết thúc khối lệnh cục bộ")
    demo_second_team(emp2, eng2)
    gc.collect()
 
    print_step(15, "Chứng minh nhân sự của nhóm thứ hai vẫn tồn tại sau khi nhóm bị hủy")
    emp2.display_info()
    eng2.display_info()
    check("E002 vẫn thuộc nhóm thứ nhất", team1.contains("E002"))
    check("S002 (từng là trưởng nhóm nhóm 2) vẫn truy cập được", eng2.full_name == "Phạm Thu Dung")
    return emp1, emp2, eng1, eng2, team1
 
 
def run_edge_cases(emp1, emp2, eng1, team1):
    print("\n" + "=" * 70)
    print("PHẦN 2: CÁC TRƯỜNG HỢP BIÊN")
    print("=" * 70)
 
    print("\n[Employee] Ràng buộc dữ liệu:")
    expect_error("Mã rỗng", lambda: Employee("", "An"), ValueError)
    expect_error("Mã chỉ có khoảng trắng", lambda: Employee("   ", "An"), ValueError)
    expect_error("Họ tên rỗng", lambda: Employee("E9", ""), ValueError)
    expect_error("Lương âm", lambda: Employee("E9", "An", -1), ValueError)
    expect_error("Lương NaN", lambda: Employee("E9", "An", float("nan")), ValueError)
    expect_error("Lương sai kiểu", lambda: Employee("E9", "An", "abc"), TypeError)
    zero = Employee("E0", "Lương không", 0)
    check("Lương = 0 là hợp lệ (biên dưới)", zero.base_salary == 0)
 
    print("\n[Employee] increase_salary:")
    expect_error("Tăng 0", lambda: emp1.increase_salary(0), ValueError)
    expect_error("Tăng số âm", lambda: emp1.increase_salary(-5), ValueError)
    expect_error("Tăng % âm", lambda: emp1.increase_salary(-10, True), ValueError)
    expect_error("by_percentage sai kiểu", lambda: emp1.increase_salary(5, "yes"), TypeError)
    before = zero.base_salary
    zero.increase_salary(10, True)
    check("Tăng % trên lương 0 vẫn bằng 0", zero.base_salary == before == 0)
    zero.increase_salary(500, False)
    check("increase_salary(500, False) = tăng cố định", zero.base_salary == 500)
 
    print("\n[SoftwareEngineer] Ràng buộc dữ liệu:")
    expect_error("Ngôn ngữ rỗng", lambda: SoftwareEngineer("S9", "X", ""), ValueError)
    expect_error("Phụ cấp âm", lambda: SoftwareEngineer("S9", "X", 1000, "Java", -1), ValueError)
    expect_error("Sai số lượng đối số", lambda: SoftwareEngineer("S9", "X", 1000, "Java"), TypeError)
 
    print("\n[ProjectTeam] Ràng buộc và trường hợp biên:")
    expect_error("Mã dự án rỗng", lambda: ProjectTeam("", "Tên"), ValueError)
    expect_error("Thêm None", lambda: team1.add_member(None), TypeError)
    expect_error("make_leader sai kiểu", lambda: team1.add_member(emp1, "yes"), TypeError)
    check("Xóa mã không tồn tại trả về False", team1.remove_member("KHONG_CO") is False)
 
    empty_team = ProjectTeam("PRJ03", "Nhóm rỗng")
    check("Nhóm rỗng: tổng chi phí = 0", empty_team.calculate_total_monthly_cost() == 0)
    empty_team.display_team()
 
    led_team = ProjectTeam("PRJ04", "Nhóm có trưởng nhóm sẵn", emp1)
    check("Constructor 3 tham số: trưởng nhóm tự vào danh sách", led_team.contains("E001"))
    check("Thêm lại trưởng nhóm bị từ chối", led_team.add_member(emp1) is False)
    check("Không xóa được trưởng nhóm duy nhất", led_team.remove_member("E001") is False)
 
    impostor = Employee("E001", "Người trùng mã")
    check("Đối tượng khác nhưng trùng mã bị từ chối khi add_member",
          led_team.add_member(impostor) is False)
    check("change_leader với đối tượng trùng mã bị từ chối",
          led_team.change_leader(impostor) is False)
    check("Trưởng nhóm không bị thay đổi", led_team.leader is emp1)
    check("Bất biến vẫn thỏa", led_team.check_invariants())
 
    check("change_leader với người ngoài nhóm: tự thêm vào nhóm",
          led_team.change_leader(eng1) and led_team.contains("S001") and led_team.leader is eng1)
    check("Trưởng nhóm cũ vẫn là thành viên", led_team.contains("E001"))
 
 
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
 
    emp1, emp2, eng1, eng2, team1 = run_required_scenario()
    run_edge_cases(emp1, emp2, eng1, team1)
    print("\n" + "=" * 70)
    print("KẾT THÚC CHƯƠNG TRÌNH: các đối tượng còn lại sẽ bị hủy (quan sát vòng đời)")
    print("=" * 70)
 
 
if __name__ == "__main__":
    main()