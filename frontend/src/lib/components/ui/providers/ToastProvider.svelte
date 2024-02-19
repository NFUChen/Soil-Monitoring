<script lang="ts" context="module">
	export type ToastData = {
		content?: string;
		type: "success" | "error" | "info";
	};
	const toastStore = easyStore<ToastData | undefined>({
		value: undefined,
	});

	export const addToast = (toast: ToastData) => toastStore.set(toast);
	const closeToast = () => toastStore.set(undefined);
</script>

<script lang="ts">
	import { Toast } from "flowbite-svelte";
	import { CheckCircle2, XCircle, AlertCircle } from "lucide-svelte";
	import { easyStore } from "$lib/utils/easyStore";
	import { blur } from "svelte/transition";
	import { debounce } from "$lib/utils/utils";

	const close = debounce(() => closeToast(), 5000);

	toastStore.subscribe((value) => {
		if (value) {
			close();
		}
	});

	$: toastType = $toastStore?.type;
	$: content = $toastStore?.content;
</script>

<div
	class="fixed bottom-0 left-1/2 z-[9999] m-4 flex -translate-x-1/2 flex-col items-end gap-2 md:top-auto">
	{#if toastType === "success"}
		<div transition:blur>
			<Toast on:close={closeToast} color="green">
				<svelte:fragment slot="icon">
					<CheckCircle2 class="square-5" />
					<span class="sr-only">Check icon</span>
				</svelte:fragment>
				<p class="w-max max-w-[200px] break-all">{ content }</p>
			</Toast>
		</div>
	{:else if toastType === "error"}
		<div transition:blur>
			<Toast on:close={closeToast} color="red">
				<svelte:fragment slot="icon">
					<XCircle class="suqare-5" />
					<span class="sr-only">Error icon</span>
				</svelte:fragment>
				<p class="w-max max-w-[200px] break-all">{ content }</p>
			</Toast>
		</div>
	{:else if toastType === "info"}
		<div transition:blur>
			<Toast color="orange">
				<svelte:fragment slot="icon">
					<AlertCircle class="square-5" />
					<span class="sr-only">Warning icon</span>
				</svelte:fragment>
				<p class="w-max max-w-[200px] break-all">{ content }</p>
			</Toast>
		</div>
	{/if}
</div>
