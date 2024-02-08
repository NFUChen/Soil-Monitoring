/** @type {import('tailwindcss').Config} */

import plugin from "tailwindcss/plugin";

export default {
	content: [
		"./src/**/*.{html,js,svelte,ts}",
		"./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
	],
	darkMode: "class",
	theme: {
		extend: {
			animation: {
				"spin-slow": "spin 3s linear infinite",
			},
			screens: {
				"2xl": "1440px",
				"3xl": "1920px",
			},
			height: {
				screen: ["100vh", "100dvh"],
				"screen-header": ["calc(100vh - 56px)", "calc(100dvh - 56px)"],
				header: "56px",
			},
			fontSize: {
				xxxs: "0.512rem !important",
				xxs: "0.662rem !important",
				"3xl": "1.953rem",
				"4xl": "2.441rem",
				"5xl": "3.052rem",
			},
			colors: {
				primary: {
					50: "#FFF5F2",
					100: "#FFF1EE",
					200: "#FFE4DE",
					300: "#FFD5CC",
					400: "#FFBCAD",
					500: "#FE795D",
					600: "#EF562F",
					700: "#EB4F27",
					800: "#CC4522",
					900: "#A5371B",
				},
				surface: {
					50: "hsl(0, 0%, 96%)",
					100: "hsl(0, 0%, 91%)",
					200: "hsl(0, 0%, 82%)",
					300: "hsl(0, 0%, 69%)",
					400: "hsl(0, 0%, 53%)",
					500: "hsl(0, 0%, 43%)",
					600: "hsl(0, 0%, 36%)",
					700: "hsl(0, 0%, 31%)",
					800: "hsl(0, 0%, 27%)",
					900: "hsl(0, 0%, 24%)",
					950: "hsl(0, 0%, 13%)",
				},
			},
		},
	},
	plugins: [
		require("flowbite/plugin"),
		plugin(function ({ matchUtilities, theme }) {
			matchUtilities(
				{
					square: (value) => {
						return {
							width: value,
							height: value,
						};
					},
				},
				{ values: theme("spacing") },
			);
		}),
	],
};
