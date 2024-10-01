# Launch Update Role

This Ansible role updates two specific functions in the launch package.

## Requirements

- Ansible 2.9 or higher
- Python 3.10 or other tested Python on the target system
- ROS Humble installed on the target system

## Role Variables

- `file1_path`: Path to the first file to be updated
- `file2_path`: Path to the second file to be updated
- `function1_name`: Name of the first function to be updated
- `function2_name`: Name of the second function to be updated
- `backup`: Whether to create backups of the original files (default: yes)

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - ros2_launch_update
```

## Mechanism

- Install required python libraries
- Make sure the ROS Launch related files (there are two of them) are installed
- Backup the original file in to .bak
- Re-write the files with the new function.
- Simply evaluate the result file.

### Maintenance

- Related PR on the official Repo: <https://github.com/ros2/launch/pull/746>
- Code base: <https://github.com/Owen-Liuyuxuan/launch/tree/feat/argument_check_skipping>

For this role, we maintain the two "updated function" in `templates`. Unless there are updates in code directly in this codes

- [get_launch_arguments_with_include_launch_description_actions](https://github.com/Owen-Liuyuxuan/launch/blob/0e97f2fc25e82d2a9a3a3eb85ee2995fafce94a4/launch/launch/launch_description.py#L93)
- [execute](https://github.com/Owen-Liuyuxuan/launch/blob/0e97f2fc25e82d2a9a3a3eb85ee2995fafce94a4/launch/launch/actions/include_launch_description.py#L146)

- If the PR is absorbed into the official launch file, we can just skip this setup and use the official code.
- Normal updates in ros2 launch not involving the two functions (even it is in the same files) will not make this role fail.
- If the official repos have changes in the directory structure it is fine.
- If there are updates in ROSVersion/PythonVersion that changes the path of the installed scripts, we need to change the parameter values to adapt to it.
