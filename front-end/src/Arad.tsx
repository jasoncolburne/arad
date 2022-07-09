import { Outlet } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';

import { ApplicationState } from './datatypes/ApplicationState';

import { GlobalState } from './GlobalState';

import './Arad.css';

const initialState: ApplicationState = {
  user: {
    roles: [],
    email: '',
  }
}

const Arad = () => {
  return (
    <GlobalState value={initialState}>
      <div className="arad">
        <Header />
        <div className="content">
          <Outlet />
        </div> 
        <Footer />
      </div>
    </GlobalState>
  );
}

export { Arad };
