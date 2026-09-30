import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import PeopleIcon from "@mui/icons-material/People";
import PaymentsIcon from "@mui/icons-material/Payments";
import AssessmentIcon from "@mui/icons-material/Assessment";

import { useAnalytics } from "../../hooks/useAnalytics";
import LoadingState from "../../components/common/LoadingState";
import ErrorState from "../../components/common/ErrorState";

function Dashboard() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useAnalytics();

  if (isLoading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  if (isError) {
    return (
      <ErrorState
        message="Failed to load dashboard data."
        onRetry={() => refetch()}
      />
    );
  }

  const summary = data?.summary;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Salary Management Dashboard
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        Welcome to the Salary Management System.
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <PeopleIcon
                color="primary"
                sx={{ fontSize: 40 }}
              />

              <Typography variant="h6">
                Total Employees
              </Typography>

              <Typography variant="h3">
                {summary?.total_employees ?? 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <PaymentsIcon
                color="primary"
                sx={{ fontSize: 40 }}
              />

              <Typography variant="h6">
                Salary Records
              </Typography>

              <Typography variant="h3">
                {summary?.total_salary_records ?? 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <AssessmentIcon
                color="primary"
                sx={{ fontSize: 40 }}
              />

              <Typography variant="h6">
                Average Salary
              </Typography>

              <Typography variant="h3">
                {summary?.average_salary?.toLocaleString() ??
                  0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;