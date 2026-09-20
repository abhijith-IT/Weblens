TOOL_REGISTRY = {
    "gecbh_official": {
        "name": "GECBH Official Website",
        "url": "https://www.gecbh.ac.in/",
        "description": (
            "Official Government Engineering College Barton Hill website "
            "containing college information, departments, faculty, and notices."
        ),
    },
    "gecbh_csi": {
        "name": "GECBH CSI",
        "url": "https://www.gecbh.ac.in/csi.php",
        "description": (
            "Official GECBH CSI page containing information about the "
            "college CSI chapter and its activities."
        ),
    },
    "csi_student_branch": {
        "name": "CSI Student Branch GECBH",
        "url": "https://csigecbh.in/",
        "description": (
            "CSI Student Branch website containing information about "
            "CSI activities, events, and student-branch information."
        ),
    },
}


def get_tool_registry():
    return TOOL_REGISTRY