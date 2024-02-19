import { writable } from "svelte/store";

export const size = writable({
	lt: {
		sm: false,
		md: false,
		lg: false,
	},
	gt: {
		sm: false,
		md: false,
		lg: false,
	},
});

const setSize = (innerWidth: number) => {
  size.update(() => {
    const lt = {
      sm: innerWidth < 640,
      md: innerWidth < 768,
      lg: innerWidth < 1024,
    };
    const gt = {
      sm: innerWidth >= 640,
      md: innerWidth >= 768,
      lg: innerWidth >= 1024,
    };
    return { lt, gt };
  });
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const useResizeDetector = (node: Node) => {
  setSize(window.innerWidth);
	window.addEventListener("resize", () => {
		const { innerWidth } = window;
    setSize(innerWidth);
	});
};
