import { env } from "$env/dynamic/public";
import { getAPI, post } from "$lib/utils/api";
import type { GernicError } from "../commonType";
import type {
	WaterReplenishmentConfigResponse,
	SaveWaterReplenishmentConfigRequest,
} from "./type";

const baseUrl: string = env.PUBLIC_BASE_URL;

export const GetWaterReplenishmentConfigService =
	async (): Promise<WaterReplenishmentConfigResponse> => {
		try {
			const response = (await getAPI(
				"/api/config/water_replenishment",
				baseUrl,
			)) as WaterReplenishmentConfigResponse;
			return response;
		} catch (error: unknown) {
			throw error as GernicError<string>;
		}
	};

export const SaveWaterReplenishmentConfigService = async (
	request: SaveWaterReplenishmentConfigRequest,
): Promise<WaterReplenishmentConfigResponse> => {
	try {
		const response = (await post(
			"/api/config/water_replenishment",
			baseUrl,
			request,
		)) as WaterReplenishmentConfigResponse;

		return response;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};
