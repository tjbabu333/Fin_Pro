import { Pagination as MuiPagination } from "@mui/material";

interface PaginationProps {
  page: number;
  count: number;
  onChange: (
    event: React.ChangeEvent<unknown>,
    page: number
  ) => void;
}

function Pagination({
  page,
  count,
  onChange,
}: PaginationProps) {
  if (count <= 1) {
    return null;
  }

  return (
    <MuiPagination
      page={page}
      count={count}
      onChange={onChange}
      color="primary"
      sx={{
        display: "flex",
        justifyContent: "center",
        mt: 3,
      }}
    />
  );
}

export default Pagination;