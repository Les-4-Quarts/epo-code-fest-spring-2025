import BasicBox from "./BasicBox.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Boxes/BasicBoxes",
    component: BasicBox,
    tags: ["autodocs"],
    argTypes: {
        title: { control: "text", description: "The title of the box" },
        color: { control: "color", description: "The color of the box" },
        bgColor: { control: "color", description: "The background color of the box" },
        icon: { control: "text", description: "The icon to display in the box. Must be part of '@mdi/js'" },
    },
    parameters: {
        backgrounds: {
            default: "light",
        },
    }

} as Meta<typeof BasicBox>;

type Story = StoryObj<typeof BasicBox>;

export const Default: Story = {
    args: {
        title: "Default Box",
        default: "This is a default box.",
    },
};