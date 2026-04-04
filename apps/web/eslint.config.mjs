import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    files: ["app/static/js/**/*.js", "apps/web/app/static/js/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script",
      globals: {
        window: "readonly",
        document: "readonly",
        navigator: "readonly",
        location: "readonly",
        console: "readonly",
        fetch: "readonly",
        URL: "readonly",
        URLSearchParams: "readonly",
        FormData: "readonly",
        CustomEvent: "readonly",
        MutationObserver: "readonly",
        IntersectionObserver: "readonly",
        requestAnimationFrame: "readonly",
        cancelAnimationFrame: "readonly",
        localStorage: "readonly",
        sessionStorage: "readonly",
        HTMLElement: "readonly",
        HTMLFormElement: "readonly",
        HTMLInputElement: "readonly",
        Node: "readonly",
        Event: "readonly",
        history: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly"
      }
    },
    rules: {
      "no-unused-vars": ["warn", {
        "argsIgnorePattern": "^(?:_|err|e|reason)$",
        "varsIgnorePattern": "^_",
        "caughtErrorsIgnorePattern": "^(?:_|_err|_err2|err|e)$"
      }],
      "no-empty": ["error", { "allowEmptyCatch": true }]
    }
  }
];
