import datetime
import random
from typing import List, TypedDict

import reflex as rx
from faker import Faker

from back.auth_class import AuthState

fake = Faker()


class Metric(TypedDict):
    title: str
    value: int

class VisitorDataPoint(TypedDict):
    date: str
    series1: int
    series2: int


class DocumentRow(TypedDict):
    id: int
    header: str
    section_type: str
    status: str
    target: int
    limit: int
    reviewer: str


class DashboardState(rx.State):
    """The state for the dashboard page."""

    key_metrics: List[Metric] = []
    visitor_data: List[VisitorDataPoint] = []
    document_data: List[DocumentRow] = []
    selected_visitor_timeframe: str = "Last 3 months"
    selected_document_tab: str = "Outline"
    document_columns: List[str] = [
        "",
        "Header",
        "Section Type",
        "Status",
        "Target",
        "Limit",
        "Reviewer",
    ]

    def _generate_fake_data(self):
        """Generates fake data for the dashboard."""
        self.key_metrics = [
            {
                "title": "Moyenne des aides en euros",
                "value": 12, #AuthState.get_average_euro,
            },
            {
                "title": "Moyenne des cumacs",
                "value": 6,
            },
        ]
        today = datetime.date.today()
        self.visitor_data = []
        for i in range(90):
            date = today - datetime.timedelta(days=i)
            self.visitor_data.append(
                {
                    "date": (
                        date.strftime("Jun %d")
                        if date.month == 6
                        else date.strftime("%b %d")
                    ),
                    "series1": fake.random_int(min=100, max=500),
                    "series2": fake.random_int(min=50, max=300),
                }
            )
        self.visitor_data.reverse()
        statuses = ["Done", "In Process", "Pending"]
        section_types = [
            "Cover page",
            "Table of contents",
            "Narrative",
            "Technical approach",
            "Management plan",
            "Pricing section",
        ]
        self.document_data = []
        for i in range(5):
            self.document_data.append(
                {
                    "id": i,
                    "header": fake.catch_phrase().replace('"', ""),
                    "section_type": random.choice(section_types),
                    "status": random.choice(statuses),
                    "target": fake.random_int(min=5, max=50),
                    "limit": fake.random_int(min=3, max=30),
                    "reviewer": fake.name(),
                }
            )
        self.document_data[0].update(
            {
                "header": "Cover page",
                "section_type": "Cover page",
                "status": "In Process",
                "target": 18,
                "limit": 5,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[1].update(
            {
                "header": "Table of contents",
                "section_type": "Table of contents",
                "status": "Done",
                "target": 29,
                "limit": 24,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[2].update(
            {
                "header": "Executive summary",
                "section_type": "Narrative",
                "status": "Done",
                "target": 10,
                "limit": 13,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[3].update(
            {
                "header": "Technical approach",
                "section_type": "Narrative",
                "status": "Done",
                "target": 27,
                "limit": 23,
                "reviewer": "Jamik Tashpulatov",
            }
        )

    @rx.event
    def load_initial_data(self):
        """Load initial fake data if not already loaded."""
        if (
            not self.key_metrics
            and (not self.visitor_data)
            and (not self.document_data)
        ):
            self._generate_fake_data()

    @rx.event
    def set_visitor_timeframe(self, timeframe: str):
        self.selected_visitor_timeframe = timeframe

    @rx.event
    def set_document_tab(self, tab: str):
        self.selected_document_tab = tab


TOOLTIP_PROPS = {
    "separator": ": ",
    "cursor": False,
    "is_animation_active": False,
    "label_style": {"fontWeight": "500"},
    "item_style": {
        "color": "currentColor",
        "display": "flex",
        "paddingBottom": "0px",
        "justifyContent": "space-between",
        "textTransform": "capitalize",
    },
    "content_style": {
        "borderRadius": "5px",
        "boxShadow": "0px 2px 6px 0px rgba(0, 0, 0, 0.1)",
        "fontSize": "0.75rem",
        "lineHeight": "1rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "width": "auto",
        "padding": "0.375rem 0.625rem",
        "backgroundColor": "white",
        "border": "1px solid #e2e8f0",
    },
}

def metric_card(metric: Metric) -> rx.Component:
    """A card displaying a single key metric."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                metric["title"],
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="flex items-center justify-between mb-1",
        ),
        rx.el.p(
            metric["value"],
            class_name="text-3xl font-semibold text-gray-900 mb-2",
        ),
        class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-sm",
    )


def key_metrics_section() -> rx.Component:
    """The section displaying key metric cards."""
    return rx.el.div(
        rx.foreach(DashboardState.key_metrics, metric_card),
        class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4",
        margin_bottom="1em",
    )