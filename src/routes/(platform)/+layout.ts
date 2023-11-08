import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";

import { fetchUser, user } from "$lib/stores/user";
import type { User } from "$lib/types/user";

import type { LayoutLoadEvent } from "./$types";

export async function load({
    url,
    fetch,
}: LayoutLoadEvent): Promise<{ user: User }> {
    // For reasons, fetchuser fires twice.
    // We should have user contain some kind of hint that the user is now
    // being fetched, so we don't fetch it twice.
    const currentUser = get(user);
    if (currentUser) {
        return { user: currentUser };
    }

    const fetchedUser = await fetchUser({ fetch });

    if (fetchedUser) {
        return { user: fetchedUser };
    }

    const next = `/login?next=${url.href}`;
    console.log("Not logged in, redirecting to", next);
    throw redirect(302, next);
}
// Could we set one of the following to true here?
// Prerender: This page is completely prerenderable, there is no user data here
export const prerender = false;
// SSR, this can be prerendered
export const ssr = false;
