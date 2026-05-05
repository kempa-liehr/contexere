import io
import os
import subprocess
from pathlib import Path
import pytest
import sys

from contexere.nxt import main

@pytest.fixture()
def temp_dir(tmp_path_factory):
    base = tmp_path_factory.mktemp("session_data")
    return base

def test_project_and_summary(monkeypatch, temp_dir):
    os.chdir(temp_dir)
    user_input = (
        "Example Research Project\n"  # project_name
        "\n"  # repo_name (default: ERP)
        "\n"  # module_name (default: erp)
        "Tester\n"  # author_name
        "Test project\n"  # description
        "\n"  # python_version_number (default)
        "\n"  # dataset_storage (default: 1 none)
        "\n"  # environment_manager (default: 1 virtualenv)
        "\n"  # dependency_file (default: 1 requirements.txt)
        "2\n"  # pydata_packages (default: 1 none)
        "2\n"  # testing_framework (default: 1 none)
        "\n"  # linting_and_formatting (default: 1 ruff)
        "2\n"  # open_source_license (default: 1 No license)
        "\n"  # docs (default: 1 mkdocs)
        "\n"  # include_code_scaffold (default: 1 Yes)
    )

    def fake_subprocess_call(cmd, **kwargs):
        return subprocess.run(
            cmd,
            input=user_input.encode(),
            **{k: v for k, v in kwargs.items() if k != "stdin"}
        ).returncode

    monkeypatch.setattr(subprocess, "call", fake_subprocess_call)

    main(["--project"])

    example_file = Path(temp_dir) / 'ERP/Makefile'
    assert example_file.exists()