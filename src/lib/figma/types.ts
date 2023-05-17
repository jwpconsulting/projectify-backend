import type { User } from "$lib/types/user";
import type { Label } from "$lib/types/workspace";

export const sideMenuCreateSizes = ["extraSmall", "small"] as const;
export type SideMenuCreateSize = (typeof sideMenuCreateSizes)[number];

export const menuButtonStates = ["normal", "accordion"] as const;
export type MenuButtonState = (typeof menuButtonStates)[number];
export const menuButtonColors = ["base", "primary", "destructive"] as const;
export type MenuButtonColor = (typeof menuButtonColors)[number];
export type ButtonAction =
    | { kind: "a"; href: string }
    | { kind: "button"; action: () => void };

export const stepperPositions = ["not-last", "last"] as const;
export type StepperPosition = (typeof stepperPositions)[number];
export const stepperActiveStates = ["inactive", "this", "next"] as const;
export type StepperActiveState = (typeof stepperActiveStates)[number];

export const borderedIconTypes = ["workspace", "filter"] as const;
export type BorderedIconType = (typeof borderedIconTypes)[number];

export const boardButtonStates = ["inactive", "disabled", "active"] as const;
export type WorkspaceBoardIconState = (typeof boardButtonStates)[number];

export const avatarStateSizes = [
    "small",
    "medium",
    "large",
    "hoverable",
] as const;
export type AvatarStateSize = (typeof avatarStateSizes)[number];

export const avatarVariantSizes = [
    "small",
    "medium",
    "large",
    "hoverable",
] as const;
export type AvatarVariantSize = (typeof avatarVariantSizes)[number];
export type AvatarVariantContent =
    | { kind: "single"; user: User | null }
    | { kind: "assign"; users: [User | null, User | null] }
    | { kind: "multiple"; users: (User | null)[] };

// TODO rename me LabelContent Justus 2023-03-07
export type LabelLabel =
    | { kind: "applyLabel" }
    | { kind: "label"; label: Label };
export type SelectLabel =
    | { kind: "allLabels" }
    | { kind: "noLabel" }
    | { kind: "label"; label: Label };

export const filterLabelMenuStates = ["list", "create"] as const;
export type FilterLabelMenuState = (typeof filterLabelMenuStates)[number];

// TODO rename to InputFieldKind Justus 2022-09-22
// TODO we need to instead support "search", "erasable", and field
// subTask should use erasable
export type InputFieldStyle =
    | { kind: "search" }
    // TODO make me "erasable"
    | { kind: "subTask" }
    | { kind: "field"; inputType: "text" | "password" };
export const inputFieldSizes = ["extraSmall", "small", "normal"] as const;
export type InputFieldSize = (typeof inputFieldSizes)[number];
export interface InputFieldAnchor {
    href: string;
    label: string;
}

export const anchorSizes = ["extraSmall", "normal"] as const;
export type AnchorSize = (typeof anchorSizes)[number];

export const taskUpdateBarKinds = ["mobile", "desktop"] as const;
export type TaskUpdateBarKind = (typeof taskUpdateBarKinds)[number];
export const taskUpdateBarStates = ["task", "updates"] as const;
export type TaskUpdateBarState = (typeof taskUpdateBarStates)[number];

export const subTaskStates = ["normal", "edit"] as const;
export type SubTaskState = (typeof subTaskStates)[number];

export const floatingActionButtonIcons = ["plus", "close"] as const;
export type FloatingActionButtonIcon =
    (typeof floatingActionButtonIcons)[number];
