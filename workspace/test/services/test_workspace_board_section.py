"""Test workspace board section services."""
import pytest

from workspace.factory import WorkspaceBoardSectionFactory
from workspace.models import WorkspaceBoard
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_board_section import (
    workspace_board_section_move,
)


@pytest.mark.django_db
def test_moving_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a section around."""
    other_section = WorkspaceBoardSectionFactory(
        workspace_board=workspace_board,
    )
    other_other_section = WorkspaceBoardSectionFactory(
        workspace_board=workspace_board,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
        other_section,
        other_other_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=0,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
        other_section,
        other_other_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=2,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        other_section,
        other_other_section,
        workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        other_section,
        workspace_board_section,
        other_other_section,
    ]


@pytest.mark.django_db
def test_moving_empty_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving when there are no other sections."""
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
    ]
    assert workspace_board_section._order == 0