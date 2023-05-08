import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";

import { mobileParameters, task, taskModule } from "$lib/storybook";

const meta: Meta<TaskUpdateCard> = {
    component: TaskUpdateCard,
    parameters: {
        layout: "fullscreen",
    },
    args: {
        task,
        taskModule,
    },
};
export default meta;

type Story = StoryObj<TaskUpdateCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
