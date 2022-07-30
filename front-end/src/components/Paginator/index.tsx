import React from "react";

import { HStack } from "@chakra-ui/react";

import { PaginationControl } from "./components/PaginationControl";

interface PaginatorProps {
  page: number;
  totalPages: number;
  setPage: Function;
  children: React.ReactNode;
}

const Paginator = (props: PaginatorProps) => {
  const { page, setPage, totalPages, children } = props;

  return (
    <HStack verticalAlign="center">
      <PaginationControl
        content="<"
        disabled={page <= 1}
        onClick={(event) => {
          setPage(page - 1);
        }}
      />
      {children}
      <PaginationControl
        content=">"
        disabled={page >= totalPages}
        onClick={(event) => {
          setPage(page + 1);
        }}
      />
    </HStack>
  );
};

export { Paginator };
