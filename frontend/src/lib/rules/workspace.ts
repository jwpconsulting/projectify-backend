// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK

import type {
    WorkspaceQuota,
    WorkspaceDetailTeamMember,
    TeamMemberRole,
} from "$lib/types/workspace";

/**
 * Functions for permission checking, see rules in Django backend
 *
 * The permission checking is not security relevant and only serves cosmetic
 * purposes. We check for the actual permissions in the backend, but would not
 * like to offer the user to perform actions that will then just fail in the
 * backend when making an API request.
 */
export type Verb = "create" | "read" | "update" | "delete";
export type Resource =
    | "workspace"
    | "teamMemberInvite"
    | "teamMember"
    | "project"
    | "section"
    | "task"
    | "label"
    | "taskLabel"
    | "subTask"
    | "chatMessage"
    | "customer";

type CrudMinimumRole = {
    [K in Verb]: TeamMemberRole;
};

type Rules = {
    [K in Resource]: CrudMinimumRole;
};

/**
 * Referencing docs/rules.md
| Resource                | Create     | Read       | Update     | Delete     |
|-------------------------|------------|------------|------------|------------|
| Workspace               | Owner      | Observer   | Owner      | Owner      |
| Team member invite   | Owner      | Owner      | Owner      | Owner      |
| Team member          | Owner      | Observer   | Owner      | Owner      |
| Project         | Maintainer | Observer   | Maintainer | Maintainer |
| Section | Maintainer | Observer   | Maintainer | Maintainer |
| Task                    | Contributor     | Observer   | Contributor     | Maintainer |
| Label                   | Maintainer | Observer   | Maintainer | Maintainer |
| Task label              | Contributor     | Observer   | Contributor     | Contributor     |
| Sub task                | Contributor     | Observer   | Contributor     | Contributor     |
| Chat message            | Contributor     | Observer   | Contributor     | Maintainer |
| Customer                | Owner      | Owner      | Owner      | Owner      |
 */

const rules: Rules = {
    workspace: {
        create: "OWNER",
        read: "OBSERVER",
        update: "OWNER",
        delete: "OWNER",
    },
    teamMemberInvite: {
        create: "OWNER",
        read: "OWNER",
        update: "OWNER",
        delete: "OWNER",
    },
    teamMember: {
        create: "OWNER",
        read: "OBSERVER",
        update: "OWNER",
        delete: "OWNER",
    },
    project: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    section: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    task: {
        create: "CONTRIBUTOR",
        read: "OBSERVER",
        update: "CONTRIBUTOR",
        delete: "MAINTAINER",
    },
    label: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    taskLabel: {
        create: "CONTRIBUTOR",
        read: "OBSERVER",
        update: "CONTRIBUTOR",
        delete: "CONTRIBUTOR",
    },
    subTask: {
        create: "CONTRIBUTOR",
        read: "OBSERVER",
        update: "CONTRIBUTOR",
        delete: "CONTRIBUTOR",
    },
    chatMessage: {
        create: "CONTRIBUTOR",
        read: "OBSERVER",
        update: "CONTRIBUTOR",
        delete: "MAINTAINER",
    },
    customer: {
        create: "OWNER",
        read: "OWNER",
        update: "OWNER",
        delete: "OWNER",
    },
};

/**
 * Total ordering for roles. For a given role, is this role at least $ROLE?
 */
const isAtLeast: {
    [K in TeamMemberRole]: { [K in TeamMemberRole]: boolean };
} = {
    OBSERVER: {
        OBSERVER: true,
        CONTRIBUTOR: false,
        MAINTAINER: false,
        OWNER: false,
    },
    CONTRIBUTOR: {
        OBSERVER: true,
        CONTRIBUTOR: true,
        MAINTAINER: false,
        OWNER: false,
    },
    MAINTAINER: {
        OBSERVER: true,
        CONTRIBUTOR: true,
        MAINTAINER: true,
        OWNER: false,
    },
    OWNER: {
        OBSERVER: true,
        CONTRIBUTOR: true,
        MAINTAINER: true,
        OWNER: true,
    },
};

/**
 * Map resource name to quota key in WorkspaceQuota
 * If no quota exists for a resource, map to undefined.
 * For example, no quota exists on workspaces themselves, since they exist
 * independently of a workspace.
 */
const resourceToQuota: {
    [K in Resource]:
        | keyof Omit<WorkspaceQuota, "workspace_status">
        | undefined;
} = {
    workspace: undefined,
    teamMemberInvite: "team_members_and_invites",
    teamMember: "team_members_and_invites",
    project: "projects",
    section: "sections",
    task: "tasks",
    label: "labels",
    taskLabel: "task_labels",
    subTask: "sub_tasks",
    chatMessage: "chat_messages",
    customer: undefined,
};

function canCreateMore(resource: Resource, quota: WorkspaceQuota): boolean {
    const quotaKey = resourceToQuota[resource];
    // Short circuit for undefined quotaKey
    if (quotaKey === undefined) {
        return true;
    }
    const resourceQuota = quota[quotaKey];
    return resourceQuota.can_create_more;
}

// TODO check trial limits as well for create actions
export function can(
    verb: Verb,
    resource: Resource,
    { role }: Pick<WorkspaceDetailTeamMember, "role">,
    quota: WorkspaceQuota,
): boolean {
    // 1. Check permission
    const minimum = rules[resource][verb];
    const hasMiniminumRole = isAtLeast[role][minimum];
    // 2. Check quota if create
    const withinQuota =
        verb === "create" ? canCreateMore(resource, quota) : true;
    return hasMiniminumRole && withinQuota;
}
