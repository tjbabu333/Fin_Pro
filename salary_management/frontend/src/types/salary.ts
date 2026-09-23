export interface Salary {
  id: number;
  employee_id: number;
  base_salary: number;
  bonus: number;
  currency: string;
  effective_from: string;
  effective_to?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface SalaryCreate {
  employee_id: number;
  base_salary: number;
  bonus?: number;
  currency: string;
  effective_from: string;
  effective_to?: string | null;
}

export interface SalaryUpdate {
  base_salary?: number;
  bonus?: number;
  currency?: string;
  effective_from?: string;
  effective_to?: string | null;
}