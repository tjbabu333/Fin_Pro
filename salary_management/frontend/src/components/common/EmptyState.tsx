import { Box, Typography } from "@mui/material";

interface EmptyStateProps {
  title?: string;
  message?: string;
}

function EmptyState({
  title = "No data found",
  message = "There is no information to display.",
}: EmptyStateProps) {
  return (
    <Box
      sx={{
        textAlign: "center",
        py: 8,
      }}
    >
      <Typography variant="h6">
        {title}
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mt: 1 }}
      >
        {message}
      </Typography>
    </Box>
  );
}

export default EmptyState;