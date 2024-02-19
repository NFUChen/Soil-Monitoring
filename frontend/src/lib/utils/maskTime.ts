export const maskTime = (value: string) => {
	const colonPosition = [2, 5];
  const lastChar = value[value.length - 1];
  const isValidColon = colonPosition.includes(value.length -1) && lastChar === ":";

	if (isNaN(Number(lastChar)) && !isValidColon) {
		return value.slice(0, -1);
	}

	let i = 0;

	while (i < 8) {
		if (
			(value.length > colonPosition[0] && i === colonPosition[0]) ||
			(value.length > colonPosition[1] && i === colonPosition[1])
		) {
			if (value[i] !== ":") {
				value = value.slice(0, i) + ":" + value.slice(i);
			}
		}
		i++;
	}
	const hh = value.slice(0, 2);
	const mm = value.slice(3, 5);
	const ss = value.slice(6, 8);

	if (hh && parseInt(hh) > 23) {
		value = "23" + value.slice(2);
	}
	if (mm && parseInt(mm) > 59) {
		value = value.slice(0, 3) + "59" + value.slice(5);
	}
	if (ss && parseInt(ss) > 59) {
		value = value.slice(0, 6) + "59";
	}
	return value.slice(0, 8);
};
