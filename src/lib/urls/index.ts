import type { SettingKind } from "$lib/types/dashboard";

export function getDashboardWorkspaceUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}`;
}

export function getDashboardWorkspaceBoardUrl(workspaceBoardUuid: string) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}`;
}

export function getDashboardWorkspaceBoardSectionUrl(
    workspaceBoardSectionUuid: string
) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}`;
}

export function getSettingsUrl(workspaceUuid: string, kind: SettingKind) {
    const suffix = {
        "index": "",
        "labels": "/labels",
        "workspace-users": "/workspace-users",
        "billing": "/billing",
    }[kind];
    return `/dashboard/workspace/${workspaceUuid}/settings${suffix}`;
}

export function getArchiveUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}/archive`;
}

export function getProfileUrl() {
    return "/user/profile";
}

export function getNewTaskUrl(workspaceBoardSectionUuid: string) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}/create-task`;
}

export function getTaskUrl(taskUuid: string) {
    return `/dashboard/task/${taskUuid}`;
}

export function getTaskUpdatesUrl(taskUuid: string) {
    return `/dashboard/task/${taskUuid}/updates`;
}

export function getTaskEditUrl(taskUuid: string) {
    return `/dashboard/task/${taskUuid}/update`;
}
