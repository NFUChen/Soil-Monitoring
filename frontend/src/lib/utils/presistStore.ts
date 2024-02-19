import { writable, type Updater } from "svelte/store";

export const createPresistStore = <T>(key: string, initialValue: T, onChange?: Updater<T>) => {
	const store = writable<T>(initialValue);

	const initFromLocalStorage = () => {
		const isBrowser = typeof window !== "undefined";

		if (!isBrowser) return;

		const value = localStorage.getItem(key);

		if (value) {
			const parsedValue = JSON.parse(value);
			set(parsedValue);
			return;
		}
		set(initialValue);
	};

	const setToLocalStorage = (value: T) => {
		localStorage.setItem(key, JSON.stringify(value));
	};

	const update = (updater: Updater<T>) => {
		store.update((curr) => {
			let next = updater(curr);
			if (onChange) {
				next = onChange(next);
			}
			setToLocalStorage(next);
			return next;
		});
	};

	const set = (value: T) => {
		setToLocalStorage(value);
		let next = value;
		if (onChange) {
			next = onChange(next);
		}
		store.set(next);
	};

	initFromLocalStorage();

	return {
		...store,
		update,
		set,
	};
};
