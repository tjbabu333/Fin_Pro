import {
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import AppLayout from "../layouts/AppLayout";

import Dashboard from "../pages/Dashboard";
import Employees from "../pages/Employees";
import EmployeeDetails from "../pages/EmployeeDetails";
import SalaryHistory from "../pages/SalaryHistory";
import Analytics from "../pages/Analytics";
import AddSalary from "../pages/AddSalary";
import AddEmployee from "../pages/AddEmployee";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route
          path="/"
          element={
            <Navigate
              to="/dashboard"
              replace
            />
          }
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/employees"
          element={<Employees />}
        />

        <Route
          path="/employees/new"
          element={<AddEmployee />}
        />

        <Route
          path="/employees/:id"
          element={<EmployeeDetails />}
        />

        <Route
          path="/employees/:id/salaries"
          element={<SalaryHistory />}
        />

        <Route
          path="/employees/:employeeId/salaries/new"
          element={<AddSalary />}
        />

        <Route
            path="/employees/:employeeId/salaries/:salaryId/edit"
            element={<AddSalary />}
        />

        <Route
          path="/analytics"
          element={<Analytics />}
        />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
