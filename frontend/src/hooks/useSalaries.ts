import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createSalary,
  getEmployeeSalaries,
  updateSalary,
} from "../api/salaries";

import type { SalaryInput } from "../api/salaries";

export function useSalaries(
  employeeId: number | undefined,
) {
  return useQuery({
    queryKey: ["salaries", employeeId],
    queryFn: () =>
      getEmployeeSalaries(employeeId!),
    enabled: Boolean(employeeId),
  });
}

export function useCreateSalary(
  employeeId: number,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (salary: SalaryInput) =>
      createSalary(employeeId, salary),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["salaries", employeeId],
      });

      queryClient.invalidateQueries({
        queryKey: ["analytics"],
      });
    },
  });
}

export function useUpdateSalary(
  employeeId: number,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      salaryId,
      salary,
    }: {
      salaryId: number;
      salary: SalaryInput;
    }) =>
      updateSalary(salaryId, salary),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["salaries", employeeId],
      });

      queryClient.invalidateQueries({
        queryKey: ["analytics"],
      });
    },
  });
}
