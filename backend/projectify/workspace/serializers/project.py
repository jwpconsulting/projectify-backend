# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Project serializers."""
from rest_framework import serializers

from projectify.workspace.models.project import Project
from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from projectify.workspace.serializers.base import (
    LabelBaseSerializer,
    ProjectBaseSerializer,
    SubTaskBaseSerializer,
    TeamMemberBaseSerializer,
    WorkspaceBaseSerializer,
)


class TaskSerializer(serializers.ModelSerializer[Task]):
    """Serialize all task details."""

    labels = LabelBaseSerializer(many=True, read_only=True)
    assignee = TeamMemberBaseSerializer(read_only=True)
    # TODO Justus 2024-04-09
    # This can be simplified as well, might only have to return completion
    # percentage
    sub_tasks = SubTaskBaseSerializer(
        many=True, read_only=True, source="subtask_set"
    )

    class Meta:
        """Meta."""

        # Leaving out created, updated, _order, and description
        model = Task
        fields = (
            "title",
            "uuid",
            "due_date",
            "number",
            "labels",
            "assignee",
            "sub_tasks",
        )


class SectionSerializer(serializers.ModelSerializer[Section]):
    """Reduced section serializer."""

    tasks = TaskSerializer(many=True, read_only=True, source="task_set")

    class Meta:
        """Meta."""

        model = Section
        fields = (
            "uuid",
            "_order",
            "title",
            "tasks",
        )


class ProjectDetailSerializer(ProjectBaseSerializer):
    """
    Project serializer.

    Serializes in both directions, workspace and sections, including their
    tasks.
    """

    sections = SectionSerializer(
        many=True, read_only=True, source="section_set"
    )

    workspace = WorkspaceBaseSerializer(read_only=True)

    class Meta(ProjectBaseSerializer.Meta):
        """Meta."""

        model = Project
        fields = (
            *ProjectBaseSerializer.Meta.fields,
            "sections",
            "workspace",
        )
