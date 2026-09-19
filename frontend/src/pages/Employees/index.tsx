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
  TextField,
  Typography,
} from "@mui/material";

import { useState } from "react";
import { Link } from "react-router-dom";

import { useEmployees } from "../../hooks/Employees";
import LoadingState from "../../components/common/LoadingState";
import ErrorState from "../../components/common/ErrorState";
import EmptyState from "../../components/common/EmptyState";

import type { Employee } from "../../types/employee";

function Employees() {
  const [search, setSearch] = useState("");

  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useEmployees({
    search,
  });

  if (isLoading) {
    return <LoadingState message="Loading employees..." />;
  }

  if (isError) {
    return (
      <ErrorState
        message="Failed to load employees."
        onRetry={() => refetch()}
      />
    );
  }

  const employees: Employee[] = Array.isArray(data)
    ? data
    : data?.items ?? [];

  const filteredEmployees = employees.filter(
    (employee) => {
      const value = search.toLowerCase();

      return (
        employee.employee_code
          .toLowerCase()
          .includes(value) ||
        employee.full_name
          .toLowerCase()
          .includes(value) ||
        employee.email
          .toLowerCase()
          .includes(value)
      );
    },
  );

  return (
    <Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Box>
          <Typography variant="h4">
            Employees
          </Typography>

          <Typography color="text.secondary">
            Manage employees and employee information.
          </Typography>
        </Box>

        <Button
          component={Link}
          to="/employees/new"
          type="button"
          variant="contained"
        >
          Add Employee
        </Button>
      </Box>

      <TextField
        label="Search employees"
        value={search}
        onChange={(event) =>
          setSearch(event.target.value)
        }
        fullWidth
        sx={{ mb: 3 }}
      />

      {filteredEmployees.length === 0 ? (
        <Paper>
          <EmptyState
            title="No employees found"
            message="No employees match your search."
          />
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>

                <TableCell>
                  Employee Code
                </TableCell>

                <TableCell>Name</TableCell>

                <TableCell>Email</TableCell>

                <TableCell>
                  Department
                </TableCell>

                <TableCell>
                  Job Title
                </TableCell>

                <TableCell>
                  Action
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {filteredEmployees.map(
                (employee) => (
                  <TableRow key={employee.id}>
                    <TableCell>
                      {employee.id}
                    </TableCell>

                    <TableCell>
                      {employee.employee_code}
                    </TableCell>

                    <TableCell>
                      {employee.full_name}
                    </TableCell>

                    <TableCell>
                      {employee.email}
                    </TableCell>

                    <TableCell>
                      {employee.department}
                    </TableCell>

                    <TableCell>
                      {employee.job_title}
                    </TableCell>

                    <TableCell>
                      <Button
                        component={Link}
                        to={`/employees/${employee.id}`}
                        size="small"
                        variant="outlined"
                      >
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ),
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}

export default Employees;
