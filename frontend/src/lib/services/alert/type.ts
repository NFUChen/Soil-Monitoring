export type AlertThreshold = {
	temperature_threshold: {
		upper_bound: number;
		lower_bound: number;
	};
	humidity_threshold: {
		upper_bound: number;
		lower_bound: number;
	};
};

export type AlertConfigResponse = AlertThreshold;

export type SaveAlertConfigRequest = AlertThreshold;
