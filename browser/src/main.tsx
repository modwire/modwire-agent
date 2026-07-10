import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

import { App } from "./App";
import "./styles.css";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#5145cd" },
    background: { default: "#f8fafc" },
  },
  shape: { borderRadius: 12 },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </StrictMode>,
);
