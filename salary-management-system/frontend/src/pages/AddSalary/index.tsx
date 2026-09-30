import { Box, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";

import SalaryForm from "../../components/salaries/SalaryForm";

import type { SalaryInput } from "../../api/salaries";

import { getSalary } from "../../api/salaries";

import { useCreateSalary, useUpdateSalary } from "../../hooks/useSalaries";

import { useEffect, useState } from "react";

import type { Salary } from "../../types/salary";

function AddSalary() {
  const { employeeId, salaryId } = useParams<{
    employeeId: string;
    salaryId?: string;
  }>();

  const navigate = useNavigate();

  const parsedEmployeeId = Number(employeeId);
  const parsedSalaryId = Number(salaryId);

  const [initialData, setInitialData] = useState<Salary | undefined>(undefined);

  const [loadError, setLoadError] = useState("");

  const createSalaryMutation = useCreateSalary(parsedEmployeeId);

  const updateSalaryMutation = useUpdateSalary(parsedEmployeeId);

  const isEditMode = Boolean(salaryId);

  useEffect(() => {
    if (!isEditMode || !Number.isFinite(parsedSalaryId)) {
      return;
    }

    const loadSalary = async () => {
      try {
        setLoadError("");

        const salary = await getSalary(parsedSalaryId);

        setInitialData(salary);
      } catch {
        setLoadError("Failed to load salary.");
      }
    };

    loadSalary();
  }, [isEditMode, parsedSalaryId]);

  const handleSubmit = (data: SalaryInput) => {
    if (isEditMode) {
      updateSalaryMutation.mutate(
        {
          salaryId: parsedSalaryId,
          salary: data,
        },
        {
          onSuccess: () => {
            navigate(`/employees/${parsedEmployeeId}/salaries`);
          },
        },
      );

      return;
    }

    createSalaryMutation.mutate(data, {
      onSuccess: () => {
        navigate(`/employees/${parsedEmployeeId}/salaries`);
      },
    });
  };

  const isSubmitting =
    createSalaryMutation.isPending || updateSalaryMutation.isPending;

  if (isEditMode && !initialData && !loadError) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Edit Salary
        </Typography>

        <Typography>Loading salary...</Typography>
      </Box>
    );
  }

  if (loadError) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Edit Salary
        </Typography>

        <Typography color="error">{loadError}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        {isEditMode ? "Edit Salary" : "Add Salary"}
      </Typography>

      <SalaryForm
        initialData={initialData}
        onSubmit={handleSubmit}
        onCancel={() => navigate(`/employees/${parsedEmployeeId}/salaries`)}
        isSubmitting={isSubmitting}
      />
    </Box>
  );
}

export default AddSalary;
