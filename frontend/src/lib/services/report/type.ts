export type DailyEnvVariable = {
  temperature: number;
  humidity: number;
  timestamp: number;
};

export type GetDailyEnvVariableResponse = {
  data: DailyEnvVariable[];
};
