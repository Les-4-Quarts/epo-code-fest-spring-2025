import ErrorBox from "./ErrorBox.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Boxes/BasicBoxes",
    component: ErrorBox,
    tags: ["autodocs"],
    argTypes: {},
    parameters: {
        backgrounds: {
            default: "light",
        },
    }

} as Meta<typeof ErrorBox>;

type Story = StoryObj<typeof ErrorBox>;

export const Error: Story = {
    args: {
        default: "This is an error box.",
    },
};