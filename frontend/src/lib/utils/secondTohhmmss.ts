export const secondTohhmmss = (second: number) => {
	const h = Math.floor(second / 3600) === 24 ? 0 : Math.floor(second / 3600);
	const m = Math.floor((second % 3600) / 60);
	const s = Math.floor((second % 3600) % 60);
	const hh = h < 10 ? `0${h}` : h;
	const mm = m < 10 ? `0${m}` : m;
	const ss = s < 10 ? `0${s}` : s;
	return `${hh}:${mm}:${ss}`;
};
