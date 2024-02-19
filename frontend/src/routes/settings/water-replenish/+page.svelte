<script lang="ts">
	import {
		Button,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Checkbox,
		Modal,
		Input,
		Label,
		type InputType,
	} from "flowbite-svelte";
	import { createMutation, createQuery } from "@tanstack/svelte-query";
	import {
		GetWaterReplenishmentConfigService,
		SaveWaterReplenishmentConfigService,
	} from "$lib/services/replenish/replenishService";
	import { maskTime } from "$lib/utils/maskTime";
	import LoadingSpinner from "$lib/components/ui/LoadingSpinner.svelte";
	import { secondTohhmmss } from "$lib/utils/secondTohhmmss";

	let addParameterModalOpen = false;
	let selectedReplenishmentTimes: number[] = [];
	let form = [
		{
			id: "replenish-time",
			type: "tel" as InputType,
			value: "",
			label: "時間",
			error: undefined as string | undefined,
			placeholder: "hh:mm:ss",
			onInput: (event: Event) => {
				const input = event.target as HTMLInputElement;
				form[0].value = maskTime(input.value);
			},
		},
		{
			id: "replenish-duration",
			type: "number" as InputType,
			value: "",
			label: "持續時間",
			placeholder: "5",
			error: undefined as string | undefined,
		},
	];

	const getWaterReplenishmentConfigQuery = createQuery({
		queryKey: ["waterReplenishmentConfig"],
		queryFn: GetWaterReplenishmentConfigService,
	});

	const saveWaterReplenishmentConfigMutation = createMutation({
		mutationKey: ["saveWaterReplenishmentConfig"],
		mutationFn: SaveWaterReplenishmentConfigService,
		onSuccess: (data) => {
			addParameterModalOpen = false;
			form = form.map((item) => ({ ...item, value: "" }));
			replenishmentTimes = data.replenishment_times.toSorted((a, b) => a.timestamp - b.timestamp);
			selectedReplenishmentTimes = [];
		},
	});

	const onStartAddingParameter = () => {
		addParameterModalOpen = true;
	};

	const onAddParameter = () => {
		const isValid = checkFormIsValid();
		if (!isValid) return;

		const replenishmentTime = {
			timestamp: form[0].value,
			duration: parseInt(form[1].value),
		};

		const oldReplenishmentTimes = replenishmentTimes.map((time) => ({
			timestamp: secondTohhmmss(time.timestamp),
			duration: time.duration,
		}));

		const request = {
			replenishment_times: [...oldReplenishmentTimes, replenishmentTime],
		};

		$saveWaterReplenishmentConfigMutation.mutate(request);
	};

	const onDeleteParameter = () => {
		const request = {
			replenishment_times: replenishmentTimes
				.filter((time) => !selectedReplenishmentTimes.includes(time.timestamp))
				.map((time) => ({
					timestamp: secondTohhmmss(time.timestamp),
					duration: time.duration,
				})),
		};

		$saveWaterReplenishmentConfigMutation.mutate(request);
	};

	const onSelectSingle = (event: Event, timestamp: number) => {
		const checked = (event.target as HTMLInputElement).checked;
		if (checked) {
			selectedReplenishmentTimes = [...selectedReplenishmentTimes, timestamp];
		} else {
			selectedReplenishmentTimes = selectedReplenishmentTimes.filter((time) => time !== timestamp);
		}
	};

	const onSelectAll = (event: Event) => {
		const value = (event.target as HTMLInputElement).checked;
		if (value) {
			selectedReplenishmentTimes = replenishmentTimes.map((time) => time.timestamp);
		} else {
			selectedReplenishmentTimes = [];
		}
	};

	const checkFormIsValid = () => {
		form.forEach((item) => checkFieldIsValid(item.id));
		if (form.some((item) => item.error)) {
			return false;
		}
		return true;
	};

	const checkFieldIsValid = (id: string) => {
		const item = form.find((item) => item.id === id);
		if (!item) return;

		item.error = undefined;
		if (!item.value) {
			item.error = "請輸入此欄位";
		}

		if (item.id === "replenish-time") {
			let time = item.value.split(":");
			time = time.filter((t) => !isNaN(Number(t)));

			if (time.length !== 3) {
				item.error = "請輸入正確的時間格式";
			}

			if (replenishmentTimes.some((time) => secondTohhmmss(time.timestamp) === item.value)) {
				item.error = "此時間已存在";
			}
		}
		form = [...form];
	};

	$: replenishmentTimes =
		$getWaterReplenishmentConfigQuery.data?.replenishment_times.toSorted(
			(a, b) => a.timestamp - b.timestamp,
		) || [];
	$: isAllSelected =
		replenishmentTimes.length !== 0 &&
		replenishmentTimes.every((time) => selectedReplenishmentTimes.includes(time.timestamp));
</script>

<Modal
	title="新增參數"
	bodyClass="overflow-visible"
	size="xs"
	bind:open={addParameterModalOpen}
	autoclose={false}>
	<form on:submit|preventDefault={onAddParameter}>
		{#each form as item}
			<div class="mb-8">
				<Label for={item.id} class="mb-2 block">{item.label}</Label>
				<Input
					on:blur={() => checkFieldIsValid(item.id)}
					on:input={item.onInput}
					bind:value={item.value}
					placeholder={item.placeholder}
					id={item.id}
					type={item.type}
					size="lg" />
				{#if item.error}
					<p class="mt-2 text-sm text-red-500">{item.error}</p>
				{/if}
			</div>
		{/each}
		<Button disabled={$saveWaterReplenishmentConfigMutation.isPending} type="submit" class="w-full">
			{#if $saveWaterReplenishmentConfigMutation.isPending}
				<LoadingSpinner />
			{:else}
				新增
			{/if}
		</Button>
	</form>
</Modal>

<div class="flex grow flex-col overflow-hidden p-4">
	<div
		class="flex flex-col overflow-hidden border border-t-4 border-surface-700 border-t-primary-600">
		<div
			class="flex flex-wrap items-center gap-2 whitespace-nowrap border-b border-surface-700 px-4 py-2">
			補水參數
			<div class="ml-auto flex items-center">
				<p class="text-sm text-surface-500">已選擇 {selectedReplenishmentTimes.length} 筆</p>
				<Button
					on:click={onDeleteParameter}
					disabled={!selectedReplenishmentTimes.length ||
						$saveWaterReplenishmentConfigMutation.isPending}
					outline
					class="ml-4 border-surface-700 text-surface-50 focus-within:ring-surface-200 hover:bg-surface-900">
					{#if $saveWaterReplenishmentConfigMutation.isPending}
						<LoadingSpinner />
					{:else}
						刪除
					{/if}
				</Button>
				<Button class="ml-2" on:click={onStartAddingParameter}>新增參數</Button>
			</div>
		</div>
		<Table hoverable={true} divClass="overflow-auto" color="custom">
			<TableHead theadClass="border-b border-surface-700 bg-transparent text-surface-400">
				<TableHeadCell class="!p-4">
					<Checkbox on:change={onSelectAll} checked={isAllSelected} class="cursor-pointer" />
				</TableHeadCell>
				<TableHeadCell>時間</TableHeadCell>
				<TableHeadCell class="whitespace-nowrap">持續時間</TableHeadCell>
			</TableHead>
			<TableBody>
				{#if $getWaterReplenishmentConfigQuery.isLoading}
					{#each new Array(8) as _}
						<TableBodyRow class="border-b border-surface-900">
							<TableBodyCell class="!p-4" colspan="3">
								<div class="h-8 w-full animate-pulse rounded-md bg-surface-700"></div>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				{:else}
					{#each replenishmentTimes as time}
						<TableBodyRow class=" !border-b border-b-surface-900 hover:!bg-surface-900">
							<TableBodyCell class="!p-4">
								<Checkbox
									on:change={(event) => onSelectSingle(event, time.timestamp)}
									checked={selectedReplenishmentTimes.includes(time.timestamp)}
									class="cursor-pointer" />
							</TableBodyCell>
							<TableBodyCell tdClass="px-6">{secondTohhmmss(time.timestamp)}</TableBodyCell>
							<TableBodyCell tdClass="px-6">{time.duration}</TableBodyCell>
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</Table>
	</div>
</div>
