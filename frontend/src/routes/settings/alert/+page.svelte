<script lang="ts">
	import AlertConfigField from "$lib/components/pages/alert/AlertConfigField.svelte";
	import LoadingSpinner from "$lib/components/ui/LoadingSpinner.svelte";
	import { addToast } from "$lib/components/ui/providers/ToastProvider.svelte";
	import { GetAlertConfigService, SaveAlertConfigService } from "$lib/services/alert/alertService";
	import { createMutation, createQuery } from "@tanstack/svelte-query";
	import { Button } from "flowbite-svelte";
	import _ from "lodash";
	import { onMount } from "svelte";
	import { parse } from "svelte/compiler";

	let maxTemperatureValue = 0;
	let minTemperatureValue = 0;
	let maxHumidityValue = 0;
	let minHumidityValue = 0;

	const getAlertConfigMutation = createMutation({
		mutationKey: ["alertConfig"],
		mutationFn: GetAlertConfigService,
	});

	const saveAlertConfigMutation = createMutation({
		mutationKey: ["saveAlertConfig"],
		mutationFn: SaveAlertConfigService,
	});

	const onSaveAlertConfig = async () => {
		maxTemperatureValue = Number(maxTemperatureValue);
		minTemperatureValue = Number(minTemperatureValue);
		maxHumidityValue = Number(maxHumidityValue);
		minHumidityValue = Number(minHumidityValue);	
		if (maxTemperatureValue < minTemperatureValue) {
			addToast({
				content: "溫度閾值上限不可小於下限",
				type: "error",
			});
			return;
		}

		if (maxHumidityValue < minHumidityValue) {
			addToast({
				content: "濕度閾值上限不可小於下限",
				type: "error",
			});
			return;
		}

		await $saveAlertConfigMutation.mutateAsync(
			{
				temperature_threshold: {
					upper_bound: maxTemperatureValue,
					lower_bound: minTemperatureValue,
				},
				humidity_threshold: {
					upper_bound: maxHumidityValue,
					lower_bound: minHumidityValue,
				},
			},
			{
				onSuccess: (data) => {
					maxTemperatureValue = data.temperature_threshold.upper_bound;
					minTemperatureValue = data.temperature_threshold.lower_bound;
					maxHumidityValue = data.humidity_threshold.upper_bound;
					minHumidityValue = data.humidity_threshold.lower_bound;
					addToast({
						content: "警示閾值已儲存",
						type: "success",
					});
				},
			},
		);
	};

	const initData = async () => {
		const data = await $getAlertConfigMutation.mutateAsync();
		maxTemperatureValue = data.temperature_threshold.upper_bound;
		minTemperatureValue = data.temperature_threshold.lower_bound;
		maxHumidityValue = data.humidity_threshold.upper_bound;
		minHumidityValue = data.humidity_threshold.lower_bound;
	};

	onMount(() => {
		initData();
	});

	$: isLoading = $getAlertConfigMutation.isPending || $saveAlertConfigMutation.isPending;
</script>

<div class="flex grow flex-col overflow-hidden p-4">
	<div
		class="flex flex-col overflow-hidden border border-t-4 border-surface-700 border-t-primary-600">
		<div class="flex items-center gap-2 border-b border-surface-700 px-4 py-2">
			溫濕度警示閾值
			<Button on:click={onSaveAlertConfig} class="ml-auto">
				{#if isLoading}
					<LoadingSpinner />
				{:else}
					儲存
				{/if}
			</Button>
		</div>
		<div class="overflow-y-auto">
			<div class="border-b border-surface-700 p-4">
				<div class="mb-4 flex items-center">
					<p>溫度</p>
				</div>
				<div class="mb-6">
					<AlertConfigField
						{isLoading}
						bind:value={maxTemperatureValue}
						label="警告上限"
						placeholder="請輸入溫度閾值上限"
						id="max-temperature" />
				</div>
				<div class="mb-6">
					<AlertConfigField
						{isLoading}
						bind:value={minTemperatureValue}
						label="警告下限"
						placeholder="請輸入溫度閾值下限"
						id="min-temperature" />
				</div>
			</div>
			<div class="p-4">
				<div class="mb-4 flex items-center">
					<p>濕度</p>
				</div>
				<div class="mb-6">
					<AlertConfigField
						{isLoading}
						bind:value={maxHumidityValue}
						label="警告上限"
						placeholder="請輸入濕度閾值上限"
						id="max-humidity" />
				</div>
				<div class="mb-6">
					<AlertConfigField
						{isLoading}
						bind:value={minHumidityValue}
						label="警告下限"
						placeholder="請輸入濕度閾值下限"
						id="min-humidity" />
				</div>
			</div>
		</div>
	</div>
</div>
