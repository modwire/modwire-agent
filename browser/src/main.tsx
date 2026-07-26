import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./app/App";
import "./styles.css";

const root = document.querySelector<HTMLDivElement>("#app");

if (!root) {
  throw new Error("The Siren Browser needs an #app element.");
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
