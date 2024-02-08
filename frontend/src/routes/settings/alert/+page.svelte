<script>
	import { Button, Input, Label } from "flowbite-svelte";
</script>

<div class="flex grow flex-col overflow-hidden p-4">
	<div
		class="border-surface-700 flex flex-col overflow-hidden border border-t-4 border-t-primary-600">
		<div class="border-surface-700 flex items-center gap-2 border-b px-4 py-2">
			溫濕度警示閾值
			<Button class="ml-auto">儲存</Button>
		</div>
		<div class="overflow-y-auto">
			<div class="border-surface-700 border-b p-4">
				<div class="mb-4 flex items-center">
					<p>溫度</p>
				</div>
				<div class="mb-6">
					<Label for="large-input" class="text-surface-50 mb-2 block">警告上限</Label>
					<Input
						id="large-input"
						size="lg"
						type="number"
						class="text-surface-50 border-surface-500 bg-transparent"
						placeholder="請輸入溫度閾值上限" />
				</div>
				<div class="mb-6">
					<Label for="large-input" class="text-surface-50 mb-2 block">警告下限</Label>
					<Input
						id="large-input"
						size="lg"
						type="number"
						class="text-surface-50 border-surface-500 bg-transparent"
						placeholder="請輸入溫度閾值下限" />
				</div>
			</div>
			<div class="p-4">
				<div class="mb-4 flex items-center">
					<p>濕度</p>
				</div>
				<div class="mb-6">
					<Label for="large-input" class="text-surface-50 mb-2 block">警告上限</Label>
					<Input
						id="large-input"
						size="lg"
						type="number"
						class="text-surface-50 border-surface-500 bg-transparent"
						placeholder="請輸入濕度閾值上限" />
				</div>
				<div class="mb-6">
					<Label for="large-input" class="text-surface-50 mb-2 block">警告下限</Label>
					<Input
						id="large-input"
						size="lg"
						type="number"
						class="text-surface-50 border-surface-500 bg-transparent"
						placeholder="請輸入濕度閾值下限" />
				</div>
			</div>
		</div>
	</div>
</div>
