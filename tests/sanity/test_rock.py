#
# Copyright 2024 Canonical, Ltd.
#

import subprocess

from k8s_test_harness.util import env_util
import pytest


@pytest.mark.parametrize("image_version", ("2.1.6", "1.9.5"))
def test_sanity(image_version):
    rock = env_util.get_build_meta_info_for_rock_version(
        "fluent-bit", image_version, "amd64"
    )
    image = rock.image

    entrypoint = "fluent-bit"
    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", entrypoint, image, "--version"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert f"Fluent Bit v{image_version}" in docker_run.stdout
