import adapter from "@sveltejs/adapter-static";
import preprocess from "svelte-preprocess";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [
        preprocess({
            scss: {
                prependData: '@use "src/variables.scss" as *;',
            },
        }),
    ],

    kit: {
        adapter: adapter({
            pages: "build",
            assets: "build",
            fallback: "redirect.html",
            precompress: false,
            strict: true,
        }),
    },
};

// eslint-disable-next-line
export default config;
