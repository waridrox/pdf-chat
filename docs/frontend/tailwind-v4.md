# Tailwind CSS v4 Integration

This project utilizes **Tailwind CSS v4**, the latest iteration of the utility-first CSS framework. Version 4 brings significant improvements in performance, a new engine, and a more streamlined developer experience, designed for the modern web.

## Key Features & Changes from v3

While a comprehensive list of changes can be found in the [official Tailwind CSS v4 documentation](https://tailwindcss.com/docs), here are some highlights relevant to users of this template:

*   **New Engine (Oxide):** Tailwind CSS v4 features a new, high-performance engine written in Rust, leading to faster build times and a more responsive development experience.
*   **Simplified Configuration:** The configuration file (`tailwind.config.js` or `tailwind.config.ts`) might look different, with a more CSS-first approach. Many common customizations are now handled more intuitively.
*   **Automatic Content Detection:** In many cases, explicit content path configuration is less critical due to smarter defaults.
*   **First-Party Vite Plugin:** Integration with Vite is smoother with the official `@tailwindcss/vite` plugin.
*   **Modern CSS Features:** v4 embraces modern CSS capabilities like cascade layers, container queries, and wide-gamut P3 colors more natively.

## Modern Browser Requirements

It's important to note that Tailwind CSS v4 is designed for modern browser environments. If you need to support older browsers, you might consider using Tailwind CSS v3.4 or implementing appropriate polyfills.

Tailwind CSS v4 officially supports:

*   **Safari 16.4+**
*   **Chrome 111+**
*   **Firefox 128+**

Ensure your target audience aligns with these browser versions.

## Using Tailwind CSS in This Project

*   **Configuration:** The Tailwind CSS configuration is located at `frontend/tailwind.config.js` (or `.ts`).
*   **Utility Classes:** Continue to use Tailwind's utility classes directly in your React components (TSX/JSX files) as you normally would.
*   **Base Styles:** Global styles, custom base styles, or component layers can be defined in `frontend/src/index.css` (or your main CSS entry point).

## Upgrading from v3 (General Advice)

If you were previously using Tailwind CSS v3 and are adapting to this v4 template, or if you're upgrading another project, refer to the official [Tailwind CSS v4 Upgrade Guide](https://tailwindcss.com/docs/upgrade-guide).

## Further Information

For the most detailed and up-to-date information, always refer to the official [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs).
