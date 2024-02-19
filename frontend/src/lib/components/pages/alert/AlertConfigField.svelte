<script lang="ts">
	import LoadingSpinner from "$lib/components/ui/LoadingSpinner.svelte";
	import { cn } from "$lib/utils/utils";

	import { Input, Label } from "flowbite-svelte";
	export let value: number;
	export let label: string;
	export let placeholder: string;
	export let isLoading: boolean;
	export let id: string;
</script>

<Label for={id} class="mb-2 block text-surface-50">{label}</Label>
<Input
	bind:value={value}
	disabled={isLoading}
	{placeholder}
	{id}
	size="lg"
  type="number"
	class={cn("border-surface-500 bg-transparent text-surface-50", {
		"ps-3": !isLoading,
	})}>
	<div slot="left">
		{#if isLoading}
			<LoadingSpinner class="text-surface-500" />
		{/if}
	</div>
</Input>
