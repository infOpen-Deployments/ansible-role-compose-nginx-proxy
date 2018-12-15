"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('path,user,group,mode', [
    ('/opt/infopen', 'root', 'root', 0o755),
    ('/opt/infopen/nginx-proxy', 'root', 'root', 0o755),
    ('/opt/infopen/nginx-proxy/releases', 'root', 'root', 0o755),
    ('/opt/infopen/nginx-proxy/repo', 'root', 'root', 0o755),
    ('/opt/infopen/nginx-proxy/shared', 'root', 'root', 0o755),
    ('/var/opt/infopen', 'root', 'root', 0o755),
    ('/var/opt/infopen/nginx-proxy', 'root', 'root', 0o755),
])
def test_service_folders(host, path, user, group, mode):
    """
    Ensure service root folders exists and have expected permissions
    """

    current_folder = host.file(path)

    assert current_folder.exists
    assert current_folder.is_directory
    assert current_folder.user == user
    assert current_folder.group == group
    assert current_folder.mode == mode


def test_service_ansistrano_current_link(host):
    """
    Ensure service has a "current" symlink
    """

    symlink_path = host.file('/opt/infopen/nginx-proxy/current')
    expected_symlink_to = '/opt/infopen/nginx-proxy/releases/19700101-1.0.0'

    assert symlink_path.exists
    assert symlink_path.is_symlink
    assert symlink_path.linked_to == expected_symlink_to
    assert symlink_path.user == 'root'
    assert symlink_path.group == 'root'


@pytest.mark.parametrize('process_name,expected_count', [
    ('nginx', 2),
    ('nginx-vts-expor', 1),  # nginx_vts_exporter
])
def test_processes(host, process_name, expected_count):
    """
    Ensure expected processes running and available
    """

    processes = host.process.filter(comm=process_name)

    assert len(processes) == expected_count
