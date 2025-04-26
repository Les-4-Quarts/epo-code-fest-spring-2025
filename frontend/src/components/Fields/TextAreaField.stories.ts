import TextAreaField from "./TextAreaField.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Fields/TextAreaField",
    component: TextAreaField,
    argTypes: {
        label: {
            description: "The label displayed above the text area.",
            control: "text",
        },
        placeholder: {
            description: "Placeholder text for the text area.",
            control: "text",
        },
    },
    parameters: {
        backgrounds: {
            default: "light",
        },
    },
} as Meta<typeof TextAreaField>;

type Story = StoryObj<typeof TextAreaField>;

export const Default: Story = {
    args: {
        label: "Default Text Area",
        placeholder: "Enter text here...",
    },
};