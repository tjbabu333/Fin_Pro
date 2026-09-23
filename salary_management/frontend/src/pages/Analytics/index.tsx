import {
  Box,
  Card,
  CardContent,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import { useAnalytics } from "../../hooks/useAnalytics";
import LoadingState from "../../components/common/LoadingState";
import ErrorState from "../../components/common/ErrorState";
import EmptyState from "../../components/common/EmptyState";

function Analytics() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useAnalytics();

  if (isLoading) {
    return <LoadingState message="Loading analytics..." />;
  }

  if (isError) {
    return (
      <ErrorState
        message="Failed to load analytics."
        onRetry={() => refetch()}
      />
    );
  }

  const summary = data?.summary;
  const departments = data?.departments ?? [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        Employee and salary analytics.
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Total Employees
              </Typography>

              <Typography variant="h4">
                {summary?.total_employees ?? 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Total Salary
              </Typography>

              <Typography variant="h4">
                {summary?.total_base_salary?.toLocaleString() ??
                  0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Total Bonus
              </Typography>

              <Typography variant="h4">
                {summary?.total_bonus?.toLocaleString() ??
                  0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography
        variant="h5"
        sx={{ mt: 5, mb: 2 }}
      >
        Department Analytics
      </Typography>

      {departments.length === 0 ? (
        <Paper>
          <EmptyState
            title="No department analytics"
            message="No department analytics are available."
          />
        </Paper>
      ) : (
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  Department
                </TableCell>

                <TableCell>
                  Employees
                </TableCell>

                <TableCell>
                  Average Salary
                </TableCell>

                <TableCell>
                  Total Salary
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {departments.map(
                (department) => (
                  <TableRow
                    key={department.department}
                  >
                    <TableCell>
                      {department.department}
                    </TableCell>

                    <TableCell>
                      {department.employee_count}
                    </TableCell>

                    <TableCell>
                      {department.average_salary.toLocaleString()}
                    </TableCell>

                    <TableCell>
                      {department.total_salary.toLocaleString()}
                    </TableCell>
                  </TableRow>
                )
              )}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
}

export default Analytics;