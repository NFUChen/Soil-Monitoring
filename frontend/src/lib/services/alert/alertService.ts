import { env } from "$env/dynamic/public";
import { getAPI, post } from "$lib/utils/api";
import type { GernicError } from "../commonType";
import type { AlertConfigResponse, AlertThreshold, SaveAlertConfigRequest } from "./type";

const baseUrl: string = env.PUBLIC_BASE_URL;

export const GetAlertConfigService =
	async (): Promise<AlertConfigResponse> => {
		try {
			const response = (await getAPI(
				"/api/config/alert",
				baseUrl,
			)) as AlertConfigResponse;
			return response;
		} catch (error: unknown) {
			throw error as GernicError<string>;
		}
	};

export const SaveAlertConfigService = async (
	request: SaveAlertConfigRequest,
): Promise<AlertThreshold> => {
	try {
		const response = (await post(
			"/api/config/alert",
			baseUrl,
			request,
		)) as AlertThreshold;

		return response;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};
