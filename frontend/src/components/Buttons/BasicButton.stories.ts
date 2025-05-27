import BasicButton from "./BasicButton.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Buttons/BasicButton",
    component: BasicButton,
    tags: ["autodocs"],
    argTypes: {
        text: {
            description: "The text to display on the button.",
            control: "text",
        },
        color: {
            description: "The text color of the button.",
            control: "color",
        },
        bgColor: {
            description: "The background color of the button.",
            control: "color",
        },
        icon: {
            description: "The icon to display on the button. Must be part of '@mdi/js'",
            control: "text",
        },
        iconSize: {
            description: "The size of the icon.",
            control: { type: "number", min: 16, max: 64, step: 1 },
        },
        activeColor: {
            description: "The text color when the button is active.",
            control: "color",
        },
        activeBgColor: {
            description: "The background color when the button is active.",
            control: "color",
        },
        isActive: {
            description: "Indicates if the button is active.",
            control: "boolean",
        },
        isLoading: {
            description: "Indicates if the button is in a loading state.",
            control: "boolean",
        },
        disabled: {
            description: "Indicates if the button is disabled.",
            control: "boolean",
        },
        to: {
            description: "The URL to navigate to when the button is clicked. If provided, the button will act as a link.",
            control: "text",
        },
        onClick: {
            description: "The function to call when the button is clicked.",
            action: "click",
        },
    },
    parameters: {
        backgrounds: {
            default: "light",
            values: [
                { name: "light", value: "#ffffff" },
                { name: "dark", value: "#333333" },
            ],
        },
    },
} as Meta<typeof BasicButton>;

type Story = StoryObj<typeof BasicButton>;

export const Default: Story = {
    args: {
        text: "Default Button",
    },
};

export const Active: Story = {
    args: {
        text: "Active Button",
        color: "white",
        bgColor: "blue",
        activeColor: "white",
        activeBgColor: "darkblue",
        isActive: true,
    },
};

export const Loading: Story = {
    args: {
        text: "Loading Button",
        color: "white",
        bgColor: "gray",
        isLoading: true,
    },
};

export const Disabled: Story = {
    args: {
        text: "Disabled Button",
        color: "white",
        bgColor: "gray",
        disabled: true,
    },
};

export const WithIcon: Story = {
    args: {
        text: "Button with Icon",
        color: "white",
        bgColor: "green",
        icon: "mdiCheck",
        iconSize: 24,
    },
};

export const OnlyIcon: Story = {
    args: {
        color: "white",
        bgColor: "green",
        icon: "mdiCheck",
        iconSize: 24,
    },
};

export const LinkButton: Story = {
    args: {
        text: "Link Button",
        color: "white",
        bgColor: "purple",
        to: "/example",
    },
};