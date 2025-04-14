import BasicChip from "./BasicChip.vue";
import type { Meta, StoryFn } from "@storybook/vue3";

export default {
    title: "Components/Chips/BasicChip",
    component: BasicChip,
    argTypes: {
        title: { control: "text", description: "Le texte affiché dans la puce." },
        color: { control: "color", description: "La couleur du texte de la puce." },
        bgColor: { control: "color", description: "La couleur d'arrière-plan de la puce." },
    },
} as Meta<typeof BasicChip>;

const Template: StoryFn<typeof BasicChip> = (args) => ({
    components: { BasicChip },
    setup() {
        return { args };
    },
    template: '<BasicChip v-bind="args" />',
});

export const Default = Template.bind({});
Default.args = {
    title: "Chip example",
    color: "#ffffff",
    bgColor: "#007bff",
};