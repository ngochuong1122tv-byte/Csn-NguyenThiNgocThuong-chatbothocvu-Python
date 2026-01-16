from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


def normalize(text):
    return text.lower().strip() if text else None


class ActionShowTuition(Action):
    def name(self):
        return "action_show_tuition"

    def run(self, dispatcher, tracker, domain):
        major = normalize(tracker.get_slot("major"))

        if not major:
            dispatcher.utter_message(" Bạn chưa chọn ngành.")
            return []

        tuition = {
            "công nghệ thông tin": (
                "Với ngành Công nghệ Thông tin, sinh viên trong một học kỳ thường "
                "đăng ký khoảng 20 tín chỉ. Với mức học phí 500.000 - 550.000 đồng/tín chỉ, "
                "tổng học phí khoảng 10 - 12 triệu đồng/học kỳ. Mỗi năm có 2 học kỳ chính."
            ),
            "kỹ thuật xây dựng": (
                "Đối với ngành Kỹ thuật Xây dựng, sinh viên thường đăng ký khoảng 20 tín chỉ/học kỳ. "
                "Với mức học phí 500.000 - 550.000 đồng/tín chỉ, tổng học phí khoảng 10 - 12 triệu đồng/học kỳ."
            ),
            "ngôn ngữ anh": (
                "Sinh viên ngành Ngôn ngữ Anh thường đăng ký khoảng 20 tín chỉ/học kỳ. "
                "Học phí trung bình 10 - 12 triệu đồng/học kỳ."
            ),
            "điều dưỡng": (
                "Ngành Điều dưỡng có đặc thù đào tạo riêng, sinh viên thường đăng ký khoảng 22 tín chỉ/học kỳ. "
                "Mức học phí 800.000 - 1.000.000 đồng/tín chỉ và phí cố định 200.000 đồng, "
                "tổng học phí khoảng 20 - 25 triệu đồng/học kỳ. Mỗi năm có 3 học kỳ."
            )
        }

        dispatcher.utter_message(
            text=tuition.get(major, " Chưa có dữ liệu học phí cho ngành này.")
        )
        return []


class ActionCalculateTuitionByMajor(Action):
    def name(self):
        return "action_calculate_tuition_by_major"

    def run(self, dispatcher, tracker, domain):
        major = tracker.get_slot("major")
        cs = tracker.get_slot("tc_co_so")
        cn = tracker.get_slot("tc_chuyen_nganh")

        if not major or cs is None or cn is None:
            dispatcher.utter_message("Vui lòng cung cấp đầy đủ ngành và số tín chỉ!")
            return []

        table = {
            "công nghệ thông tin": (500000, 595000),
            "kỹ thuật xây dựng": (500000, 595000),
            "điều dưỡng": (500000, 545000),
            "ngôn ngữ anh": (250000, 300000)
        }

        gia_cs, gia_cn = table[major.lower()]
        total = cs * gia_cs + cn * gia_cn

        dispatcher.utter_message(
            text=f" Tổng học phí dự kiến: {total:,.0f} VNĐ"
        )

        # RESET SLOT SAU KHI TÍNH
        return [
            SlotSet("tc_co_so", None),
            SlotSet("tc_chuyen_nganh", None)
        ]

class ActionSetAcademicFormContext(Action):
    def name(self):
        return "action_set_academic_form_context"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("confirm_context", "academic_form")]

class ActionSetTTSVContext(Action):
    def name(self):
        return "action_set_ttsv_context"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("confirm_context", "ttsv")]

class ActionResetConfirmContext(Action):
    def name(self):
        return "action_reset_confirm_context"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("confirm_context", None)]
