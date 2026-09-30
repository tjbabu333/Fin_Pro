import {
  Box,
  Button,
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
} from "@mui/material";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import type { SalaryInput } from "../../api/salaries";
import type { Salary } from "../../types/salary";

const salarySchema = z
  .object({
    base_salary: z
      .number()
      .min(0, "Base salary cannot be negative"),

    bonus: z
      .number()
      .min(0, "Bonus cannot be negative"),

    currency: z
      .string()
      .length(3, "Currency must be 3 characters"),

    effective_from: z
      .string()
      .min(1, "Effective from date is required"),

    effective_to: z
      .string()
      .optional()
      .or(z.literal("")),
  })
  .refine(
    (data) =>
      !data.effective_to ||
      data.effective_to >= data.effective_from,
    {
      message:
        "Effective to date cannot be before effective from date",
      path: ["effective_to"],
    },
  );

type SalaryFormValues = z.infer<typeof salarySchema>;

interface SalaryFormProps {
  initialData?: Salary;
  onSubmit: (data: SalaryInput) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
}

function SalaryForm({
  initialData,
  onSubmit,
  onCancel,
  isSubmitting = false,
}: SalaryFormProps) {
  const {
    control,
    handleSubmit,
  } = useForm<SalaryFormValues>({
    resolver: zodResolver(salarySchema),
    defaultValues: {
      base_salary: initialData?.base_salary ?? 0,
      bonus: initialData?.bonus ?? 0,
      currency: initialData?.currency ?? "USD",
      effective_from:
        initialData?.effective_from ?? "",
      effective_to:
        initialData?.effective_to ?? "",
    },
  });

  const submitForm = (values: SalaryFormValues) => {
    const data: SalaryInput = {
      base_salary: values.base_salary,
      bonus: values.bonus,
      currency: values.currency.toUpperCase(),
      effective_from: values.effective_from,
      effective_to: values.effective_to || null,
    };

    onSubmit(data);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(submitForm)}
    >
      <Stack spacing={3}>
        <Controller
          name="base_salary"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              type="number"
              label="Base Salary"
              fullWidth
              error={Boolean(fieldState.error)}
              helperText={fieldState.error?.message}
              inputProps={{
                min: 0,
                step: "0.01",
              }}
              onChange={(event) =>
                field.onChange(
                  event.target.value === ""
                    ? 0
                    : Number(event.target.value),
                )
              }
            />
          )}
        />

        <Controller
          name="bonus"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              type="number"
              label="Bonus"
              fullWidth
              error={Boolean(fieldState.error)}
              helperText={fieldState.error?.message}
              inputProps={{
                min: 0,
                step: "0.01",
              }}
              onChange={(event) =>
                field.onChange(
                  event.target.value === ""
                    ? 0
                    : Number(event.target.value),
                )
              }
            />
          )}
        />

        <Controller
          name="currency"
          control={control}
          render={({ field, fieldState }) => (
            <FormControl
              fullWidth
              error={Boolean(fieldState.error)}
            >
              <InputLabel>Currency</InputLabel>

              <Select
                {...field}
                label="Currency"
              >
                <MenuItem value="USD">USD</MenuItem>
                <MenuItem value="EUR">EUR</MenuItem>
                <MenuItem value="GBP">GBP</MenuItem>
                <MenuItem value="INR">INR</MenuItem>
              </Select>

              {fieldState.error && (
                <FormHelperText>
                  {fieldState.error.message}
                </FormHelperText>
              )}
            </FormControl>
          )}
        />

        <Controller
          name="effective_from"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              type="date"
              label="Effective From"
              fullWidth
              error={Boolean(fieldState.error)}
              helperText={fieldState.error?.message}
              slotProps={{
                inputLabel: {
                  shrink: true,
                },
              }}
            />
          )}
        />

        <Controller
          name="effective_to"
          control={control}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              type="date"
              label="Effective To"
              fullWidth
              error={Boolean(fieldState.error)}
              helperText={fieldState.error?.message}
              slotProps={{
                inputLabel: {
                  shrink: true,
                },
              }}
            />
          )}
        />

        <Stack
          direction="row"
          spacing={2}
          justifyContent="flex-end"
        >
          <Button
            type="button"
            variant="outlined"
            onClick={onCancel}
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
              : initialData
                ? "Update Salary"
                : "Save Salary"}
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
}

export default SalaryForm;
