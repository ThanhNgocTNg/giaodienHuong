"""Run with: GEMINI_API_KEY='' .venv/bin/python -m unittest discover -s tests -v.

Exercise the existing data workflow through Streamlit's real session state.
No Gemini requests or remote spreadsheet requests are made by these tests.
"""

import io
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.env = os.environ.get("GEMINI_API_KEY")
        os.environ["GEMINI_API_KEY"] = ""
        self.app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assert_healthy()

    def tearDown(self):
        if self.env is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = self.env

    def assert_healthy(self):
        self.assertEqual([], [e.message for e in self.app.exception])
        self.assertEqual([], [e.value for e in self.app.error])

    def load(self, content, name):
        """Use the same ingestion and backup operations as the native uploader."""
        orch = self.app.session_state.orchestrator
        success, message = orch.load_file(content, name)
        self.assertTrue(success, message)
        orch.data_agent.file_infos[name]["original_df"] = orch.data_agent.raw_dataframes[name].copy()
        self.app.session_state.files_loaded = [name]
        self.app.session_state.file_messages = [dict(file=name, success=success, msg=message)]
        self.app.session_state.current_step = 1
        self.app.run()
        self.assert_healthy()
        return orch.data_agent.raw_dataframes[name].copy()

    def go_to_report(self):
        self.app.button(key="btn_approve_step1").click().run()
        self.assertEqual(2, self.app.session_state.current_step)
        self.assert_healthy()
        self.app.button(key="btn_approve_step2").click().run()
        self.assertEqual(3, self.app.session_state.current_step)
        self.assert_healthy()

    def test_start_and_approval_guards(self):
        self.assertEqual(0, len(self.app.sidebar.selectbox))
        self.app.button(key="sb_nav_3").click().run()
        self.assertEqual(0, self.app.session_state.current_step)
        self.app.button(key="btn_hero_start").click().run()
        self.assertEqual(1, self.app.session_state.current_step)
        self.assertTrue(self.app.button(key="top_nav_step2").disabled)
        self.assertTrue(self.app.button(key="top_nav_step3").disabled)
        self.assert_healthy()

    def test_sample_report_export_and_context_survive_navigation(self):
        name = "bao_cao_thi_truong.csv"
        original = self.load((ROOT / "sample_data" / name).read_bytes(), name)
        self.app.text_input(key="biz_type").set_value("Bán lẻ").run()
        self.go_to_report()
        self.assertTrue(self.app.session_state.editable_report)
        self.assertTrue(self.app.session_state.editable_plan)
        self.assertEqual(1, len(self.app.get("download_button")))
        pd.testing.assert_frame_equal(original, self.app.session_state.orchestrator.data_agent.raw_dataframes[name])
        self.app.button(key="sb_nav_1").click().run()
        self.assertEqual("Bán lẻ", self.app.text_input(key="biz_type").value)
        self.assert_healthy()

    def test_approved_fixes_and_restore_original(self):
        name = "issues.csv"
        original = self.load(
            b"region,revenue,customer\nNorth,100,A\nNorth,100,A\nSouth,-20,B\nWest,,C\n", name
        )
        self.app.button(key="btn_approve_step1").click().run()
        self.assertEqual(3, len(self.app.checkbox))
        self.app.button(key=f"btn_apply_fixes_s2_{name}").click().run()
        self.assert_healthy()
        fixed = self.app.session_state.orchestrator.data_agent.raw_dataframes[name]
        self.assertEqual(3, len(fixed))
        self.assertEqual(0, fixed.isna().sum().sum())
        self.assertTrue((fixed["revenue"] >= 0).all())
        self.app.button(key=f"btn_undo_clean_s2_{name}").click().run()
        pd.testing.assert_frame_equal(original, self.app.session_state.orchestrator.data_agent.raw_dataframes[name])
        self.assert_healthy()

    def test_search_sort_and_column_selection(self):
        name = "sales.csv"
        self.load(b"region,revenue\nNorth,100\nSouth,50\nWest,200\n", name)
        self.app.text_input(key=f"s1_{name}_search").set_value("South").run()
        self.assertTrue(any("**1 / 3**" in caption.value for caption in self.app.caption))
        self.app.text_input(key=f"s1_{name}_search").set_value("").run()
        self.app.selectbox(key=f"s1_{name}_scol").select("revenue").run()
        self.app.selectbox(key=f"s1_{name}_sasc").select("Giảm dần").run()
        self.app.multiselect(key=f"s1_{name}_cols").select("revenue").run()
        displayed = self.app.dataframe[0].value
        self.assertEqual([200, 100, 50], displayed["revenue"].tolist())
        self.assertEqual(["revenue"], displayed.columns.tolist())
        self.assert_healthy()

    def test_excel_ingestion_and_report_editing(self):
        content = io.BytesIO()
        pd.DataFrame({"region": ["North", "South", "West"], "revenue": [100, 50, 200]}).to_excel(content, index=False)
        self.load(content.getvalue(), "sales.xlsx")
        self.go_to_report()
        self.app.button(key="toggle_edit_dashboard_btn").click().run()
        self.assertTrue(self.app.session_state.show_edit_dashboard)
        self.assertTrue(self.app.dataframe)
        self.app.button(key="toggle_edit_report_btn").click().run()
        self.app.text_input(key="rep_title_input").set_value("Báo cáo thử nghiệm").run()
        save = next(b for b in self.app.button if b.label == "Lưu thay đổi báo cáo")
        save.click().run()
        self.assertEqual("Báo cáo thử nghiệm", self.app.session_state.dashboard_title)
        self.assert_healthy()

    def test_context_suggestion_has_no_duplicate_widget_default_warning(self):
        from streamlit.elements.lib import policies
        from ui import clean_ui_text

        self.load(b"month,region,orders,revenue\nJan,North,12,100\nFeb,South,8,70\n", "context.csv")
        self.app.text_area(key="biz_extra").set_value("Theo dõi kết quả quý này").run()
        with patch.object(policies, "_shown_default_value_warning", False):
            self.app.button(key="btn_ai_suggest_ctx").click().run()
        self.assertTrue(self.app.text_input(key="biz_type").value)
        self.assertTrue(self.app.text_area(key="biz_questions").value)
        self.assertEqual("Theo dõi kết quả quý này", self.app.text_area(key="biz_extra").value)
        self.assertFalse(any("Session State API" in warning.value for warning in self.app.warning))
        for button in self.app.button:
            self.assertEqual(button.label, clean_ui_text(button.label))
        self.assert_healthy()

    def test_report_scope_still_selects_individual_files_without_icon_prefixes(self):
        self.load(b"region,revenue\nNorth,100\nSouth,50\nWest,200\n", "first.csv")
        self.load(b"region,revenue\nNorth,10\nSouth,30\nWest,20\n", "second.csv")
        self.go_to_report()
        self.assertEqual(6, self.app.session_state.dashboard_scores_df["Số bản ghi"].sum())
        self.app.selectbox(key="s3_file_scope").select("second.csv").run()
        self.assertEqual(3, self.app.session_state.dashboard_scores_df["Số bản ghi"].sum())
        self.assertIn("second.csv", self.app.session_state.dashboard_title)
        self.assertNotIn("first.csv", self.app.session_state.dashboard_title)
        self.assert_healthy()


if __name__ == "__main__":
    unittest.main()
