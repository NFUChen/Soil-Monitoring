import { createPresistStore } from "$lib/utils/presistStore";

export type ConfigStoreType = unknown;
export const configStore = createPresistStore<ConfigStoreType>("config", {});
