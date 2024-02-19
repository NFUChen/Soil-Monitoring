<script lang="ts">
	import { cn } from "$lib/utils/utils";
import { Loader2 } from "lucide-svelte";
	let className: string | undefined = undefined;
	export { className as class};
</script>

<Loader2 class={cn("animate-spin text-surface-100", className)} />
