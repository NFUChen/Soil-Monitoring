<script lang="ts">
	import "../lib/css/app.scss";
	import "../lib/css/scrollbar.scss";
	import type { LayoutData } from "./$types";
	import { cn } from "$lib/utils/utils";
	import { QueryClientProvider } from "@tanstack/svelte-query";
	import { browser } from "$app/environment";
	import ToastProvider from "$lib/components/ui/providers/ToastProvider.svelte";
	import { useResizeDetector } from "$lib/stores/sizeStore";
	import HeaderNav from "$lib/components/pages/layout/HeaderNav.svelte";

	export let data: LayoutData;

</script>

<div
	use:useResizeDetector
	class={cn("flex h-screen overflow-hidden bg-surface-950 text-surface-50", { hidden: !browser })}>
	<QueryClientProvider client={data.queryClient}>
		<ToastProvider />
		<div class="flex grow flex-col overflow-hidden">
			<HeaderNav />
			<slot />
		</div>
	</QueryClientProvider>
</div>
