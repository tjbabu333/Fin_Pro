export interface Employee {
  id: number;
  employee_code: string;
  full_name: string;
  email: string;
  country: string;
  department?: string | null;
  job_title?: string | null;
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface EmployeeCreate {
  employee_code: string;
  full_name: string;
  email: string;
  country: string;
  department?: string;
  job_title?: string;
  status?: string;
}

export interface EmployeeUpdate {
  full_name?: string;
  email?: string;
  country?: string;
  department?: string;
  job_title?: string;
  status?: string;
}