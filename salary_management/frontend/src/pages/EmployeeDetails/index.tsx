import { Box, Button, Card, CardContent, Grid, Typography } from "@mui/material";
import { Link, useParams } from "react-router-dom";

import { useEmployee } from "../../hooks/useEmployee";
import LoadingState from "../../components/common/LoadingState";
import ErrorState from "../../components/common/ErrorState";

function EmployeeDetails() {
  const { id } = useParams<{ id: string }>();
  const employeeId = Number(id);

  const {
    data: employee,
    isLoading,
    isError,
    refetch,
  } = useEmployee(employeeId);

  if (isLoading) {
    return <LoadingState message="Loading employee..." />;
  }

  if (isError || !employee) {
    return (
      <Box>
        <ErrorState
          message="Employee could not be loaded."
          onRetry={() => refetch()}
        />

        <Button
          component={Link}
          to="/employees"
          sx={{ mt: 2 }}
          variant="outlined"
        >
          Back to Employees
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          mb: 3,
        }}
      >
        <Box>
          <Typography variant="h4">
            {employee.full_name}
          </Typography>

          <Typography color="text.secondary">
            {employee.employee_code}
          </Typography>
        </Box>

        <Button component={Link} to="/employees" variant="outlined">
          Back
        </Button>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Employee Information
          </Typography>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Employee Code
              </Typography>
              <Typography>{employee.employee_code}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Full Name
              </Typography>
              <Typography>{employee.full_name}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Email
              </Typography>
              <Typography>{employee.email}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Country
              </Typography>
              <Typography>{employee.country}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Department
              </Typography>
              <Typography>{employee.department}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Job Title
              </Typography>
              <Typography>{employee.job_title}</Typography>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant="caption" color="text.secondary">
                Status
              </Typography>
              <Typography>{employee.status}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6">
            Salary
          </Typography>

          <Typography color="text.secondary" sx={{ mb: 2 }}>
            View the employee's complete salary history.
          </Typography>

          <Button
            component={Link}
            to={`/employees/${employee.id}/salaries`}
            variant="contained"
          >
            View Salary History
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}

export default EmployeeDetails;
