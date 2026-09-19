import { Box, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";

import SalaryForm from "../../components/salaries/SalaryForm";

import type { SalaryInput } from "../../api/salaries";

import {
  useCreateSalary,
  useUpdateSalary,
} from "../../hooks/useSalaries";

function AddSalary() {
  const { employeeId, salaryId } = useParams<{
    employeeId: string;
    salaryId?: string;
  }>();

  const navigate = useNavigate();

  const parsedEmployeeId = Number(employeeId);
  const parsedSalaryId = Number(salaryId);

  const createSalaryMutation =
    useCreateSalary(parsedEmployeeId);

  const updateSalaryMutation =
    useUpdateSalary(parsedEmployeeId);

  const isEditMode = Boolean(salaryId);

  const handleSubmit = (data: SalaryInput) => {
    if (isEditMode) {
      updateSalaryMutation.mutate(
        {
          salaryId: parsedSalaryId,
          salary: data,
        },
        {
          onSuccess: () => {
            navigate(
              `/employees/${parsedEmployeeId}/salaries`,
            );
          },
        },
      );

      return;
    }

    createSalaryMutation.mutate(data, {
      onSuccess: () => {
        navigate(
          `/employees/${parsedEmployeeId}/salaries`,
        );
      },
    });
  };

  const isSubmitting =
    createSalaryMutation.isPending ||
    updateSalaryMutation.isPending;

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        {isEditMode ? "Edit Salary" : "Add Salary"}
      </Typography>

      <SalaryForm
        onSubmit={handleSubmit}
        onCancel={() =>
          navigate(
            `/employees/${parsedEmployeeId}/salaries`,
          )
        }
        isSubmitting={isSubmitting}
      />
    </Box>
  );
}

export default AddSalary;
