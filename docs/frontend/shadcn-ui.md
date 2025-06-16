# Shadcn UI Guide

This project leverages [Shadcn UI](https://ui.shadcn.com/) for building its user interface. Shadcn UI is not a traditional component library but rather a collection of beautifully designed components that you can copy and paste into your application. This approach gives you full ownership and control over the code, allowing for deep customization.

## Philosophy

Understanding the philosophy behind Shadcn UI is key to using it effectively:

*   **You Own the Code:** When you add a component, its source code is added directly to your project (typically under `frontend/src/components/ui/`). You can modify it as much as you need.
*   **Not a Dependency:** It's not a package you install from npm in the usual sense (apart from the CLI tool). This means no versioning conflicts with a third-party library and no waiting for the library maintainer to update or fix something.
*   **Built with Radix UI and Tailwind CSS:** Components are generally built using [Radix UI Primitives](https://www.radix-ui.com/) for accessibility and behavior, and styled with [Tailwind CSS](https://tailwindcss.com/) for a utility-first approach.

## Adding Components

To add new components to your project, use the Shadcn UI CLI. Make sure you are in the `frontend` directory:

```bash
npx shadcn-ui@latest add [component-name]
```

For example, to add an `alert-dialog`:

```bash
npx shadcn-ui@latest add alert-dialog
```

This command will typically do the following:
1.  Check your `components.json` for configuration.
2.  Install any necessary dependencies for the component (e.g., `@radix-ui/react-alert-dialog`).
3.  Add the component's source code to `frontend/src/components/ui/`.

## Configuration (`components.json`)

The behavior of the Shadcn UI CLI is configured by the `components.json` file located in your `frontend` directory. This file defines:

*   `$schema`: The schema URL for `components.json`.
*   `style`: The style of components to use (e.g., "default", "new-york"). This template uses `default`.
*   `rsc`: Whether to install React Server Components (RSC) compatible components (true/false).
*   `tsx`: Whether to use TypeScript for components (true/false). This template uses `true`.
*   `tailwind`:
    *   `config`: Path to your Tailwind CSS configuration file.
    *   `css`: Path to your main CSS file where Tailwind directives are imported.
    *   `baseColor`: The base color for your theme (e.g., "slate", "zinc").
    *   `cssVariables`: Whether to use CSS variables for theming.
*   `aliases`:
    *   `components`: Path alias for where your UI components are stored (e.g., `~/components`, which might map to `src/components`).
    *   `utils`: Path alias for utility functions (e.g., `~/lib/utils` for `cn()` function).

Ensure this file is configured correctly for your project structure if you deviate from the template's defaults.

## Customizing Components

Since the component code is directly in your project (e.g., `frontend/src/components/ui/button.tsx`), you can customize it by:

*   **Modifying Styles:** Directly change Tailwind CSS classes within the component's TSX file.
*   **Altering Behavior:** Change the underlying Radix UI primitives or add your own logic.
*   **Extending Functionality:** Add new props or features to the component.

## Theming

Shadcn UI components are designed to be themed using CSS variables. Check the `frontend/src/index.css` (or your main CSS file) for the theme variables defined by Shadcn UI when you initialized it. You can customize these variables to change the overall look and feel of the components.

## Best Practices

*   **Keep CLI Updated:** Occasionally run `npx shadcn-ui@latest init` to ensure your CLI and local setup are up-to-date with any changes from Shadcn UI (be careful and review changes if you have heavily customized `components.json`).
*   **Refer to Official Docs:** For specific component APIs, props, and usage examples, always refer to the [official Shadcn UI documentation](https://ui.shadcn.com/docs/components/accordion).
*   **Understand Dependencies:** When you add a component, it might install peer dependencies (like Radix UI packages). Be aware of these in your `package.json`.

By following this guide and leveraging the official documentation, you can effectively use Shadcn UI to build a beautiful and highly customizable frontend for this application.
