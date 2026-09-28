NUMBER_COLORS = {
    1: "#388E3C",
    2: "#00897B",
    3: "#1976D2",
    4: "#7B1FA2",
    5: "#C2185B",
    6: "#F3E309",
    7: "#E65100",
    8: "#D32F2F",
}

base_style = """
    QPushButton {
        color: white;
        border-radius: 5px;
        padding: 6px;
        color: black;
    }
    QPushButton:hover {
        background-color: #3a75b5;  /* Lighter blue on hover */
    }
    QPushButton:pressed {
        background-color: #1f4268;  /* Darker blue when clicked */
    }
"""

covered = base_style + """
    QPushButton {
        background-color: #2b5c8f;
    }
    QPushButton:hover {
        background-color: #3a75b5;  /* Lighter blue on hover */
    }
    QPushButton:pressed {
        background-color: #1f4268;  /* Darker blue when clicked */
    }
"""

uncovered = base_style + """
    QPushButton {
        background-color: white;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: white;
    }
    QPushButton:pressed {
        background-color: white;
    }
"""

flagged = base_style + """
    QPushButton {
        background-color: #ffcc00;
    }
    QPushButton:hover {
        background-color: #ffd633;
    }
    QPushButton:pressed {
        background-color: #e6b800;
    }
"""