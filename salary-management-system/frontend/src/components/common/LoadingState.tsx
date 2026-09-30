import { Box, CircularProgress, Typography } from "@mui/material";

interface LoadingStateProps {
  message?: string;
}

function LoadingState({
  message = "Loading...",
}: LoadingStateProps) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: 250,
        gap: 2,
      }}
    >
      <CircularProgress />

      <Typography color="text.secondary">
        {message}
      </Typography>
    </Box>
  );
}

export default LoadingState;