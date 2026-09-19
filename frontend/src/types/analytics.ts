export interface AnalyticsSummary {
  total_employees: number;
  total_salary_records: number;
  total_base_salary: number;
  total_bonus: number;
  average_salary: number;
}

export interface DepartmentAnalytics {
  department: string;
  employee_count: number;
  average_salary: number;
  total_salary: number;
}

export interface Analytics {
  summary: AnalyticsSummary;
  departments: DepartmentAnalytics[];
}