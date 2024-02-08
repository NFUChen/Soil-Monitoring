import { browser } from "$app/environment";
import { QueryClient } from "@tanstack/svelte-query";
import type { BackendErrorResponse, GernicError } from "$lib/services/commonType";
import type { LayoutLoad } from "./$types";
import { addToast } from "$lib/components/ui/providers/ToastProvider.svelte";

export const load: LayoutLoad = async () => {
	const notifyError = (error: unknown) => {
		const e = error as GernicError<BackendErrorResponse | string>;
		const errorMessage = typeof e.message === "string" ? e.message : e.message.error;
		if (!browser) {
			return;
		}
		if (e.status === 401) {
			addToast({
				content: "請重新登入",
				type: "error",
			});
			return;
		}
		if (e.status > 399) {
			addToast({
				type: "error",
				content: "系統錯誤",
			});
			return;
		}
		addToast({
			type: "error",
			content: errorMessage,
		});
	};
	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				enabled: browser,
				retry(failureCount, error: unknown) {
					notifyError(error);
					return false;
				},
			},
			mutations: {
				onError: notifyError,
			},
		},
	});

	return { queryClient };
};
