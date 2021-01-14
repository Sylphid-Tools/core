name = "sylphid_core"

version = "0.2.0"

build_requires = ["python"]

tests = {
    "unit": {
        "command": "pytest -sr {root}/tests",
        "requires": ["pytest", "pytest_cov", "pyfakefs", "mock"],
        "run_on": ["default", "pre_install"],
    }
}


def commands():
    env.PYTHONPATH.append("{root}/python")
