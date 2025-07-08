# Frontend (React + Vite)

This directory contains the frontend application built with React and Vite.

## Overview

- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4, Shadcn UI
- **Language**: TypeScript

## Project Structure

```
frontend/
├── public/             # Static assets
├── src/
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable UI components
│   ├── context/        # State management (e.g., React Context)
│   ├── features/       # Feature-based components (e.g., auth, dashboard)
│   ├── hooks/          # Custom hooks
│   ├── layouts/        # Layout components (e.g., MainLayout)
│   ├── lib/            # Utility functions and constants
│   ├── pages/          # Page components (routed)
│   ├── routes/         # React Router definitions
│   ├── types/          # TypeScript types
│   ├── index.tsx       # Entry point
│   ├── index.css       # Global styles
│   └── vite-env.d.ts   # Vite environment types
├── components.json     # Shadcn UI configuration
├── index.html          # Main HTML file
├── package.json        # Project dependencies and scripts
├── README.md           # This file
├── tailwind.config.js  # Tailwind CSS configuration
├── tsconfig.json       # TypeScript configuration
├── Dockerfile          # Dockerfile for containerization
├── vite.config.ts      # Vite configuration
└── .gitignore          # Git ignore file
```
*(Adjust the structure above to reflect the actual project layout)*

## Getting Started

### Prerequisites

- Node.js (version 22.10.0 or later recommended)
- npm or yarn

### Installation

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or
    # yarn install
    ```

### Environment Variables

Create a `.env` file in the `frontend` directory by copying `.env.example` (if one exists) or by creating it manually.

Key environment variables:

- `VITE_API_URL`: The base URL for the backend API (e.g., `http://localhost:8000/api` for local development, or your production API URL).

Example `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

### Available Scripts

In the `frontend` directory, you can run the following scripts:

- **`npm run dev` or `yarn dev`**: Runs the app in development mode. Open [http://localhost:5173](http://localhost:5173) (or the port Vite assigns) to view it in the browser. The page will reload if you make edits.

- **`npm run build` or `yarn build`**: Builds the app for production to the `dist` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

- **`npm run lint` or `yarn lint`**: Lints the codebase using ESLint.

- **`npm run preview` or `yarn preview`**: Serves the production build locally to preview it.

## Styling

This project uses Tailwind CSS for utility-first styling.
- Tailwind configuration is in `tailwind.config.js`.
- Base styles and custom CSS can be found in `src/index.css`.

### Shadcn UI

This project utilizes [Shadcn UI](https://ui.shadcn.com/) for its component library. Shadcn UI is not a traditional component library; instead, you install individual components into your project, giving you full control over their code and styling.

**Adding New Components:**

To add new Shadcn UI components, use the Shadcn UI CLI. Ensure you are in the `frontend` directory:

```bash
npx shadcn-ui@latest add [component-name]
```
For example, to add a button:
```bash
npx shadcn-ui@latest add button
```
This command will add the component's source code to `src/components/ui/` (or as configured in `components.json`).

**Configuration:**

- The Shadcn UI configuration is in `components.json`.
- Components are typically installed into `src/components/ui`.

**Customization:**

Since you own the component code, you can customize components directly by editing their files in `src/components/ui/`. Tailwind CSS utility classes are used for styling, making them easy to modify to fit the project's design system.

## Adding New Components and Pages

- **Components**: Create new reusable components in `src/components/`.
- **Pages**: Create new page components in `src/pages/` and ensure they are added to your routing configuration (e.g., in `App.tsx` or a dedicated routes file).

## Further Information

- [React Documentation](https://reactjs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation (v4)](https://tailwindcss.com/docs)
- [Shadcn UI Documentation](https://ui.shadcn.com/docs)
