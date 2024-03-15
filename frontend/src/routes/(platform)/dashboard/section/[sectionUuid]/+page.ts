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
import { redirect, error } from "@sveltejs/kit";

import { getSection } from "$lib/repository/workspace/section";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

export async function load({
    fetch,
    params,
}: {
    fetch: typeof window.fetch;
    params: { sectionUuid: string };
}) {
    const section = await getSection(params.sectionUuid, { fetch });
    if (!section) {
        error(404);
    }
    const project = section.project;
    redirect(302, getDashboardWorkspaceBoardUrl(project.uuid));
}
