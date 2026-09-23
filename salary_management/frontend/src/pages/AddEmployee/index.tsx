import {
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { createEmployee } from "../../api/employees";

const employeeSchema = z.object({
  employee_code: z
    .string()
    .trim()
    .min(1, "Employee code is required"),

  full_name: z
    .string()
    .trim()
    .min(2, "Full name must be at least 2 characters"),

  email: z
    .string()
    .trim()
    .email("Enter a valid email address"),

  country: z
    .string()
    .trim()
    .min(1, "Country is required"),

  department: z
    .string()
    .trim()
    .min(1, "Department is required"),

  job_title: z
    .string()
    .trim()
    .min(1, "Job title is required"),

  status: z
    .string()
    .trim()
    .min(1, "Status is required"),
});

type EmployeeFormData = z.infer<typeof employeeSchema>;

function AddEmployee() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [serverError, setServerError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<EmployeeFormData>({
    resolver: zodResolver(employeeSchema),
    defaultValues: {
      employee_code: "",
      full_name: "",
      email: "",
      country: "",
      department: "",
      job_title: "",
      status: "ACTIVE",
    },
  });

  const onSubmit = async (form: EmployeeFormData) => {
    setServerError("");

    try {
      await createEmployee(form);

      await queryClient.invalidateQueries({
        queryKey: ["employees"],
      });

      navigate("/employees");
    } catch (err: any) {
      setServerError(
        err?.response?.data?.error?.message ||
          "Failed to create employee.",
      );
    }
  };

  return (
    <Box>
      <Typography
        variant="h4"
        gutterBottom
      >
        Add Employee
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 3 }}
      >
        Create a new employee record.
      </Typography>

      <Card>
        <CardContent>
          <Box
            component="form"
            onSubmit={handleSubmit(onSubmit)}
            noValidate
          >
            <Stack spacing={3}>
              <TextField
                label="Employee Code"
                {...register("employee_code")}
                error={Boolean(errors.employee_code)}
                helperText={errors.employee_code?.message}
                fullWidth
              />

              <TextField
                label="Full Name"
                {...register("full_name")}
                error={Boolean(errors.full_name)}
                helperText={errors.full_name?.message}
                fullWidth
              />

              <TextField
                label="Email"
                type="email"
                {...register("email")}
                error={Boolean(errors.email)}
                helperText={errors.email?.message}
                fullWidth
              />

              <TextField
                label="Country"
                {...register("country")}
                error={Boolean(errors.country)}
                helperText={errors.country?.message}
                fullWidth
              />

              <TextField
                label="Department"
                {...register("department")}
                error={Boolean(errors.department)}
                helperText={errors.department?.message}
                fullWidth
              />

              <TextField
                label="Job Title"
                {...register("job_title")}
                error={Boolean(errors.job_title)}
                helperText={errors.job_title?.message}
                fullWidth
              />

              <TextField
                label="Status"
                {...register("status")}
                error={Boolean(errors.status)}
                helperText={errors.status?.message}
                fullWidth
              />

              {serverError && (
                <Typography color="error">
                  {serverError}
                </Typography>
              )}

              <Stack
                direction="row"
                spacing={2}
                justifyContent="flex-end"
              >
                <Button
                  type="button"
                  variant="outlined"
                  onClick={() =>
                    navigate("/employees")
                  }
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>

                <Button
                  type="submit"
                  variant="contained"
                  disabled={isSubmitting}
                >
                  {isSubmitting
                    ? "Saving..."
                    : "Save Employee"}
                </Button>
              </Stack>
            </Stack>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}

export default AddEmployee;
