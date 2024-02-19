import { type ClassValue, clsx } from "clsx";
import { extendTailwindMerge } from "tailwind-merge";

const twMerge = extendTailwindMerge({
	extend: {
		classGroups: {
			"font-size": ["text-xxs", "text-xxxs"],
		},
	},
});

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function debounce<F extends (...params: unknown[]) => void>(fn: F, delay = 2500) {
	let timeoutID: number;
	return function (this: unknown, ...args: unknown[]) {
		clearTimeout(timeoutID);
		timeoutID = setTimeout(() => {
			return fn.apply(this, args);
		}, delay);
	} as F;
}

export function setQueryParams(params: Record<string, string | number>) {
	const url = new URL(window.location.href);
	for (const [key, value] of Object.entries(params)) {
		if (!value) {
			url.searchParams.delete(key);
			continue;
		}
		url.searchParams.set(key, value.toString());
	}
	window.history.replaceState({}, "", url.toString());
}

export function getQueryParams() {
	const url = new URL(window.location.href);
	const params = Object.fromEntries(url.searchParams.entries());
	return params;
}
