# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Workspace signals."""
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Union,
    cast,
)

from django.db import (
    transaction,
)
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import (
    receiver,
)

from asgiref.sync import async_to_sync as _async_to_sync
from channels.layers import (
    get_channel_layer,
)

from user.signal_defs import (
    user_invitation_redeemed,
)
from workspace.models import TaskLabel
from workspace.models.chat_message import ChatMessage
from workspace.models.label import Label
from workspace.models.sub_task import SubTask
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.models.workspace_user_invite import WorkspaceUserInvite
from workspace.services.workspace import (
    workspace_add_user,
)
from workspace.types import ConsumerEvent

from . import (
    signal_defs,
)

if TYPE_CHECKING:
    from user.models import (  # noqa: F401
        User,
    )


Unknown = object


HasOrIsWorkspace = Union[
    Workspace,
    Label,
    WorkspaceUser,
    WorkspaceBoard,
]
HasOrIsWorkspaceBoard = Union[
    WorkspaceBoard,
    WorkspaceBoardSection,
    Task,
    TaskLabel,
    SubTask,
]
HasOrIsTask = Union[Task, TaskLabel, SubTask, ChatMessage]


logger = logging.getLogger(__name__)

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(instance: WorkspaceUser, **kwargs: object) -> None:
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


def group_send(destination: str, event: ConsumerEvent) -> None:
    """Send message to a channels group."""
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        destination,
        event,
    )


def send_workspace_change_signal(instance: HasOrIsWorkspace) -> None:
    """Send workspace.change signal to correct group."""
    match instance:
        case Workspace():
            workspace = instance
        case Label():
            workspace = instance.workspace
        case WorkspaceUser():
            workspace = instance.workspace
        case WorkspaceBoard():
            workspace = instance.workspace
    uuid = str(workspace.uuid)
    group_send(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


def send_workspace_board_change_signal(
    instance: HasOrIsWorkspaceBoard,
) -> None:
    """Send workspace_board.change signal to correct group."""
    match instance:
        case WorkspaceBoard():
            workspace_board = instance
        case WorkspaceBoardSection():
            workspace_board = instance.workspace_board
        case Task():
            workspace_board = instance.workspace_board_section.workspace_board
        case TaskLabel():
            workspace_board = (
                instance.task.workspace_board_section.workspace_board
            )
        case SubTask():
            workspace_board = (
                instance.task.workspace_board_section.workspace_board
            )
    uuid = str(workspace_board.uuid)
    group_send(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


def send_task_change_signal(instance: HasOrIsTask) -> None:
    """Send task.change signal to correct group."""
    match instance:
        case Task():
            task = instance
        case TaskLabel():
            task = instance.task
        case SubTask():
            task = instance.task
        case ChatMessage():
            task = instance.task
    uuid = str(task.uuid)
    group_send(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=Workspace)
@receiver(post_delete, sender=Workspace)
def workspace_changed(instance: Workspace, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=Label)
@receiver(post_delete, sender=Label)
def label_changed(instance: Label, **kwargs: Unknown) -> None:
    """Broadcast changes upon label save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=WorkspaceUser)
@receiver(post_delete, sender=WorkspaceUser)
def workspace_user_changed(instance: WorkspaceUser, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace user save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=WorkspaceBoard)
@receiver(post_delete, sender=WorkspaceBoard)
def workspace_board_changed(
    instance: WorkspaceBoard, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace board save/delete."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance)


@receiver(post_save, sender=WorkspaceBoardSection)
@receiver(post_delete, sender=WorkspaceBoardSection)
def workspace_board_section_changed(
    instance: WorkspaceBoardSection, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace board section save/delete."""
    send_workspace_board_change_signal(instance)


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def task_changed(instance: Task, **kwargs: Unknown) -> None:
    """Broadcast changes upon task save/delete."""
    send_workspace_board_change_signal(instance)
    send_task_change_signal(instance)


@receiver(post_save, sender=TaskLabel)
@receiver(post_delete, sender=TaskLabel)
def task_label_changed(instance: TaskLabel, **kwargs: Unknown) -> None:
    """Broadcast changes upon task label save/delete."""
    send_workspace_board_change_signal(instance)
    send_task_change_signal(instance)


@receiver(post_save, sender=SubTask)
@receiver(post_delete, sender=SubTask)
def sub_task_changed(instance: SubTask, **kwargs: Unknown) -> None:
    """Broadcast changes upon sub task save/delete."""
    send_workspace_board_change_signal(instance)
    send_task_change_signal(instance)


@receiver(post_save, sender=ChatMessage)
@receiver(post_delete, sender=ChatMessage)
def chat_message_changed(instance: ChatMessage, **kwargs: Unknown) -> None:
    """Broadcast changes upon chat message save/delete."""
    send_task_change_signal(instance)


# TODO this should be in services
@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(
    user: "User", instance: WorkspaceUserInvite, **kwargs: Unknown
) -> None:
    """Redeem workspace invitations."""
    qs = WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        workspace = invite.workspace
        workspace_add_user(workspace=workspace, user=user)
        invite.redeem()
