#
# Copyright 2024 Canonical, Ltd.
#
import logging

from k8s_test_harness import harness
from k8s_test_harness.util import env_util, k8s_util

pytest_plugins = ["k8s_test_harness.plugin"]

LOG = logging.getLogger(__name__)


def test_integration_fluent_bit(module_instance: harness.Instance):
    fluent_bit_rock = env_util.get_build_meta_info_for_rock_version(
        "fluent-bit", "2.1.6", "amd64"
    )

    images = [k8s_util.HelmImage(fluent_bit_rock.image)]

    helm_command = k8s_util.get_helm_install_command(
        "fluent-bit",
        "fluent-bit",
        namespace="fluent-bit",
        repository="https://fluent.github.io/helm-charts",
        chart_version="0.34.2",  # chart version with 2.1.6 app
        images=images,
    )

    module_instance.exec(helm_command)

    k8s_util.wait_for_daemonset(module_instance, "fluent-bit", "fluent-bit")
