import { writable, type Updater } from "svelte/store";

type OnChangeFunc<T> = ({ curr, next }: { curr: T; next: T }) => T;

export const easyStore = <T>({
	value: initialValue,
	onChange,
}: {
	value: T;
	onChange?: OnChangeFunc<T>;
}) => {
	const store = writable<T>(initialValue);

	const update = (updater: Updater<T>) => {
		store.update((value) => {
			let next = updater(value);
			if (onChange) {
				next = onChange({ curr: value, next });
			}
			return next;
		});
	};

	const set = (value: T) => {
		let next = value;
		if (onChange) {
			next = onChange({ curr: value, next });
		}
		store.set(next);
	};

	return {
		...store,
		update,
		set,
	};
};
