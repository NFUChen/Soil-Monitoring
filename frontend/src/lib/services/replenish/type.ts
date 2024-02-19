export type WaterReplenishmentTime = {
	duration: number;
	is_done: boolean;
	target: string | null;
	timestamp: number;
};

export type WaterReplenishmentConfigResponse = {
  replenishment_times: WaterReplenishmentTime[];
};

export type SaveWaterReplenishmentConfigRequest = {
  replenishment_times: {
    timestamp: string;
    duration: number;
  }[];
};
