<script lang="ts">
	import { cn } from "$lib/utils/utils";
	import { Alert } from "flowbite-svelte";
	import { AlertTriangle } from "lucide-svelte";

	export let minValue: number;
	export let maxValue: number;
	export let value: number;
	export let colorClass: string;

	let actualOffset = 0;
	const setSize = (node: HTMLDivElement) => {
		const setOffset = () => {
			const gapWidth = 16;
			node.style.gap = `${gapWidth}px`;
			const dotWidth = node.querySelector("#dot")?.getBoundingClientRect().width ?? 0;
			const minValueWidth = node.querySelector("#minValue")?.getBoundingClientRect().width ?? 0;
			const barWidth = node.querySelector("#bar")?.getBoundingClientRect().width ?? 0;
			const range = maxValue - minValue;
			const pixelPerValue = (barWidth - dotWidth) / range;

			if (value > maxValue) {
				actualOffset = minValueWidth + gapWidth + (maxValue - minValue) * pixelPerValue;
				return;
			}

			if (value < minValue) {
				actualOffset = minValueWidth + gapWidth;
				return;
			}

			actualOffset = minValueWidth + gapWidth + (value - minValue) * pixelPerValue;
		};
		setOffset();
		window.addEventListener("resize", setOffset);

		return {
			destroy() {
				window.removeEventListener("resize", setOffset);
			},
		};
	};
</script>

{#key value}
	<div use:setSize class="relative flex items-center pt-4">
		<p id="minValue" class="text-surface-200">{minValue}</p>
		<div id="bar" class="h-2 grow rounded-full bg-surface-300"></div>
		<p id="maxValue" class="text-surface-200">{maxValue}</p>
		{#if value >= minValue && value <= maxValue}
			<div
				id="dot"
				style={`left: ${actualOffset}px`}
				class={cn("absolute top-0 rounded-full transition-all square-3 ", colorClass)}>
			</div>
		{:else}
			<div id="dot" class="absolute top-0 flex square-5" style={`left: ${actualOffset}px`}>
				<AlertTriangle class="animate-bounce text-red-400" />
			</div>
		{/if}
	</div>
{/key}
