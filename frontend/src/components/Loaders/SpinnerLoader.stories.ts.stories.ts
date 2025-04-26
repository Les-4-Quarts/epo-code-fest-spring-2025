import SpinnerLoader from "./SpinnerLoader.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Loaders/SpinnerLoader",
    component: SpinnerLoader,
    argTypes: {
        color: { control: "color", description: "The color of the spinner" },
        size: { control: "number", description: "The size of the spinner" },
    },
    parameters: {
        backgrounds: {
            default: "light",
        },
    },
} as Meta<typeof SpinnerLoader>;

type Story = StoryObj<typeof SpinnerLoader>;

export const Default: Story = {
    args: {
        color: 'var(--primary-color)',
        size: 1,
    }
};