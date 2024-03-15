// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentProject } from "$lib/stores/dashboard/project";
import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
import type {
    LabelSelection,
    TasksPerUser,
    WorkspaceUserSelection,
} from "$lib/types/ui";
import type {
    Label,
    Task,
    Section,
    SectionWithTasks,
} from "$lib/types/workspace";

interface CurrentFilter {
    labels: LabelSelection;
    workspaceUser: WorkspaceUserSelection;
    sections: SectionWithTasks[];
}

function filterSectionsTasks(
    currentFilter: CurrentFilter,
): SectionWithTasks[] {
    let sections: SectionWithTasks[] = currentFilter.sections;
    if (currentFilter.labels.kind === "noLabel") {
        // TODO filter by no label? Justus 2023-04-04
        // eslint-disable-next-line
        // Maybe: return sections;
    } else if (currentFilter.labels.kind === "allLabels") {
        // TODO what to do here?
        // eslint-disable-next-line
        // Maybe: return sections;
    } else {
        const labelUuids = [...currentFilter.labels.labelUuids.keys()];

        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.find((labelUuid) => l.uuid === labelUuid)
                            ? true
                            : false,
                    ) >= 0
                );
            });

            return { ...section, tasks };
        });
    }

    const workspaceUserSelection = currentFilter.workspaceUser;
    if (workspaceUserSelection.kind !== "allWorkspaceUsers") {
        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                if (workspaceUserSelection.kind === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee
                        ? workspaceUserSelection.workspaceUserUuids.has(
                              task.assignee.uuid,
                          )
                        : false;
                }
            });

            return { ...section, tasks };
        });
    }

    return sections;
}

export const currentSections = derived<
    [
        typeof selectedLabels,
        typeof selectedWorkspaceUser,
        typeof currentProject,
    ],
    SectionWithTasks[] | undefined
>(
    [selectedLabels, selectedWorkspaceUser, currentProject],
    (
        [$selectedLabels, $selectedWorkspaceUser, $currentProject],
        set,
    ) => {
        if (!$currentProject) {
            set(undefined);
            return;
        }
        const sections = $currentProject.sections;
        set(
            filterSectionsTasks({
                labels: $selectedLabels,
                workspaceUser: $selectedWorkspaceUser,
                sections,
            }),
        );
    },
    undefined,
);

export const tasksPerUser: Readable<TasksPerUser> = derived<
    Readable<Section[] | undefined>,
    TasksPerUser
>(
    currentSections,
    ($currentSections, set) => {
        if (!$currentSections) {
            return;
        }
        const assigned = new Map<string, number>();
        let unassigned = 0;
        $currentSections.forEach((section) => {
            if (!section.tasks) {
                return;
            }
            section.tasks.forEach((task) => {
                if (!task.assignee) {
                    unassigned = unassigned + 1;
                    return;
                }
                const uuid = task.assignee.uuid;
                assigned.set(uuid, assigned.get(uuid) ?? 0 + 1);
            });
        });
        set({ unassigned, assigned });
    },
    { unassigned: 0, assigned: new Map<string, number>() },
);
