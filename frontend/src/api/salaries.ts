import apiClient from "./client";

export interface Salary {
  id: number;
  employee_id: number;
  base_salary: number;
  bonus: number;
  currency: string;
  effective_from: string;
  effective_to: string | null;
}

export interface SalaryInput {
  base_salary: number;
  bonus: number;
  currency: string;
  effective_from: string;
  effective_to: string | null;
}

export async function getEmployeeSalaries(
  employeeId: number,
): Promise<Salary[]> {
  const response = await apiClient.get<Salary[]>(
    `/employees/${employeeId}/salaries`,
  );

  return response.data;
}

export async function getSalary(
  salaryId: number,
): Promise<Salary> {
  const response = await apiClient.get<Salary>(
    `/salaries/${salaryId}`,
  );

  return response.data;
}

export async function createSalary(
  employeeId: number,
  data: SalaryInput,
): Promise<Salary> {
  const response = await apiClient.post<Salary>(
    `/employees/${employeeId}/salaries`,
    data,
  );

  return response.data;
}

export async function updateSalary(
  salaryId: number,
  data: SalaryInput,
): Promise<Salary> {
  const response = await apiClient.put<Salary>(
    `/salaries/${salaryId}`,
    data,
  );

  return response.data;
}

export async function deleteSalary(
  salaryId: number,
): Promise<void> {
  await apiClient.delete(`/salaries/${salaryId}`);
}
