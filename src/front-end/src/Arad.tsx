import React from "react";

import { Box, ChakraProvider, theme } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";

import { Header } from "./components/Header";
import { Footer } from "./components/Footer";

import { emptyState } from "./datatypes/ApplicationState";

import { GlobalState } from "./GlobalState";

import "./Arad.css";

const currentHostname = window.location.hostname;

const Arad = () => {
  return (
    <GlobalState value={emptyState}>
      <ChakraProvider theme={theme}>
        <Box className="arad">
          <Header />
          <Box className="content" overflowY="auto">
            <Outlet />
          </Box>
          <Footer />
        </Box>
      </ChakraProvider>
    </GlobalState>
  );
};

export { Arad, currentHostname };
