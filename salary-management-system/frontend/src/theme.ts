import {
  createTheme,
} from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#1976d2",
    },

    secondary: {
      main: "#9c27b0",
    },

    background: {
      default: "#f5f7fa",
    },
  },

  typography: {
    fontFamily: [
      "Inter",
      "Roboto",
      "Arial",
      "sans-serif",
    ].join(","),
  },

  shape: {
    borderRadius: 8,
  },

  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow:
            "0 2px 8px rgba(0, 0, 0, 0.08)",
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow:
            "0 2px 8px rgba(0, 0, 0, 0.08)",
        },
      },
    },
  },
});

export default theme;