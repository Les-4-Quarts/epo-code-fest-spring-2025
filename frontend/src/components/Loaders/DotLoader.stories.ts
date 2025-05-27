import DotLoader from "./DotLoader.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Loaders/DotLoader",
    component: DotLoader,
    tags: ["autodocs"],
    argTypes: {},
    parameters: {
        backgrounds: {
            default: "light",
        },
    },
} as Meta<typeof DotLoader>;

type Story = StoryObj<typeof DotLoader>;

export const Default: Story = {};