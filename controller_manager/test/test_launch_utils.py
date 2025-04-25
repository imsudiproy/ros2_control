import pytest
from unittest.mock import patch, MagicMock
from launch import LaunchDescription
from launch_ros.actions import Node

# filepath: controller_manager/controller_manager/test_launch_utils.py

from .launch_utils import (
    generate_controllers_spawner_launch_description,
    generate_controllers_spawner_launch_description_from_dict,
    generate_load_controller_launch_description,
)


@patch("controller_manager.controller_manager.launch_utils.Node")
@patch("controller_manager.controller_manager.launch_utils.LaunchDescription")
def test_generate_controllers_spawner_launch_description(mock_launch_description, mock_node):
    # Mock Node and LaunchDescription
    mock_node.return_value = MagicMock()
    mock_launch_description.return_value = MagicMock()

    # Test data
    controller_names = ["joint_state_broadcaster"]
    controller_params_files = ["/path/to/controller_params.yaml"]
    extra_spawner_args = ["--load-only"]

    # Call the function
    result = generate_controllers_spawner_launch_description(
        controller_names, controller_params_files, extra_spawner_args
    )

    # Assertions
    assert isinstance(result, LaunchDescription)
    mock_node.assert_called_once_with(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "controller_manager",
            "--param-file",
            "/path/to/controller_params.yaml",
            "--load-only",
        ],
        shell=True,
        output="screen",
    )
    mock_launch_description.assert_called_once()


@patch("controller_manager.controller_manager.launch_utils.generate_controllers_spawner_launch_description")
def test_generate_controllers_spawner_launch_description_from_dict(mock_generate):
    # Test data
    controller_info_dict = {
        "joint_state_broadcaster": "/path/to/controller_params.yaml",
        "position_controller": None,
    }
    extra_spawner_args = ["--load-only"]

    # Call the function
    generate_controllers_spawner_launch_description_from_dict(controller_info_dict, extra_spawner_args)

    # Assertions
    mock_generate.assert_called_once_with(
        controller_names=["joint_state_broadcaster", "position_controller"],
        controller_params_files=["/path/to/controller_params.yaml"],
        extra_spawner_args=extra_spawner_args,
    )


@patch("controller_manager.controller_manager.launch_utils.generate_controllers_spawner_launch_description")
def test_generate_load_controller_launch_description(mock_generate):
    # Test data
    controller_name = "joint_state_broadcaster"
    controller_params_file = "/path/to/controller_params.yaml"
    extra_spawner_args = ["--load-only"]

    # Call the function
    generate_load_controller_launch_description(controller_name, controller_params_file, extra_spawner_args)

    # Assertions
    mock_generate.assert_called_once_with(
        controller_names=[controller_name],
        controller_params_files=[controller_params_file],
        extra_spawner_args=extra_spawner_args,
    )