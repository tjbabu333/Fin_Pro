import apiClient from "./client";
import type {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
} from "../types/employee";

export interface EmployeeListParams {
  page?: number;
  page_size?: number;
  search?: string;
  department?: string;
}

export interface EmployeeListResponse {
  items: Employee[];
  total: number;
  page?: number;
  page_size?: number;
  pages?: number;
}

export async function getEmployees(
  params?: EmployeeListParams
): Promise<Employee[] | EmployeeListResponse> {
  const response = await apiClient.get("/employees", {
    params,
  });

  return response.data;
}

export async function getEmployee(
  employeeId: number
): Promise<Employee> {
  const response = await apiClient.get(
    `/employees/${employeeId}`
  );

  return response.data;
}

export async function createEmployee(
  employee: EmployeeCreate
): Promise<Employee> {
  const response = await apiClient.post(
    "/employees",
    employee
  );

  return response.data;
}

export async function updateEmployee(
  employeeId: number,
  employee: EmployeeUpdate
): Promise<Employee> {
  const response = await apiClient.patch(
    `/employees/${employeeId}`,
    employee
  );

  return response.data;
}