def get_launch_arguments_with_include_launch_description_actions(
    self, conditional_inclusion=False, only_search_local=False
) -> List[Tuple[DeclareLaunchArgument, List['IncludeLaunchDescription']]]:
    """
    Return a list of launch arguments with its associated include launch descriptions actions.

    The first element of the tuple is a declare launch argument action.
    The second is `None` if the argument was declared at the top level of this
    launch description, if not it's a list with all the nested include launch description
    actions involved.

    This list is generated (never cached) by searching through this launch
    description for any instances of the action that declares launch
    arguments.

    It will use :py:meth:`launch.LaunchDescriptionEntity.describe_sub_entities`
    and :py:meth:`launch.LaunchDescriptionEntity.describe_conditional_sub_entities`
    in order to discover as many instances of the declare launch argument
    actions as is possible.
    Also, specifically in the case of the
    :py:class:`launch.actions.IncludeLaunchDescription` action, the method
    :py:meth:`launch.LaunchDescriptionSource.try_get_launch_description_without_context`
    is used to attempt to load launch descriptions without the "runtime"
    context available.
    This function may fail, e.g. if the path to the launch file to include
    uses the values of launch configurations that have not been set yet,
    and in that case the failure is ignored and the arguments defined in
    those launch files will not be seen either.

    Duplicate declarations of an argument are ignored, therefore the
    default value and description from the first instance of the argument
    declaration is used.
    """
    from .actions import IncludeLaunchDescription  # noqa: F811
    declared_launch_arguments: List[
        Tuple[DeclareLaunchArgument, List[IncludeLaunchDescription]]] = []
    from .actions import ResetLaunchConfigurations

    def process_entities(entities, *, _conditional_inclusion, nested_ild_actions=None,
                            only_search_local=False):
        for entity in entities:
            if isinstance(entity, DeclareLaunchArgument):
                # Avoid duplicate entries with the same name.
                if entity.name in (e.name for e, _ in declared_launch_arguments):
                    continue
                # Stuff this contextual information into the class for
                # potential use in command-line descriptions or errors.
                entity._conditionally_included = _conditional_inclusion
                entity._conditionally_included |= entity.condition is not None
                declared_launch_arguments.append((entity, nested_ild_actions))
            if only_search_local:
                if isinstance(entity, IncludeLaunchDescription):
                    continue
            if isinstance(entity, ResetLaunchConfigurations):
                # Launch arguments after this cannot be set directly by top level arguments
                return
            else:
                next_nested_ild_actions = nested_ild_actions
                if isinstance(entity, IncludeLaunchDescription):
                    if next_nested_ild_actions is None:
                        next_nested_ild_actions = []
                    next_nested_ild_actions.append(entity)
                process_entities(
                    entity.describe_sub_entities(),
                    _conditional_inclusion=False,
                    nested_ild_actions=next_nested_ild_actions,
                    only_search_local=only_search_local)
                for conditional_sub_entity in entity.describe_conditional_sub_entities():
                    process_entities(
                        conditional_sub_entity[1],
                        _conditional_inclusion=True,
                        nested_ild_actions=next_nested_ild_actions,
                        only_search_local=only_search_local)

    process_entities(self.entities, _conditional_inclusion=conditional_inclusion,
                        only_search_local=only_search_local)

    return declared_launch_arguments
