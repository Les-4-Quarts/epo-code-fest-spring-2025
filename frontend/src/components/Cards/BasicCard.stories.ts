import BasicCard from "./BasicCard.vue";
import type { Meta, StoryObj } from "@storybook/vue3";

export default {
    title: "Components/Cards/BasicCard",
    component: BasicCard,
    tags: ["autodocs"],
    argTypes: {
        title: {
            description: "The title displayed at the top of the card.",
            control: "text",
        },
        buttonText: {
            description: "The text displayed on the button.",
            control: "text",
        },
        isLoading: {
            description: "Displays a loading spinner on the button when true.",
            control: "boolean",
        },
        disabled: {
            description: "Disables the button when true.",
            control: "boolean",
        },
        onClick: {
            description: "Event emitted when the button is clicked.",
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
} as Meta<typeof BasicCard>;

type Story = StoryObj<typeof BasicCard>;

export const Default: Story = {
    args: {
        title: "Default Card",
        buttonText: "Click Me",
        isLoading: false,
        disabled: false,
    },
    render: (args) => ({
        components: { BasicCard },
        setup() {
            return { args };
        },
        template: `
      <BasicCard v-bind="args">
        <p>This is a default card with some content inside.</p>
      </BasicCard>
    `,
    }),
};

export const Loading: Story = {
    args: {
        title: "Loading Card",
        buttonText: "Loading...",
        isLoading: true,
        disabled: false,
    },
    render: (args) => ({
        components: { BasicCard },
        setup() {
            return { args };
        },
        template: `
      <BasicCard v-bind="args">
        <p>The button is currently in a loading state.</p>
      </BasicCard>
    `,
    }),
};

export const Disabled: Story = {
    args: {
        title: "Disabled Card",
        buttonText: "Disabled",
        isLoading: false,
        disabled: true,
    },
    render: (args) => ({
        components: { BasicCard },
        setup() {
            return { args };
        },
        template: `
      <BasicCard v-bind="args">
        <p>The button is disabled and cannot be clicked.</p>
      </BasicCard>
    `,
    }),
};

export const WithoutButton: Story = {
    args: {
        title: "Card Without Button",
        buttonText: "",
        isLoading: false,
        disabled: false,
    },
    render: (args) => ({
        components: { BasicCard },
        setup() {
            return { args };
        },
        template: `
      <BasicCard v-bind="args">
        <p>This card does not have a button.</p>
      </BasicCard>
    `,
    }),
};