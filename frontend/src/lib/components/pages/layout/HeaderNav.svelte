<script lang="ts">
	import { TabItem, Tabs } from "flowbite-svelte";
	import { GridSolid } from "flowbite-svelte-icons";
	import { AlertTriangle, DropletIcon } from "lucide-svelte";
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";

	$: isDashBoardUrl = $page.url.pathname === "/dashboard";
	$: isWaterRepenishUrl = $page.url.pathname === "/settings/water-replenish";
	$: isAlertSettingUrl = $page.url.pathname === "/settings/alert";
</script>

<header class="p-4">
	<Tabs style="underline" contentClass="hidden">
		<div slot="divider"></div>
		<TabItem open={isDashBoardUrl} on:click={() => goto("/dashboard")}>
			<div slot="title" class="flex items-center gap-2">
				<GridSolid size="sm" />
				面板
			</div>
		</TabItem>
		<TabItem open={isWaterRepenishUrl} on:click={() => goto("/settings/water-replenish")}>
			<div slot="title" class="flex items-center gap-2">
				<DropletIcon class="square-5" />
				補水參數
			</div>
		</TabItem>
		<TabItem open={isAlertSettingUrl} on:click={() => goto("/settings/alert")}>
			<div slot="title" class="flex items-center gap-2">
				<AlertTriangle class="square-5" />
				警示設置
			</div>
		</TabItem>
	</Tabs>
</header>
