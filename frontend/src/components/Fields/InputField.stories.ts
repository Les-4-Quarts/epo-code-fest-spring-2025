import InputField from "./InputField.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Fields/InputField",
    component: InputField,
    argTypes: {
        label: {
            description: "The label displayed above the input field.",
            control: "text",
        },
        placeholder: {
            description: "Placeholder text for the input field.",
            control: "text",
        },
        type: {
            description: "The type of the input field (e.g., text, password, email).",
            control: "text",
        },

    },
    parameters: {
        backgrounds: {
            default: "light",
        },
    },
} as Meta<typeof InputField>;

type Story = StoryObj<typeof InputField>;

export const Default: Story = {
    args: {
        label: "Default Input",
        placeholder: "Enter text here...",
        type: "text",
    },
};

export const Password: Story = {
    args: {
        label: "Password Input",
        placeholder: "Enter password here...",
        type: "password",
    },
};
export const Email: Story = {
    args: {
        label: "Email Input",
        placeholder: "Enter email here...",
        type: "email",
    },
};