import { useQuery } from "@tanstack/react-query";
import { getEmployee } from "../api/employees";

export function useEmployee(
  employeeId: number | undefined
) {
  return useQuery({
    queryKey: ["employee", employeeId],
    queryFn: () => getEmployee(employeeId!),
    enabled: Boolean(employeeId),
  });
}