import { Box, ChakraProvider, theme } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';

import { ApplicationState } from './datatypes/ApplicationState';

import { GlobalState } from './GlobalState';

import './Arad.css';

const initialState: ApplicationState = {
  user: {
    id: '',
    email: '',
  },
  roles: [],
}

const Arad = () => {
  return (
    <GlobalState value={initialState}>
      <ChakraProvider theme={theme}>
        <Box className="arad">
          <Header />
          <Box className="content">
            <Outlet />
          </Box>
          <Footer />
        </Box>
      </ChakraProvider>
    </GlobalState>
  );
}

export { Arad };
