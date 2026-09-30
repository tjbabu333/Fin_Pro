import { useQuery } from "@tanstack/react-query";

import { getEmployees } from "../api/employees";
import type { EmployeeListParams } from "../api/employees";

export function useEmployees(
  params?: EmployeeListParams,
) {
  return useQuery({
    queryKey: ["employees", params],
    queryFn: () => getEmployees(params),
  });
}
