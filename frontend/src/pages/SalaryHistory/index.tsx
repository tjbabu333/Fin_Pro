import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { Link, useParams } from "react-router-dom";

import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingState from "../../components/common/LoadingState";
import { useSalaries } from "../../hooks/useSalaries";

function SalaryHistory() {
  const { id } = useParams<{ id: string }>();

  const employeeId = Number(id);

  const {
    data: salaries,
    isLoading,
    isError,
    refetch,
  } = useSalaries(employeeId);

  if (isLoading) {
    return <LoadingState message="Loading salary history..." />;
  }

  if (isError) {
    return (
      <ErrorState
        message="Failed to load salary history."
        onRetry={() => refetch()}
      />
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
          <Typography variant="h4">Salary History</Typography>

          <Typography color="text.secondary">
            Employee ID: {employeeId}
          </Typography>
        </Box>

        <Box
          sx={{
            display: "flex",
            gap: 2,
          }}
        >
          <Button
            component={Link}
            to={`/employees/${employeeId}/salaries/new`}
            variant="contained"
          >
            Add Salary
          </Button>

          <Button
            component={Link}
            to={`/employees/${employeeId}`}
            variant="outlined"
          >
            Back to Employee
          </Button>
        </Box>
      </Box>

      {!salaries || salaries.length === 0 ? (
        <Paper>
          <EmptyState
            title="No salary records"
            message="This employee does not have any salary records."
          />
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Base Salary</TableCell>
                <TableCell>Bonus</TableCell>
                <TableCell>Total</TableCell>
                <TableCell>Currency</TableCell>
                <TableCell>Effective From</TableCell>
                <TableCell>Effective To</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {salaries.map((salary) => {
                const baseSalary = Number(salary.base_salary);
                const bonus = Number(salary.bonus);
                const total = baseSalary + bonus;

                return (
                  <TableRow key={salary.id}>
                    <TableCell>{salary.id}</TableCell>

                    <TableCell>
                      {baseSalary.toLocaleString()}
                    </TableCell>

                    <TableCell>
                      {bonus.toLocaleString()}
                    </TableCell>

                    <TableCell>
                      {total.toLocaleString()}
                    </TableCell>

                    <TableCell>{salary.currency}</TableCell>

                    <TableCell>{salary.effective_from}</TableCell>

                    <TableCell>
                      {salary.effective_to || "Current"}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}

export default SalaryHistory;
