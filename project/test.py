from grid import Grid
from Weather_System import WeatherSystem
from Orchestrator import orchestrate_missions
from Execution import execute_flight

def run_comprehensive_simulation():
    print("=== [AeroPath System] Starting Integrated Test ===\n")

    # 1. إعداد الخريطة والطقس
    # شبكة 15x15 مع منطقة محظورة في المنتصف
    my_grid = Grid(15, 15)
    my_grid.register_no_fly_zones([(7,7), (7,8), (8,7), (8,8)])
    weather = WeatherSystem()

    # 2. تعريف الأسطول (10 حالات تغطي كافة الاحتمالات)
    fleet = {
        "D01_Normal":      {"target": (5, 5),   "battery": 300, "max_battery": 300, "payload": 2},
        "D02_Low_Battery": {"target": (14, 14), "battery": 50,  "max_battery": 200, "payload": 1},  # سيفشل في الفحص المبدئي
        "D03_In_NoFly":    {"target": (7, 7),   "battery": 300, "max_battery": 300, "payload": 0},  # سيفشل في التخطيط
        "D04_Heavy_Load":  {"target": (1, 8),   "battery": 500, "max_battery": 500, "payload": 10}, # استهلاك طاقة عالي
        "D05_Wind_Storm":  {"target": (10, 10), "battery": 250, "max_battery": 250, "payload": 2},  # سيتعرض لرياح مفاجئة
        "D06_Queue_A":     {"target": (0, 10),  "battery": 300, "max_battery": 300, "payload": 2},  # سيحدث تأخير (Delay)
        "D07_Queue_B":     {"target": (10, 0),  "battery": 300, "max_battery": 300, "payload": 2},  # سيحدث تأخير إضافي
        "D08_Edge_Case":   {"target": (14, 0),  "battery": 400, "max_battery": 400, "payload": 1},  # أقصى حدود الخريطة
        "D09_Standard":    {"target": (3, 3),   "battery": 200, "max_battery": 200, "payload": 1},
        "D10_Critical":    {"target": (12, 12), "battery": 150, "max_battery": 150, "payload": 2}   # عودة طارئة بسبب نقص الطاقة
    }

    # 3. مرحلة التنظيم (Orchestration)
    print("[Phase 1] Planning & Scheduling Missions...")
    planned_missions = orchestrate_missions(my_grid, fleet)

    # 4. مرحلة التنفيذ (Execution) مع محاكاة الرياح الديناميكية
    print("\n[Phase 2] Executing Flights with Dynamic Monitoring...")
    
    # محاكاة: المستخدم يرفع الرياح لـ 12 ضعف على الدرون D05 فقط أثناء طيرانه
    weather.set_drone_wind("D05_Wind_Storm", 12.0)

    for d_id, res in planned_missions.items():
        print(f"\n> Analyzing Drone: {d_id}")
        
        if res['status'] == "Success":
            # تشغيل المراقبة اللحظية
            status, path = execute_flight(my_grid, d_id, res['path'], fleet[d_id], weather)
            
            # عرض النتائج بطريقة منظمة
            print(f"  Result: {status}")
            print(f"  Delay: {res['delay']} seconds")
            print(f"  Path Length: {len(path)} steps")
            if "Emergency" in status or "Abort" in status:
                print(f" Caution: Drone initiated safety protocols.")
        else:
            print(f"  Result: Failed during planning")
            print(f"  Reason: {res['reason']}")

    print("\n=== Simulation Finished ===")

if __name__ == "__main__":
    run_comprehensive_simulation()