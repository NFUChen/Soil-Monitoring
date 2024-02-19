<script lang="ts">
	import { browser } from "$app/environment";
	import { cn } from "$lib/utils/utils";
	import * as echarts from "echarts";
	import { onMount } from "svelte";

	let className: string | undefined = undefined;

	export { className as class };

	type EChartsOption = echarts.EChartsOption;

	let chartDom: HTMLDivElement;
	let option: EChartsOption;

	let halfHour = 30 * 60 * 1000;
	let time = [];
	let temparatureData = [];
	let humidityData = [];

	for (let i = 1; i <= 48; i++) {
		// get today every half hour since  00:00
		const now = new Date();
		const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
		const t = new Date(today.getTime() + i * halfHour);
		// 20 - 40 degrees random
		const temp = Math.floor(Math.random() * (40 - 30 + 1)) + 30;
		const humid = Math.floor(Math.random() * (70 - 50 + 1)) + 50;

		time.push(t.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false }));
		temparatureData.push(temp);
		humidityData.push(humid);
	}

	option = {
		tooltip: {
			trigger: "axis",
			position: function (pt) {
				return [pt[0], "10%"];
			},
		},
		grid: {
			left: "2%",
			right: "2%",
			bottom: "2%",
			containLabel: true,
		},
		legend: {
			data: ["溫度", "濕度"],
			right: 10,
      textStyle: {
        color: 'hsl(0, 0%, 96%)'
      }
		},
    title: {
      text: '溫濕度圖表',
      textStyle: {
        color: 'hsl(0, 0%, 96%)'
      }
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
			boundaryGap: [0, 0.05],
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
			boundaryGap: [0, 0.2],
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

	onMount(() => {
		const myChart = echarts.init(chartDom);
		option && myChart.setOption(option);

		if (!browser) return;

		window.onresize = () => {
			myChart.resize();
		};
	});
</script>

<div bind:this={chartDom} class={cn("w-full", className)} />
