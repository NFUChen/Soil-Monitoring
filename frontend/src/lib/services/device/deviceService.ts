import { env } from "$env/dynamic/public";
import { getAPI } from "$lib/utils/api";
import type { GernicError } from "../commonType";
import type { DeviceIsTurnOnResponse, DeviceTurnOnResponse } from "./type";

const baseUrl: string = env.PUBLIC_BASE_URL;

export const DeviceTurnOnService = async (): Promise<boolean> => {
	try {
		const response = (await getAPI("/api/device/turn_on", baseUrl)) as DeviceTurnOnResponse;

		if (response !== "Success") {
			throw { status: 200, message: "開啟設備失敗"}
		}

		return true;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};

export const DeviceTurnOffOnService = async (): Promise<boolean> => {
	try {
		const response = (await getAPI("/api/device/turn_off", baseUrl)) as DeviceTurnOnResponse;

		if (response !== "Success") {
			throw { status: 200, message: "關閉設備失敗"}
		}

		return true;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};

export const DeviceIsTurnOnService = async (): Promise<boolean> => {
	try {
		const response = (await getAPI("/api/device/is_turn_on", baseUrl)) as DeviceIsTurnOnResponse;

		return response.is_turn_on;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};
