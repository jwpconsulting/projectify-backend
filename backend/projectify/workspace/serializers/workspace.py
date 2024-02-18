# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Workspace serializers."""


from . import (
    base,
)


class WorkspaceDetailSerializer(base.WorkspaceBaseSerializer):
    """
    Workspace detail serializer.

    Serializers ws board as well, but not the sections and so forth that they
    contain.
    """

    workspace_users = base.WorkspaceUserBaseSerializer(
        read_only=True, many=True, source="workspaceuser_set"
    )
    workspace_boards = base.WorkspaceBoardBaseSerializer(
        read_only=True, many=True, source="workspaceboard_set"
    )
    labels = base.LabelBaseSerializer(
        read_only=True, many=True, source="label_set"
    )

    class Meta(base.WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBaseSerializer.Meta.fields,
            "workspace_users",
            "workspace_boards",
            "labels",
        )
