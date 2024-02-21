<script context="module" lang="ts">
	import { env } from "$env/dynamic/public";
	import io from "socket.io-client";

	const baseUrl: string = env.PUBLIC_BASE_URL;
	export const socket = io(baseUrl, {
		autoConnect: false,
		extraHeaders: {
			"ngrok-skip-browser-warning": "true",
		},
	});
</script>

<script lang="ts">
	import CheckSuccess from "$lib/components/pages/dashboard/CheckSuccess.svelte";
	import TempHumidCharts from "$lib/components/pages/dashboard/TempHumidCharts.svelte";
	import ThreshHoldBar from "$lib/components/pages/dashboard/ThreshHoldBar.svelte";
	import { addToast } from "$lib/components/ui/providers/ToastProvider.svelte";
	import {
		DeviceIsTurnOnService,
		DeviceTurnOffOnService,
		DeviceTurnOnService,
	} from "$lib/services/device/deviceService";
	import { GetWaterReplenishmentConfigService } from "$lib/services/replenish/replenishService";
	import { cn } from "$lib/utils/utils";
	import { createMutation, createQuery } from "@tanstack/svelte-query";
	import { Button, Skeleton } from "flowbite-svelte";
	import { Droplet, SprayCan, Thermometer } from "lucide-svelte";
	import { secondTohhmmss } from "$lib/utils/secondTohhmmss";
	import { afterUpdate, onDestroy, onMount, tick } from "svelte";
	import type { WaterReplenishmentTime } from "$lib/services/replenish/type";
	import { GetAlertConfigService } from "$lib/services/alert/alertService";
	import _ from "lodash";
	import { GetDailyEnvVariablesService } from "$lib/services/report/reportService";

	// ======
	let minTemperatureValue = 0;
	let maxTemperatureValue = 0;
	let temperatureValue = 0;

	let minHumidityValue = 0;
	let maxHumidityValue = 0;
	let humidityValue = 0;
	// ======

	let isTemperatureAlert = false;
	let isHumidityAlert = false;
	let isPreventClicking = false;
	let nextRemainSeconds = 0;
	let replenishmentTimes: WaterReplenishmentTime[] = [];
	let nextRemainInterval: number;
	let currentReplenishmentTime: WaterReplenishmentTime | undefined;

	const deviceIsTurnOnQuery = createQuery({
		queryKey: ["deviceIsTurnOn"],
		queryFn: DeviceIsTurnOnService,
	});

	const getDailyEnvVariablesQuery = createQuery({
		queryKey: ["dailyEnvVariables"],
		queryFn: GetDailyEnvVariablesService,
		refetchInterval: 1000 * 60,
	});

	const getAlertConfigMutation = createMutation({
		mutationKey: ["alertConfig"],
		mutationFn: GetAlertConfigService,
	});

	const getWaterReplenishmentConfigMutation = createMutation({
		mutationKey: ["waterReplenishmentConfig"],
		mutationFn: GetWaterReplenishmentConfigService,
	});

	const deviceTurnOnMutation = createMutation({
		mutationKey: ["deviceTunrOn"],
		mutationFn: DeviceTurnOnService,
	});

	const deviceTurnOffMutation = createMutation({
		mutationKey: ["deviceTunrOff"],
		mutationFn: DeviceTurnOffOnService,
	});

	const hideTemperatureAlert = _.debounce((value: number) => {
		isTemperatureAlert = false;
	}, 3000);

	const hideHumidityAlert = _.debounce((value: number) => {
		isHumidityAlert = false;
	}, 3000);

	const onTurnOnDevice = async () => {
		if (isPreventClicking) return;
		isPreventClicking = true;

		if (isDeviceTurnOn) {
			// turn off the device
			await $deviceTurnOffMutation.mutateAsync(undefined, {
				onSuccess: async () => {
					addToast({
						content: "補水已關閉",
						type: "success",
					});
					await $deviceIsTurnOnQuery.refetch();
					setTimeout(() => {
						isPreventClicking = false;
					}, 3000);
				},
			});
			return;
		}
		// turn on the device
		await $deviceTurnOnMutation.mutateAsync(undefined, {
			onSuccess: async () => {
				addToast({
					content: "補水成功",
					type: "success",
				});
				await $deviceIsTurnOnQuery.refetch();
				setTimeout(() => {
					isPreventClicking = false;
				}, 3000);
			},
		});
	};

	const getNextReplenishmentTime = () => {
		const start = new Date();
		start.setHours(0, 0, 0, 0);
		const now = new Date();
		const nowSeconds = (now.getTime() - start.getTime()) / 1000;
		const toNextTimeRemainSeconds = (currentReplenishmentTime?.timestamp ?? 0) - nowSeconds;
		if (toNextTimeRemainSeconds <= 0) {
			return 0;
		}
		return toNextTimeRemainSeconds;
	};

	const initAlertConfig = async () => {
		const alertConfigResponse = await $getAlertConfigMutation.mutateAsync(undefined);
		const { temperature_threshold, humidity_threshold } = alertConfigResponse;
		minTemperatureValue = temperature_threshold.lower_bound;
		maxTemperatureValue = temperature_threshold.upper_bound;
		minHumidityValue = humidity_threshold.lower_bound;
		maxHumidityValue = humidity_threshold.upper_bound;
	};

	const getReplenishmentTimes = async () => {
		const response = await $getWaterReplenishmentConfigMutation.mutateAsync(undefined);
		replenishmentTimes = response.replenishment_times;
	};

	const initReplenish = async () => {
		// get replenishment times
		await getReplenishmentTimes();
		if (replenishmentTimes.length) {
			nextRemainSeconds = getNextReplenishmentTime();

			nextRemainInterval = setInterval(async () => {
				// if no remain time, clear interval
				if (remainReplenishmentTimes.length === 0) {
					clearInterval(nextRemainInterval);
					return;
				}

				nextRemainSeconds--;
				// if this turn is done, get next turn
				if (nextRemainSeconds <= 0) {
					await refetchDeviceTurnOnAfterTimeout((currentReplenishmentTime?.duration ?? 0) * 1000);
					await getReplenishmentTimes();
					scrollToNextTime();
					nextRemainSeconds = getNextReplenishmentTime();
				}
			}, 1000);
		}
	};

	const refetchDeviceTurnOnAfterTimeout = async (timeout: number) => {
		await $deviceIsTurnOnQuery.refetch();
		setTimeout(() => {
			$deviceIsTurnOnQuery.refetch();
		}, timeout);
	};

	const scrollToNextTime = () => {
		setTimeout(() => {
			const nextTime = document.getElementById(`t-${currentReplenishmentTime?.timestamp}`);
			const nextTimeParent = nextTime?.parentElement;
			if (nextTime && nextTimeParent) {
				const offsetTop = nextTime.offsetTop - nextTimeParent.offsetTop - nextTimeParent.clientHeight + nextTime.clientHeight;
				nextTimeParent.scrollTo({
					top: offsetTop,
					behavior: "smooth",
				});
			}
		}, 100);
	};

	onMount(async () => {
		await Promise.all([initAlertConfig(), initReplenish()]);

		scrollToNextTime();

		// connect to socket
		socket.connect();

		socket.on("sensor", (data: string) => {
			const { temperature, humidity } = JSON.parse(data);
			temperatureValue = temperature;
			humidityValue = humidity;
		});

		socket.on("alert/temperature", (data: string) => {
			if (data) {
				isTemperatureAlert = true;
				hideTemperatureAlert(temperatureValue);
			}
		});

		socket.on("alert/humidity", (data: string) => {
			if (data) {
				isHumidityAlert = true;
				hideHumidityAlert(humidityValue);
			}
		});
	});

	onDestroy(() => {
		clearInterval(nextRemainInterval);
		socket.offAny();
		socket.disconnect();
	});

	$: remainReplenishmentTimes = replenishmentTimes.filter((time) => !time.is_done) ?? [];
	$: currentReplenishmentTime = remainReplenishmentTimes[0] || undefined;
	$: isDeviceTurnOn = $deviceIsTurnOnQuery.data;
	$: replenishLabel = isDeviceTurnOn ? "開啟" : "關閉";
</script>

<div class="flex grow flex-col gap-4 overflow-y-auto p-4">
	<div class="grid shrink-0 grid-cols-1 gap-4 sm:grid-cols-2 xl:h-60 xl:grid-cols-4">
		<!-- 溫度 -->
		<div
			class="col-span-2 flex flex-col border border-surface-900 p-2 shadow-lg shadow-black/20 sm:col-span-1">
			<div class="flex grow flex-col gap-2">
				<div class="flex items-center gap-2">
					<Thermometer class="text-primary-600" />
					<p class="shrink-0">現在溫度</p>
				</div>
				<div class="flex grow items-center justify-center">
					<p
						class={cn("text-7xl tracking-wide", {
							"text-red-400": isTemperatureAlert,
						})}>
						{temperatureValue}°
					</p>
				</div>
				<ThreshHoldBar
					minValue={minTemperatureValue}
					maxValue={maxTemperatureValue}
					value={temperatureValue}
					colorClass="bg-surface-50" />
			</div>
		</div>

		<!-- 濕度 -->
		<div
			class="col-span-2 flex flex-col border border-surface-900 p-2 shadow-lg shadow-black/20 sm:col-span-1">
			<div class="flex grow flex-col gap-2">
				<div class="flex items-center gap-2">
					<Droplet class="text-blue-500" />
					<p class="shrink-0">現在濕度</p>
				</div>
				<div class="flex grow items-center justify-center">
					<p
						class={cn("text-7xl tracking-wide", {
							"text-red-400": isHumidityAlert,
						})}>
						{humidityValue}
						<span class="text-4xl">%</span>
					</p>
				</div>
				<ThreshHoldBar
					minValue={minHumidityValue}
					maxValue={maxHumidityValue}
					value={humidityValue}
					colorClass="bg-surface-50" />
			</div>
		</div>

		<!-- 補水 -->
		<div
			class="col-span-2 flex h-fit flex-col overflow-hidden border border-surface-900 shadow-lg shadow-black/20 lg:h-auto">
			<div class="flex grow flex-col overflow-hidden">
				<div class="flex grow flex-wrap gap-4 overflow-hidden sm:flex-nowrap">
					<div class="flex w-full flex-col overflow-hidden p-2 sm:w-1/4">
						<!-- title -->
						<div class="mb-4 flex items-center gap-2">
							<SprayCan class="text-surface-100" />
							<p class="shrink-0">補水</p>
						</div>
						<!-- list -->
						<div class="mb-2 grid grid-cols-2 px-2 text-sm text-surface-300">
							<p>時間</p>
							<p class="text-center">持續</p>
						</div>
						<div class="flex h-32 grow flex-col gap-2 self-stretch overflow-y-auto px-2 xl:h-auto">
							{#if $getWaterReplenishmentConfigMutation.isPending}
								<div class="flex flex-col gap-3">
									{#each new Array(5) as _}
										<div class="h-4 w-full animate-pulse rounded-md bg-surface-700" />
									{/each}
								</div>
							{:else}
								{#each replenishmentTimes as time, i}
									<div
										id={`t-${time.timestamp}`}
										class={cn("grid grid-cols-2 text-sm tracking-wide text-surface-200", {
											"text-surface-700": time.is_done,
											"animate-pulse font-bold":
												time.timestamp === currentReplenishmentTime?.timestamp,
										})}>
										<p class="">{secondTohhmmss(time.timestamp)}</p>
										<p class="text-center">{time.duration}</p>
									</div>
								{/each}
							{/if}
						</div>
					</div>

					<!-- next time -->
					<div class="flex grow flex-col items-center justify-center p-2">
						<p class="mb-4">離下次</p>
						<div class="text-4xl">
							{#if $getWaterReplenishmentConfigMutation.isPending}
								<div class="h-16 w-60 animate-pulse rounded-lg bg-surface-700" />
							{:else}
								{secondTohhmmss(nextRemainSeconds)}
							{/if}
						</div>
					</div>

					<!-- button -->
					<div class="flex w-full flex-col items-center justify-center px-4 py-2 sm:w-auto">
						<Button
							color="primary"
							class={cn(
								"h-16 w-full overflow-hidden p-0 text-lg sm:aspect-square sm:rounded-full sm:square-36",
								{
									" hover:bg-primary-700": isPreventClicking,
									"bg-blue-600 hover:bg-blue-700": isDeviceTurnOn,
									"hover:bg-blue-700": isPreventClicking && isDeviceTurnOn,
								},
							)}
							on:click={onTurnOnDevice}>
							{#if isPreventClicking}
								<CheckSuccess
									circleClass={isDeviceTurnOn ? "fill-blue-600" : "fill-primary-600"}
									strokeClass={isDeviceTurnOn ? "stroke-blue-600" : "stroke-primary-600"} />
							{:else}
								<div>
									<p class="mb-2">手動補水</p>
									<p class="text-xs">狀態：{replenishLabel}</p>
								</div>
							{/if}
						</Button>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div
		class="col-span-2 flex grow flex-col border border-surface-900 p-2 shadow-lg shadow-black/20">
		<div class="flex grow flex-col">
			<TempHumidCharts
				envDatas={$getDailyEnvVariablesQuery.data ?? []}
				class="h-72 overflow-hidden lg:grow" />
		</div>
	</div>
</div>

<style>
	@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap");
	* {
		font-family: "Montserrat", sans-serif;
	}
</style>
