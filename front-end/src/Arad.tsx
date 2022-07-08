import { Outlet } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';
import './Arad.css';


const Arad = () => {
  return (
      <div className="arad">
        <Header />
        <div className="content">
          <Outlet />
        </div> 
        <Footer />
      </div>
  );
}

export { Arad };
