from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionShowTuition(Action):
    def name(self):
        return "action_show_tuition"

    def run(self, dispatcher, tracker, domain):
        major = tracker.get_slot("major")

        if not major:
            dispatcher.utter_message("❗ Bạn chưa chọn ngành.")
            return []

        major = major.lower().strip()

        tuition = {
            "Công Nghệ Thông Tin": "Với gành Công nghệ thông tin, sinh viên trong một học kỳ thường đăng ký khoảng 20 tín chỉ. Với mức học phí 500.000 - 550.000 đồng cho mỗi tín chỉ, tổng học phí một học kỳ vào khoảng 10.000.000-12.000.000 đồng. mỗi năm có 2 học kì chính.",
            "Kỹ Thuật Xây Dựng": "Đối với ngành Kỹ thuật xây dựng,  sinh viên trong một học kỳ thường đăng ký khoảng 20 tín chỉ. Với mức học phí 500.000 - 550.000 đồng cho mỗi tín chỉ, tổng học phí một học kỳ vào khoảng 10.000.000-12.000.000 đồng. mỗi năm có 2 học kì chính.",
            "Ngôn Ngữ Anh": "Sinh viên trong một học kỳ thường đăng ký khoảng 20 tín chỉ. Với mức học phí 500.000 - 550.000 đồng cho mỗi tín chỉ, tổng học phí một học kỳ vào khoảng 10.000.000-12.000.000 đồng. mỗi năm có 2 học kì chính.",
            "Điều Dưỡng": "Do đặc thù đào tạo, sinh viên thường đăng ký khoảng 22 tín chỉ mỗi học kỳ. Với mức học phí 800.000- 1.000.000 đồng cho mỗi tín chỉ và phí cố định 200.000 đồng, tổng học phí một học kỳ là 20.000.000 - 25.000.000 đồng.Mỗi năm có 3 học kì"
        }

        dispatcher.utter_message(
            text=tuition.get(major, "Chưa có dữ liệu học phí ngành này.")
        )
        return []

class ActionCalculateTuitionByMajor(Action):
    def name(self):
        return "action_calculate_tuition_by_major"

    def run(self, dispatcher, tracker, domain):
        major = tracker.get_slot("major")
        cs = tracker.get_slot("tc_co_so")
        cn = tracker.get_slot("tc_chuyen_nganh")

        table = {
            "công nghệ thông tin": (500000, 595000),
            "kỹ thuật xây dựng": (500000, 595000),
            "điều dưỡng": (500000, 545000),
            "ngôn ngữ anh": (250000, 300000)
        }

        gia_cs, gia_cn = table[major]
        total = cs * gia_cs + cn * gia_cn

        dispatcher.utter_message(
            text=f"Tổng học phí dự kiến: {total:,.0f} VNĐ"
        )
        return []
