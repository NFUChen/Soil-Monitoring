<script lang="ts">
	import { browser } from "$app/environment";
	import type { DailyEnvVariable, GetDailyEnvVariableResponse } from "$lib/services/report/type";
	import { cn } from "$lib/utils/utils";
	import * as echarts from "echarts";
	import { onMount } from "svelte";

	let className: string | undefined = undefined;

	export { className as class };
	export let envDatas: DailyEnvVariable[] = [];

	type EChartsOption = echarts.EChartsOption;

	let chartDom: HTMLDivElement;
	let chart: echarts.ECharts;
	let option: EChartsOption;

	const convertTimestampToTime = (timestamp: number) => {
		return new Date(timestamp).toLocaleTimeString("en-US", {
			hour: "2-digit",
			minute: "2-digit",
			second: "2-digit",
			hour12: false,
		});
	};

	onMount(() => {
		if (!browser) return;
		chart = echarts.init(chartDom);
		window.onresize = () => {
			chart.resize();
		};
	});

	$: time = envDatas.map((x) => convertTimestampToTime(x.timestamp * 1000)) ?? [];
	$: temparatureData = envDatas.map((x) => x.temperature) ?? [];
	$: humidityData = envDatas.map((x) => x.humidity) ?? [];
	$: option, option && chart?.setOption(option);
	$: option = {
		tooltip: {
			trigger: "axis",
		},
		dataZoom: [
			{
				show: true,
				realtime: true,
				start: 75,
				end: 100,
				xAxisIndex: [0, 1],
			},
		],
		grid: {
			left: "2%",
			right: "2%",
			bottom: "15%",
			containLabel: true,
		},
		legend: {
			data: ["溫度", "濕度"],
			right: 10,
			textStyle: {
				color: "hsl(0, 0%, 96%)",
			},
		},
		title: {
			text: "溫濕度圖表",
			textStyle: {
				color: "hsl(0, 0%, 96%)",
			},
		},
		xAxis: {
			splitLine: {
				show: true,
				lineStyle: {
					color: "hsl(0, 0%, 31%)",
				},
			},
			axisLine: {
				lineStyle: {
					color: "hsl(0, 0%, 43%)",
				},
			},
			type: "category",
			data: time,
		},
		yAxis: {
			splitLine: {
				lineStyle: {
					color: "hsl(0, 0%, 31%)",
				},
			},
			axisLine: {
				lineStyle: {
					color: "hsl(0, 0%, 43%)",
				},
			},
			type: "value",
			boundaryGap: [0, 0.5],
		},
		series: [
			{
				name: "溫度",
				type: "line",
				symbol: "none",
				sampling: "lttb",
				itemStyle: {
					color: "#EF562F",
				},
				data: temparatureData,
			},
			{
				name: "濕度",
				type: "line",
				symbol: "none",
				sampling: "lttb",
				itemStyle: {
					color: "#60a5fa",
				},
				data: humidityData,
			},
		],
	};
</script>

<div bind:this={chartDom} class={cn("w-full", className)} />
