import type { Meta, StoryObj } from "@storybook/svelte";

import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";

import { sideNavModule, workspace } from "$lib/storybook";

const meta: Meta<SideNavContextMenu> = {
    component: SideNavContextMenu,
    argTypes: {},
    args: { workspace, sideNavModule },
};
export default meta;

type Story = StoryObj<SideNavContextMenu>;

export const Default: Story = {};
