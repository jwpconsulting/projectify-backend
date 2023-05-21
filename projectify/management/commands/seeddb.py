"""Seeddb command."""
import random
from typing import (
    Iterable,
    Optional,
    Sequence,
)

from django.contrib import (
    auth,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.core.management.base import (
    BaseCommand,
)
from django.db import (
    transaction,
)

import tqdm
from corporate.factory import (
    CustomerFactory,
)
from corporate.models import (
    CustomerSubscriptionStatus,
)
from user.factory import (
    SuperUserFactory,
    UserFactory,
)
from workspace.factory import (
    ChatMessageFactory,
    LabelFactory,
    SubTaskFactory,
    TaskFactory,
    WorkspaceBoardFactory,
    WorkspaceBoardSectionFactory,
    WorkspaceFactory,
)
from workspace.models import (
    Label,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
)


class Command(BaseCommand):
    """Command."""

    N_USERS = 5

    def create_users(self) -> Optional[Sequence[AbstractBaseUser]]:
        """Create users."""
        if auth.get_user_model().objects.count():
            return None
        super_user = SuperUserFactory.create(
            email="admin@localhost",
            password="password",
        )
        guest_user = UserFactory.create(
            email="guest@localhost",
            password="password",
        )

        users: Iterable[AbstractBaseUser] = super_user, guest_user
        n_users = self.N_USERS - auth.get_user_model().objects.count()
        UserFactory.create_batch(n_users)
        users = list(auth.get_user_model().objects.all())
        return users

    N_WORKSPACES = 3
    N_WORKSPACE_BOARDS = 3
    SECTION_TITLES = [
        "Backlog",
        "To Do",
        "Ongoing",
        "Review",
        "Done",
    ]

    def create_tasks(
        self, section: WorkspaceBoardSection, labels: Sequence[Label]
    ) -> None:
        """Create tasks for a workspace board section."""
        for _ in tqdm.trange(10, desc="Tasks"):
            task = TaskFactory.create(workspace_board_section=section)
            n_labels = random.randint(0, 3)
            chosen_labels = random.choices(labels, k=n_labels)
            for label in tqdm.tqdm(chosen_labels, desc="Labels"):
                task.add_label(label)
            for _ in tqdm.trange(3, desc="Subtasks & chat messages"):
                SubTaskFactory(task=task)
                ChatMessageFactory(task=task)

    def populate_workspace_board(self, board: WorkspaceBoard) -> None:
        """Populate a workspace board."""
        labels = list(board.workspace.label_set.all())
        if board.workspaceboardsection_set.count():
            return None
        for title in tqdm.tqdm(
            self.SECTION_TITLES,
            desc="Workspace board sections",
        ):
            section = WorkspaceBoardSectionFactory.create(
                workspace_board=board,
                title=title,
            )
            self.create_tasks(section, labels)

    N_LABELS = 3

    def create_workspaces(
        self, users: Sequence[AbstractBaseUser]
    ) -> Iterable[Workspace]:
        """Create workspaces."""
        n_workspaces = self.N_WORKSPACES - Workspace.objects.count()
        for _ in tqdm.trange(n_workspaces, desc="Workspaces with users"):
            WorkspaceFactory(add_users=random.sample(users, 3))
        workspaces = Workspace.objects.all()
        for workspace in tqdm.tqdm(workspaces, desc="Workspaces"):
            n_labels = self.N_LABELS - workspace.label_set.count()
            LabelFactory.create_batch(
                n_labels,
                workspace=workspace,
            )
            n = self.N_WORKSPACE_BOARDS - workspace.workspaceboard_set.count()
            WorkspaceBoardFactory.create_batch(
                n,
                workspace=workspace,
            )
            boards = WorkspaceBoard.objects.all()
            for board in tqdm.tqdm(boards, desc="Workspace boards"):
                self.populate_workspace_board(board)
        return list(Workspace.objects.all())

    def create_corporate_accounts(
        self, workspaces: Iterable[Workspace]
    ) -> None:
        """Create corporate accounts."""
        for workspace in tqdm.tqdm(workspaces, desc="Corporate accounts"):
            if not hasattr(workspace, "customer"):
                CustomerFactory(
                    workspace=workspace,
                    subscription_status=CustomerSubscriptionStatus.ACTIVE,
                )

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        """Handle."""
        users = self.create_users()
        if not users:
            return
        workspaces = self.create_workspaces(users)
        self.create_corporate_accounts(workspaces)
