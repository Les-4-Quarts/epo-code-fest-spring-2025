import BasicChip from "./BasicChip.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Chips/BasicChip",
    component: BasicChip,
    tags: ["autodocs"],
    argTypes: {
        title: { control: "text", description: "The title of the chip" },
        color: { control: "color", description: "The text color of the chip" },
        bgColor: { control: "color", description: "The background color of the chip" },
    },
    parameters: {
        backgrounds: {
            default: "light",
        },
    },
} as Meta<typeof BasicChip>;

type Story = StoryObj<typeof BasicChip>;

export const Default: Story = {
    args: {
        title: "Default Chip",
    },
};

export const DarkDefault: Story = {
    args: {
        title: "Dark Default Chip",
    },
    parameters: {
        backgrounds: {
            default: "dark",
        },
    },
    decorators: [
        (story) => ({
            components: { story },
            template: `<div class="dark"><story /></div>`,
        }),
    ]
};

export const CustomColor: Story = {
    args: {
        title: "Custom Color Chip",
        color: "#FFFFFF",
        bgColor: "#FF5733",
    },
};