<script lang="ts">
	import SveltyPicker from "svelty-picker";
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
	} from "flowbite-svelte";

	let addParameterModalOpen = false;
	let datePickerVisible = false;
	let dateValue: string;
	const onAddParameter = () => {
		addParameterModalOpen = true;
	};
</script>

<Modal title="新增參數" bodyClass="overflow-visible" size="xs" bind:open={addParameterModalOpen} autoclose={false}>
	<form>
		<div class="mb-8">
			<Label for="replenish-time" class="mb-2 block">時間</Label>
			<div class="relative">
				<Input
					readonly
					value={dateValue}
					id="replenish-time"
					size="lg"
					on:blur={() => (datePickerVisible = false)}
					on:click={() => (datePickerVisible = true)} />
				<div class="absolute top-full h-0">
					{#if datePickerVisible}
						<SveltyPicker
							bind:value={dateValue}
							pickerOnly
							format="yyyy-mm-dd hh:mm:ss"
							on:cancel={() => (datePickerVisible = false)}
							on:blur={() => (datePickerVisible = false)}
							on:input={(v) => {
								dateValue = v.detail;
								datePickerVisible = false;
							}}
							mode="datetime" />
					{/if}
				</div>
			</div>
		</div>
		<div class="mb-8">
			<Label for="replenish-duration" class="mb-2 block">持續時間</Label>
			<Input size="lg" id="replenish-duration" />
		</div>
		<Button type="submit" class="w-full">新增</Button>
	</form>
</Modal>

<div class="flex grow flex-col overflow-hidden p-4">
	<div
		class="border-surface-700 flex flex-col overflow-hidden border border-t-4 border-t-primary-600">
		<div
			class="border-surface-700 flex flex-wrap items-center gap-2 whitespace-nowrap border-b px-4 py-2">
			補水參數
			<div class="ml-auto flex items-center">
				<p class="text-surface-500 text-sm">已選擇 0 筆</p>
				<Button
					outline
					class="text-surface-50 border-surface-700 hover:bg-surface-900 focus-within:ring-surface-200 ml-4"
					>刪除</Button>
				<Button class="ml-2" on:click={onAddParameter}>新增參數</Button>
			</div>
		</div>
		<Table hoverable={true} divClass="overflow-auto" color="custom">
			<TableHead theadClass="border-b border-surface-700 bg-transparent text-surface-400">
				<TableHeadCell class="!p-4">
					<Checkbox class="cursor-pointer" />
				</TableHeadCell>
				<TableHeadCell>時間</TableHeadCell>
				<TableHeadCell class="whitespace-nowrap">持續時間</TableHeadCell>
			</TableHead>
			<TableBody>
				{#each new Array(50) as _}
					<TableBodyRow class=" hover:!bg-surface-900 border-b-surface-900 !border-b">
						<TableBodyCell class="!p-4">
							<Checkbox class="cursor-pointer" />
						</TableBodyCell>
						<TableBodyCell tdClass="px-6">Apple MacBook Pro 17"</TableBodyCell>
						<TableBodyCell tdClass="px-6">Sliver</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	</div>
</div>
