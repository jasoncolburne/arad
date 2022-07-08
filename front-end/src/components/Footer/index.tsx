import { Link } from "react-router-dom"; 

import "./index.css"

const Footer = () => {
  return (
    <footer>
      <div className="footer">
        <div className="left">
          Accessible Research Article Database
        </div>
        <div className="right">
          <Link to='/logout'>Logout</Link>
        </div>
      </div>
    </footer>
  );
}

export { Footer };
