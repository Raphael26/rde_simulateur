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