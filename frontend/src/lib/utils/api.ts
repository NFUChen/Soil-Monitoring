import { browser } from "$app/environment";

// Type Definitions for API ====================================================
type FileData = Record<"files", File[]>;

type SendParams = {
	method: string;
	path: string;
	params?: Record<string, string>;
	data?: unknown;
	headers?: HeadersInit;
	origin: string;
};

type RequestParams = Partial<Omit<SendParams, "path">> & {
	credentials?: RequestCredentials;
	keepalive?: boolean;
	body?: BodyInit | null;
};

const logError = (path: string, status: number, response: object) => {
	// browser dont need to log error, to hide sensitive data
	if (browser) return;
	const time = new Date().toLocaleString("zh-TW", { timeZone: "Asia/Taipei" });
	console.log("");
	console.error("ERROR: ", time, path, status);
	console.table(response);
	console.log("");
};

// API Implements ==============================================================
const send = async ({ method, path, params, data, headers, origin }: SendParams) => {
	const uri = new URL(origin);

	// check if path starts with a slash
	if (!path.startsWith("/")) {
		path = "/".concat(path);
	}

	// concat path to uri
	uri.pathname = uri.pathname.concat(path);

	// replace double slashes with single slashes
	uri.pathname = uri.pathname.replace(/\/{2,}/g, "/");

	const opts: RequestParams = {};

	opts.method = method;

	opts.headers = new Headers(headers);
	opts.headers.append('ngrok-skip-browser-warning', 'true');

	// opts.credentials = "include";

	opts.keepalive = true;

	if (data) {
		const contentType: string = (data as FileData).files && (data as FileData).files[0]?.type;

		if (
			!(
				contentType == "application/msword" ||
				contentType == "application/pdf" ||
				contentType == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
				contentType == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
				contentType == "image/gif" ||
				contentType == "image/ico" ||
				contentType == "image/jpeg" ||
				contentType == "image/png" ||
				contentType == "image/svg" ||
				contentType == "image/svg+xml" ||
				contentType == "image/webp"
			)
		) {
			opts.headers.set("Content-Type", "application/json");
			if (typeof data !== "string") {
				opts.body = JSON.stringify(data);
			} else {
				opts.body = data;
			}
		} else {
			const form = new FormData();

			if ((data as FileData).files) {
				for (const x of (data as FileData).files) {
					form.append("files", x);
				}
			}
			for (const d in data) {
				if (d !== "files") {
					const value = (data as Record<string, string | Blob>)[d];
					form.append(d, value);
				}
			}
			opts.body = form;
		}
	}

	if (params) {
		Object.keys(params).forEach((key) => uri.searchParams.append(key, params[key]));
	}

	const url = uri.toString();

	const response = await fetch(url, opts);

	const isJson = response.headers.get("content-type")?.includes("application/json");

	const res = isJson ? await response.json() : await response.text();

	if (response?.status > 499) {
		logError(path, response.status, res);
		throw { status: response.status, message: "Internal Error" };
	} else if (response?.status > 399) {
		logError(path, response.status, res);
		throw { status: response.status, message: res };
	} else {
		// const setCookieForLogin = response.headers.get("set-cookie");
		// if (setCookieForLogin) {
		// 	const sidCookie = cookie.parse(setCookieForLogin);
		// 	res.jsid = sidCookie["JSID"];
		// }
		return res;
	}
};

export const getAPI = (path: string, origin: string, headers?: HeadersInit) => {
	return send({ method: "GET", path, origin, headers });
};

export const del = <T>(path: string, origin: string, data: T, headers?: HeadersInit) => {
	return send({ method: "DELETE", path, data, origin, headers });
};

export const post = <T>(path: string, origin: string, data: T, headers?: HeadersInit) => {
	return send({ method: "POST", path, data, origin, headers });
};

export const put = <T>(path: string, origin: string, data: T, headers?: HeadersInit) => {
	return send({ method: "PUT", path, data, origin, headers });
};
