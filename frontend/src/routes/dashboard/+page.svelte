<script>
	import TempHumidCharts from "$lib/components/pages/dashboard/TempHumidCharts.svelte";
	import ThreshHoldBar from "$lib/components/pages/dashboard/ThreshHoldBar.svelte";
	import { Button } from "flowbite-svelte";
	import { Droplet, SprayCan, Thermometer } from "lucide-svelte";

	let minTemperatureValue = 10;
	let maxTemperatureValue = 30;
	let temperatureValue = 22;

	let minHumidityValue = 20;
	let maxHumidityValue = 80;
	let humidityValue = 65;

	const randomValue = () => {
		temperatureValue =
			Math.floor(Math.random() * (maxTemperatureValue - minTemperatureValue + 1)) +
			minTemperatureValue;
	};
</script>

<div class="flex grow flex-col gap-4 overflow-y-auto p-4">
	<div class="grid shrink-0 grid-cols-1 gap-4 sm:grid-cols-2 xl:h-60 xl:grid-cols-4">
		<!-- 溫度 -->
		<div
			class="border-surface-900 col-span-2 flex flex-col border p-2 shadow-lg shadow-black/20 sm:col-span-1">
			<div class="flex grow flex-col gap-2">
				<div class="flex items-center gap-2">
					<Thermometer class="text-primary-600" />
					<p class="shrink-0">現在溫度</p>
				</div>
				<div class="flex grow items-center justify-center">
					<p class="text-7xl tracking-wide">{temperatureValue}°</p>
				</div>
				<ThreshHoldBar
					minValue={minTemperatureValue}
					maxValue={maxTemperatureValue}
					value={temperatureValue}
					color="primary-600" />
			</div>
		</div>

		<!-- 濕度 -->
		<div
			class="border-surface-900 col-span-2 flex flex-col border p-2 shadow-lg shadow-black/20 sm:col-span-1">
			<div class="flex grow flex-col gap-2">
				<div class="flex items-center gap-2">
					<Droplet class="text-blue-500" />
					<p class="shrink-0">現在濕度</p>
				</div>
				<div class="flex grow items-center justify-center">
					<p class="text-7xl tracking-wide">
						{humidityValue}
						<span class="text-4xl">%</span>
					</p>
				</div>
				<ThreshHoldBar
					minValue={minHumidityValue}
					maxValue={maxHumidityValue}
					value={humidityValue}
					color="blue-500" />
			</div>
		</div>

		<!-- 補水 -->
		<div
			class="border-surface-900 col-span-2 flex h-fit flex-col overflow-hidden border shadow-lg shadow-black/20 lg:h-auto">
			<div class="flex grow flex-col overflow-hidden">
				<div class="flex grow flex-wrap gap-4 overflow-hidden sm:flex-nowrap">
					<div class="flex flex-col overflow-hidden p-2 w-full sm:w-auto ">
						<!-- title -->
						<div class="mb-4 flex items-center gap-2">
							<SprayCan class="text-surface-100" />
							<p class="shrink-0">補水</p>
						</div>
						<!-- list -->
						<div class="flex items-center justify-center h-32 px-2 grow flex-col gap-2 self-stretch overflow-y-auto xl:h-auto">
							<div class="flex items-center">
								<div class="rounded-full bg-primary-600 square-2" />
								<p class="ml-2 text-sm">今日 20:30:30</p>
							</div>
							{#each new Array(50) as _, i}
								<p class="text-surface-300 text-sm">今日 20:30:3{i}</p>
							{/each}
						</div>
					</div>
          
          <!-- next time -->
					<div class="flex grow flex-col items-center justify-center p-2">
						<p class="mb-4">離下次</p>
						<div class="text-4xl">00:04:39</div>
					</div>

          <!-- button -->
					<div class="flex w-full sm:w-auto items-center justify-center py-2 px-4">
						<Button
							color="primary"
							class="h-16 w-full text-lg sm:aspect-square sm:rounded-full sm:square-36"
							on:click={randomValue}>補水</Button>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div
		class="border-surface-900 col-span-2 flex grow flex-col border p-2 shadow-lg shadow-black/20">
		<div class="flex grow flex-col">
			<!-- <div class="mb-2 flex items-center gap-2">
				<BarChart3 class="text-surface-100" />
				<p class="shrink-0">圖表</p>
			</div> -->
			<TempHumidCharts class="h-72 lg:grow" />
		</div>
	</div>
</div>

<style>
	@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap");
	* {
		font-family: "Montserrat", sans-serif;
	}
</style>
