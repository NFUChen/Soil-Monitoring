import { env } from "$env/dynamic/public";
import { getAPI } from "$lib/utils/api";
import type { GernicError } from "../commonType";
import type { DailyEnvVariable, GetDailyEnvVariableResponse } from "./type";

const baseUrl: string = env.PUBLIC_BASE_URL;

export const GetDailyEnvVariablesService = async (): Promise<DailyEnvVariable[]> => {
	try {
		const response = (await getAPI(
			"/api/report/daily_environment_variable",
			baseUrl,
		)) as GetDailyEnvVariableResponse;
		return response.data;
	} catch (error: unknown) {
		throw error as GernicError<string>;
	}
};
