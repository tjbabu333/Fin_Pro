import { Box, Button, Typography } from "@mui/material";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void | Promise<unknown>;
}

function ErrorState({
  message = "Something went wrong.",
  onRetry,
}: ErrorStateProps) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: 250,
        gap: 2,
        textAlign: "center",
      }}
    >
      <Typography
        variant="h6"
        color="error"
      >
        {message}
      </Typography>

      {onRetry && (
        <Button
          variant="contained"
          onClick={onRetry}
        >
          Retry
        </Button>
      )}
    </Box>
  );
}

export default ErrorState;
