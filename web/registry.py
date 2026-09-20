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
        "Official GECBH CSI page. Use this source for questions about "
        "CSI Student Branch GECBH, its staff advisor, executive committee, "
        "CSI activities, workshops, competitions, project guidance, "
        "talk sessions, and CSI-related information officially published "
        "by GECBH."
    ),
},
   "csi_student_branch": {
    "name": "CSI Student Branch GECBH",
    "url": "https://csigecbh.in/",
    "description": (
        "CSI Student Branch GECBH website. Use this source for current "
        "student-branch activities, events, announcements, achievements, "
        "and information specifically published on the student branch website."
    ),
},
}


def get_tool_registry():
    return TOOL_REGISTRY