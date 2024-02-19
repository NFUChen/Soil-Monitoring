export const autoFocus = (node: Node) => {
	if (node.nodeType === Node.ELEMENT_NODE) {
		const currentElement = node as HTMLElement;
		currentElement.focus();
	}
};
