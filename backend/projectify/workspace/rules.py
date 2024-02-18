# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Workspace app rules.

The order of rules follows the ordering of models.
"""
from functools import partial

import rules

from projectify.user.models import User

from .models.const import WorkspaceUserRoles
from .models.workspace import Workspace
from .selectors.quota import Resource, workspace_quota_for
from .selectors.workspace_user import workspace_user_find_for_workspace


def check_permissions_for(
    role: WorkspaceUserRoles, user: User, workspace: Workspace
) -> bool:
    """Check whether a user has required role for target."""
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace, user=user
    )
    if workspace_user is None:
        return False
    return workspace.has_at_least_role(workspace_user, role)


# Role predicates
# ---------------
# Observer < Member < Maintainer < Owner
is_at_least_observer = rules.predicate(
    partial(check_permissions_for, WorkspaceUserRoles.OBSERVER)
)
is_at_least_member = rules.predicate(
    partial(check_permissions_for, WorkspaceUserRoles.MEMBER)
)
is_at_least_maintainer = rules.predicate(
    partial(check_permissions_for, WorkspaceUserRoles.MAINTAINER)
)
is_at_least_owner = rules.predicate(
    partial(check_permissions_for, WorkspaceUserRoles.OWNER)
)


def within_quota(
    resource: Resource, _user: User, workspace: Workspace
) -> bool:
    """Extract .within_quota from workspace_quota_for."""
    return workspace_quota_for(
        resource=resource, workspace=workspace
    ).within_quota


# Quota predicates
# ----------------
# Return True if a chat message can be created for workspace
within_chat_message_quota = rules.predicate(
    partial(within_quota, "ChatMessage")
)
# Return True if a label can be created for workspace
within_label_quota = rules.predicate(partial(within_quota, "Label"))
# Return True if a sub task can be created in workspace
within_sub_task_quota = rules.predicate(partial(within_quota, "SubTask"))
# Return True if a task can be created in workspace
within_task_quota = rules.predicate(partial(within_quota, "Task"))
# Return True if a task label can be created for a task
within_task_label_quota = rules.predicate(partial(within_quota, "TaskLabel"))
# Return True if a workspace board can be created in workspace
within_workspace_board_quota = rules.predicate(
    partial(within_quota, "WorkspaceBoard")
)
# Return True if a section can be created in a workspace
within_workspace_board_section_quota = rules.predicate(
    partial(within_quota, "WorkspaceBoardSection")
)
# Return True if a workspace user can be added to a workspace
# The two following use the same quota
within_workspace_user_quota = rules.predicate(
    partial(within_quota, "WorkspaceUserAndInvite")
)
# Return True if a workspace user invite can be sent for a workspace
within_workspace_user_invite_quota = within_workspace_user_quota


# Workspace
# Anyone should be able to create a workspace
rules.add_perm("workspace.create_workspace", rules.is_active)
rules.add_perm("workspace.read_workspace", is_at_least_observer)
rules.add_perm("workspace.update_workspace", is_at_least_owner)
rules.add_perm("workspace.delete_workspace", is_at_least_owner)

# Workspace user invite
rules.add_perm(
    "workspace.create_workspace_user_invite",
    is_at_least_owner & within_workspace_user_invite_quota,
)
rules.add_perm("workspace.read_workspace_user_invite", is_at_least_owner)
rules.add_perm("workspace.update_workspace_user_invite", is_at_least_owner)
rules.add_perm("workspace.delete_workspace_user_invite", is_at_least_owner)

# Workspace user
rules.add_perm(
    "workspace.create_workspace_user",
    is_at_least_owner & within_workspace_user_quota,
)
rules.add_perm("workspace.read_workspace_user", is_at_least_observer)
rules.add_perm("workspace.update_workspace_user", is_at_least_owner)
rules.add_perm("workspace.delete_workspace_user", is_at_least_owner)

# Workspace board
rules.add_perm(
    "workspace.create_workspace_board",
    is_at_least_maintainer & within_workspace_board_quota,
)
rules.add_perm("workspace.read_workspace_board", is_at_least_observer)
rules.add_perm("workspace.update_workspace_board", is_at_least_maintainer)
rules.add_perm("workspace.delete_workspace_board", is_at_least_maintainer)

# Workspace board section
rules.add_perm(
    "workspace.create_workspace_board_section",
    is_at_least_maintainer & within_workspace_board_section_quota,
)
rules.add_perm("workspace.read_workspace_board_section", is_at_least_observer)
rules.add_perm(
    "workspace.update_workspace_board_section", is_at_least_maintainer
)
rules.add_perm(
    "workspace.delete_workspace_board_section", is_at_least_maintainer
)

# Task
rules.add_perm("workspace.create_task", is_at_least_member & within_task_quota)
rules.add_perm("workspace.read_task", is_at_least_observer)
rules.add_perm("workspace.update_task", is_at_least_member)
rules.add_perm("workspace.delete_task", is_at_least_maintainer)

# Label
rules.add_perm(
    "workspace.create_label", is_at_least_maintainer & within_label_quota
)
rules.add_perm("workspace.read_label", is_at_least_observer)
rules.add_perm("workspace.update_label", is_at_least_maintainer)
rules.add_perm("workspace.delete_label", is_at_least_maintainer)

# Task label
rules.add_perm(
    "workspace.create_task_label", is_at_least_member & within_task_label_quota
)
rules.add_perm("workspace.read_task_label", is_at_least_observer)
rules.add_perm("workspace.update_task_label", is_at_least_member)
rules.add_perm("workspace.delete_task_label", is_at_least_member)


# Sub task
rules.add_perm(
    "workspace.create_sub_task", is_at_least_member & within_sub_task_quota
)
rules.add_perm("workspace.read_sub_task", is_at_least_observer)
rules.add_perm("workspace.update_sub_task", is_at_least_member)
rules.add_perm("workspace.delete_sub_task", is_at_least_member)

# Chat message
rules.add_perm(
    "workspace.create_chat_message",
    is_at_least_member & within_chat_message_quota,
)
rules.add_perm("workspace.read_chat_message", is_at_least_observer)
rules.add_perm("workspace.update_chat_message", is_at_least_member)
rules.add_perm("workspace.delete_chat_message", is_at_least_maintainer)
