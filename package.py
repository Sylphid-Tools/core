name = "sylphid_core"

version = "0.3.0"

build_requires = ["python"]

requires = ["requests"]

tests = {
    "unit": {
        "command": "pytest -sr {root}/tests",
        "requires": ["pytest", "pytest_cov", "pyfakefs", "mock"],
        "run_on": ["default", "pre_install"],
    }
}


def commands():
    env.PYTHONPATH.append("{root}/python")
